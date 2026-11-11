#!/usr/bin/env python3
"""Music: tracks by Kevin MacLeod (incompetech.com), licensed CC BY 4.0 (see LICENSES.md).
Downloads each MP3 once into tools/music_src/ and converts it to a loudness-levelled Ogg Vorbis file in
game/ExchangeTides/sounds/<slot>/<slot>.ogg. tools/gen_project.py turns every sounds/<name>/ folder into
a GameMaker sound asset. Change made (as CC BY asks us to state): volume levelled and converted to Ogg.
Needs network on first run and ffmpeg (FFMPEG env var or PATH). Run: python3 tools/music.py"""
import os, re, subprocess, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'tools', 'music_src')
SOUNDS = os.path.join(ROOT, 'game', 'ExchangeTides', 'sounds')
SRC = 'https://incompetech.com/music/royalty-free/mp3-royaltyfree/{}.mp3'
FFMPEG = os.environ.get('FFMPEG', 'ffmpeg')
TARGET_LUFS = -20.0

# slot -> exact title (shown in the credits)
TRACKS = {
    'snd_music_title': 'Teller of the Tales',
    'snd_music_port': 'Thatched Villagers',
    'snd_music_port2': 'Folk Round',
    'snd_music_tavern': 'Master of the Feast',
    'snd_music_sea': 'Achaidh Cheide',
    'snd_music_battle': 'Five Armies',
    'snd_music_battle2': 'Clash Defiant',
    'snd_music_victory': 'Lord of the Land',
}


def lufs(path):
    err = subprocess.run([FFMPEG, '-nostats', '-i', path, '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', err)[-1])


if __name__ == '__main__':
    os.makedirs(CACHE, exist_ok=True)
    for slot, title in TRACKS.items():
        mp3 = os.path.join(CACHE, title + '.mp3')
        if not os.path.exists(mp3):
            req = urllib.request.Request(SRC.format(urllib.parse.quote(title)), headers={'User-Agent': 'exchange-tides-build'})
            open(mp3, 'wb').write(urllib.request.urlopen(req, timeout=120).read())
        d = os.path.join(SOUNDS, slot)
        os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f.endswith(('.mp3', '.ogg', '.wav')):
                os.remove(os.path.join(d, f))
        ogg = os.path.join(d, slot + '.ogg')
        gain = TARGET_LUFS - lufs(mp3)
        subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', mp3, '-af', f'volume={gain:.2f}dB', '-ac', '2', '-ar', '44100',
                        '-c:a', 'libvorbis', '-q:a', '3', '-map_metadata', '-1', ogg], check=True)
        print(f'{slot}: "{title}" {lufs(ogg):.1f} LUFS {os.path.getsize(ogg) / 1e6:.1f} MB')
