#!/usr/bin/env python3
"""Generate the game's painted sprites with a local ComfyUI server.

Prompts, seeds and modes come from art_spec.json (style rules: docs/ART_STYLE.md).
  txt2img : text-to-image, then downscaled to the sprite's in-game size.
  img2img : repaints the vector sprite in tools/artgen/vector/<name>.png. This keeps composition
            and port positions; with keep_alpha the original transparency mask is reapplied.

Usage:
  python3 -I tools/artgen/comfy_gen.py --host http://HOST:8188 [--only a,b] [--variants N]
  python3 -I tools/artgen/comfy_gen.py --install [--pick name=2,...]  # copy chosen variants into the game
Uses the standard library only.
"""
import argparse, json, os, shutil, sys, time, uuid, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SPRITES = os.path.join(ROOT, 'game', 'ExchangeTides', 'datafiles', 'sprites')
VECTOR = os.path.join(HERE, 'vector')
OUT = os.path.join(HERE, 'out')
CKPT = 'DreamShaperXL_Lightning.safetensors'


def png_size(path):
    with open(path, 'rb') as f:
        b = f.read(24)
    return int.from_bytes(b[16:20], 'big'), int.from_bytes(b[20:24], 'big')


class Comfy:
    def __init__(self, host):
        self.host = host.rstrip('/')
        self.cid = uuid.uuid4().hex

    def get(self, path):
        with urllib.request.urlopen(self.host + path, timeout=60) as r:
            return r.read()

    def post_json(self, path, obj):
        req = urllib.request.Request(self.host + path, json.dumps(obj).encode(), {'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())

    def upload(self, path):
        name = 'et_' + os.path.basename(path)
        bnd = uuid.uuid4().hex
        body = (f'--{bnd}\r\nContent-Disposition: form-data; name="image"; filename="{name}"\r\n'
                'Content-Type: image/png\r\n\r\n').encode() + open(path, 'rb').read() + \
               f'\r\n--{bnd}\r\nContent-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n--{bnd}--\r\n'.encode()
        req = urllib.request.Request(self.host + '/upload/image', body, {'Content-Type': f'multipart/form-data; boundary={bnd}'})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())['name']

    def run(self, graph):
        pid = self.post_json('/prompt', {'prompt': graph, 'client_id': self.cid})['prompt_id']
        t0 = time.time()
        while time.time() - t0 < 600:
            h = json.loads(self.get('/history/' + pid))
            if pid in h:
                st = h[pid].get('status', {})
                if st.get('status_str') == 'error':
                    raise RuntimeError(json.dumps(st.get('messages', ''))[:2000])
                imgs = [im for o in h[pid]['outputs'].values() for im in o.get('images', [])]
                return [self.get('/view?' + urllib.parse.urlencode(im)) for im in imgs]
            time.sleep(0.5)
        raise TimeoutError(pid)


def build_graph(spec, a, seed, ref_name, w, h):
    s = spec['sampler']
    g = {
        'ckpt': {'class_type': 'CheckpointLoaderSimple', 'inputs': {'ckpt_name': CKPT}},
        # "style": false skips the house style (e.g. for plain textures); "negative_extra" adds per-asset avoidances.
        'pos': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['ckpt', 1], 'text': a['prompt'] + (', ' + spec['style'] if a.get('style', True) else '')}},
        'neg': {'class_type': 'CLIPTextEncode', 'inputs': {'clip': ['ckpt', 1], 'text': spec['negative'] + (', ' + a['negative_extra'] if a.get('negative_extra') else '')}},
        'ks': {'class_type': 'KSampler', 'inputs': {
            'model': ['ckpt', 0], 'positive': ['pos', 0], 'negative': ['neg', 0], 'seed': seed,
            'steps': s['steps'], 'cfg': s['cfg'], 'sampler_name': s['sampler_name'], 'scheduler': s['scheduler'],
            'denoise': a.get('denoise', 1.0), 'latent_image': ['lat', 0]}},
        'dec': {'class_type': 'VAEDecode', 'inputs': {'samples': ['ks', 0], 'vae': ['ckpt', 2]}},
        'fit': {'class_type': 'ImageScale', 'inputs': {'image': ['dec', 0], 'upscale_method': 'area',
                                                       'width': w, 'height': h, 'crop': 'center'}},
        'save': {'class_type': 'SaveImage', 'inputs': {'images': ['fit', 0], 'filename_prefix': 'et_' + a['name']}},
    }
    if a['mode'] == 'txt2img':
        gw, gh = a['size']
        g['lat'] = {'class_type': 'EmptyLatentImage', 'inputs': {'width': gw, 'height': gh, 'batch_size': 1}}
        return g
    k = a.get('scale', 1)
    g['ref'] = {'class_type': 'LoadImage', 'inputs': {'image': ref_name}}
    src = ['ref', 0]
    if a.get('keep_alpha'):
        # Flatten the transparent sprite onto a parchment backdrop before repainting.
        g['bg'] = {'class_type': 'EmptyImage', 'inputs': {'width': w, 'height': h, 'batch_size': 1,
                                                         'color': int(a.get('bg', 'E8DCC0'), 16)}}
        g['inv'] = {'class_type': 'InvertMask', 'inputs': {'mask': ['ref', 1]}}
        g['flat'] = {'class_type': 'ImageCompositeMasked', 'inputs': {
            'destination': ['bg', 0], 'source': ['ref', 0], 'x': 0, 'y': 0, 'resize_source': False, 'mask': ['inv', 0]}}
        src = ['flat', 0]
    g['up'] = {'class_type': 'ImageScale', 'inputs': {'image': src, 'upscale_method': 'bicubic',
                                                      'width': w * k, 'height': h * k, 'crop': 'disabled'}}
    g['enc'] = {'class_type': 'VAEEncode', 'inputs': {'pixels': ['up', 0], 'vae': ['ckpt', 2]}}
    g['ks']['inputs']['latent_image'] = ['enc', 0]
    if a.get('keep_alpha'):
        # The LoadImage mask is 1 where transparent; growing it erodes the alpha, trimming backdrop fringes.
        g['trim'] = {'class_type': 'GrowMask', 'inputs': {'mask': ['ref', 1], 'expand': a.get('trim', 1),
                                                          'tapered_corners': True}}
        g['alpha'] = {'class_type': 'JoinImageWithAlpha', 'inputs': {'image': ['fit', 0], 'alpha': ['trim', 0]}}
        g['save']['inputs']['images'] = ['alpha', 0]
    return g


def generate(args, spec):
    c = Comfy(args.host)
    stats = json.loads(c.get('/system_stats'))
    print('ComfyUI', stats.get('system', {}).get('comfyui_version', '?'), '|',
          ', '.join(d.get('name', '') for d in stats.get('devices', [])))
    ckpts = json.loads(c.get('/object_info/CheckpointLoaderSimple'))['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]
    if CKPT not in ckpts:
        sys.exit(f'{CKPT} not found in ComfyUI models/checkpoints (have: {ckpts})')
    os.makedirs(OUT, exist_ok=True)
    only = set(args.only.split(',')) if args.only else None
    for a in spec['assets']:
        if only and a['name'] not in only:
            continue
        sprite = os.path.join(SPRITES, a['name'] + '.png')
        vec = os.path.join(VECTOR, a.get('ref', a['name']) + '.png')
        w, h = a['out'] if 'out' in a else png_size(vec if os.path.exists(vec) else sprite)
        ref = c.upload(vec) if a['mode'] == 'img2img' else None
        for v in range(args.variants):
            t0 = time.time()
            data = c.run(build_graph(spec, a, a['seed'] + 1000 * v, ref, w, h))[0]
            path = os.path.join(OUT, f"{a['name']}_v{v}.png")
            open(path, 'wb').write(data)
            print(f"{a['name']} v{v} {w}x{h} {time.time() - t0:.1f}s -> {os.path.relpath(path, ROOT)}", flush=True)


def install(args, spec):
    picks = dict(p.split('=') for p in args.pick.split(',')) if args.pick else {}
    n = 0
    for a in spec['assets']:
        v = picks.get(a['name'], '0')
        src = os.path.join(OUT, f"{a['name']}_v{v}.png")
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(SPRITES, a['name'] + '.png'))
            n += 1
    print(f'installed {n} sprites into {os.path.relpath(SPRITES, ROOT)}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--host', default='http://127.0.0.1:8188')
    ap.add_argument('--only', default='')
    ap.add_argument('--variants', type=int, default=1)
    ap.add_argument('--install', action='store_true')
    ap.add_argument('--pick', default='')
    args = ap.parse_args()
    spec = json.load(open(os.path.join(HERE, 'art_spec.json')))
    install(args, spec) if args.install else generate(args, spec)


if __name__ == '__main__':
    main()
