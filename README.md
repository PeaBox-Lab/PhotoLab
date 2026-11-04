# PeaBox Photo Lab

**Current release:** v0.2.19  
**Version format:** `99.99.99`  
**Release ZIP naming:** `peabox-photo-lab-v<version>.zip`

A privacy-first, local photo editor for creators, bloggers, small businesses, and everyday users. It runs in a browser while Python, Streamlit, Pillow, and NumPy perform the editing.

## Highlights

- Non-destructive adjustments and live before/after preview
- Smart auto optimization and five creative presets
- Light, colour, crop, rotate, mirror, borders, and watermark controls
- Selective colour, duotone, dreamy glow, pencil sketch, pixel art, and vignette
- Dominant colour palette extraction
- Downloadable style proof sheet
- Social format pack for square, portrait, landscape, and story crops
- Image health check and fresh exports without copied EXIF metadata
- JPEG, PNG, and WebP export
- Export presets for Web High Quality, Social 1080, and Archive PNG

## Run locally

### Windows

Double-click `run_windows.bat`.

### Linux or macOS

```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```

### Manual setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Privacy

When run locally, the application processes image bytes on your computer and does not intentionally persist uploads. Exports are newly encoded and original EXIF metadata is not copied. A remote deployment necessarily receives uploaded files on that server, so operators must secure the deployment.

## Repository topics

`python`, `streamlit`, `pillow`, `photo-editor`, `image-processing`, `creator-tools`, `privacy-first`, `webp`, `peabox`

## Contributing and security

Read `CONTRIBUTING.md`. Report security issues using `SECURITY.md`, not a public issue.

## License

MIT


## v0.2.3 additions
- Black & white and negative quick effects
- Custom export width/height with optional aspect-ratio preservation
- Live output dimensions and encoded file-size preview


## v0.2.4 additions
- Adjustable Sepia effect
- Exposure Analysis in Image Inspector
- Automatic warnings for excessive deep shadows or bright highlights
- Corrected custom-dimension export flow


## v0.2.5 additions
- Portrait Soft, Cinematic, and High Key styles
- Adjustable Clarity and Noise Reduction
- Email Compact and 4K Display export presets
- Expanded proof sheet with the latest styles


## v0.2.6 additions
- Posterize and Solarize creative effects
- RGB Channel Mixer with independent 50-150% controls
- Privacy PNG lossless export preset
- Megapixel reporting alongside output resolution and encoded size


## v0.2.7 additions
- Matte/Fade creative finishing control
- Adjustable Film Grain
- Split Toning with shadow and highlight hue controls
- Photo Print high-quality JPEG export preset


## v0.2.8 additions
- Adjustable Lens Vignette with edge softness control
- Date or caption stamping in any corner
- Phone Wallpaper and Square Profile export presets


## v0.2.9 additions
- Soft Focus finishing tool for gentle diffusion
- Fine Detail enhancement for texture definition
- Messaging JPEG and Web Thumbnail WebP export presets
- Richer export summary including format and quality status


## v0.2.10 additions
- Exposure adjustment from -2.0 EV to +2.0 EV
- Adaptive Vibrance for stronger low-saturation color enhancement
- Edge Sharpen for additional structural crispness
- Portfolio and Low Bandwidth WebP presets


## v0.2.11 additions
- Gamma control from 0.50 to 2.00
- Green-to-magenta Tint correction
- Auto Levels with adjustable 0-10% cutoff
- Presentation HD and Presentation 4K export presets


## v0.2.12 additions
- Adjustable Auto White Balance based on the Gray World method
- Micro Contrast for local texture and dimensionality
- Highlight Fade for softer bright tones
- Blog Optimized WebP and Master JPEG export presets


## v0.2.13 additions
- Dehaze for improved clarity in hazy or washed-out photos
- Bloom/Glow for soft luminous highlights
- Color Cast Analysis with RGB means and channel-spread guidance
- Gallery WebP and Quick Share export presets


## v0.2.14 additions
- Texture Clarity for broader local detail enhancement
- Independent shadow-color hue/strength grading
- Independent highlight-color hue/strength grading
- Social High Quality and Proof JPEG export presets


## v0.2.15 additions
- Chromatic Pop for saturation-aware color enhancement
- Soft Skin diffusion control
- Composition Safe Area preview overlay with adjustable margins
- Mobile WebP and Client Review export presets


## v0.2.16 additions
- Monochrome Channel Mixer with independent RGB weighting
- Luminance-mask preview for highlights, midtones, and shadows
- Adjustable mask overlay opacity
- Contact Sheet Web and Lossless Master export presets


## v0.2.17 additions
- Black Point and White Point tone-range controls
- Auto Temperature Correction
- Focus Analysis with editing guidance
- Desktop Wallpaper and Fast Preview export presets


## v0.2.18 additions
- Defringe / Chromatic Cleanup for strong color-edge artifacts
- Orton Glow creative finishing effect
- Dynamic Range analysis in Image Inspector
- Marketplace JPEG and Tiny Web WebP export presets


## v0.2.19 additions
- Presence / Atmospheric Clarity from -100 to +100
- Color Density from -100 to +100
- Image Inspector clipping check for near-black and near-white channels
- Portfolio Master and Chat Optimized export presets
