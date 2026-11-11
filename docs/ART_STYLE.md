# Exchange Tides — art style

**One line:** a painted storybook of the golden age of sail. Gouache and ink, warm light, readable at small sizes.

## Rules
- **Medium:** gouache or oil-wash painting with confident ink linework. Visible but controlled brushwork. Not photographic, not 3D, not anime, not pixel art.
- **Light:** warm late-afternoon key light from the upper left, with cool teal shadows.
- **Palette:** parchment and cream (#F2E6CA), deep sea teal (#2E6E82), weathered wood browns, brass and gold (#D6AA46), and oxblood red for danger and pirates. Saturation is high in focal areas and low in the background.
- **Shapes:** clear silhouettes first. Every sprite must read at its in-game size: 64 px icons, 160×200 portraits, 260×220 ships.
- **Characters:** head and shoulders, three-quarter view, looking toward the viewer, with a painted backdrop in one dominant colour per character, chosen so the cast is easy to tell apart. Faces are expressive, slightly stylised and grounded, never cartoonish. Clothing is period-appropriate (about 1700–1750) and distinctive per role.
- **Ships:** side view facing right, centred on a transparent background. Pirate variants have darker, patched sails, and the navy has crisp white sails with blue trim.
- **Icons:** one object, centred, with a strong silhouette on a transparent background. No text.
- **Never:** text, logos, watermarks, borders or frames baked into the image. Never reuse Tradewinds assets.

## Pipeline
`tools/artgen/comfy_gen.py` drives a local ComfyUI server (model: DreamShaper XL Lightning, OpenRAIL++).
- **Portraits and title:** text-to-image, then downscaled to the sprite size.
- **Map, ships, fort and icons:** image-to-image from the vector art in `tools/artgen/gen.py`. This keeps composition, port positions and silhouettes, and the original alpha mask is reapplied afterwards.

Prompts and seeds are in `tools/artgen/art_spec.json`, so every image can be regenerated exactly.
