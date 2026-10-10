# 📷 PeaBox Photo Lab

> **Edit. Enhance. Create. Privately.**

PeaBox Photo Lab is a lightweight, privacy-first photo editing and creator toolkit built with **Python**, **Streamlit**, **Pillow**, and **NumPy**.

It is designed for users who want practical photo-editing capabilities without the complexity of a professional graphics suite.

Along with everyday image adjustments, PeaBox Photo Lab includes creative effects, smart enhancements, social-media exports, colour palette extraction, style comparisons, watermarking, image inspection, and creator-focused utilities.

---

## ✨ Highlights

- 🖥️ Simple browser-based interface
- 🔒 Privacy-first local workflow
- 🎨 Non-destructive editing
- 🪄 Smart Auto Optimize
- 🌡️ Temperature and tonal adjustments
- 🎞️ Creative presets
- 🖌️ Artistic effects
- 👀 Before/after comparison
- 📐 Social-media crop formats
- 🎨 Colour palette extraction
- 🖼️ Style comparison sheet
- 🏷️ Watermark and branding tools
- 📦 Social Format Pack export
- 🔍 Image quality inspector
- 📤 JPEG, PNG and WebP export
- 🧹 Fresh exports without copying original EXIF metadata

---

## 📑 Table of Contents

- #what-is-peabox-photo-lab
- #who-is-it-for
- #features
- #system-requirements
- #installation
- #windows-installation
- #linux-installation
- #macos-installation
- #starting-peabox-photo-lab
- #user-guide
- #photo-editing-controls
- #creative-lab
- #creator-toolkit
- #image-inspector
- #exporting-images
- #recommended-workflows
- #privacy
- #project-structure
- #troubleshooting
- #developer-guide
- #contributing
- #security
- #roadmap
- #license

---

# What is PeaBox Photo Lab?

PeaBox Photo Lab aims to provide commonly needed photo-editing and creator functions without forcing users to learn a complicated professional image editor.

The basic workflow is intentionally simple:

```text
Upload
   ↓
Enhance
   ↓
Edit
   ↓
Create
   ↓
Inspect
   ↓
Export
```

The application runs through a browser interface while Python performs the image processing.

Your original photograph is not overwritten.

---

# Who is it for?

PeaBox Photo Lab can be useful for:

- Casual photographers
- Bloggers
- Content creators
- Teachers
- Students
- Small businesses
- Social-media managers
- Website owners
- Presentation creators
- Developers
- Anyone needing quick image preparation

PeaBox Photo Lab is not intended to replace full professional image-editing applications.

Instead, its philosophy is simple:

> **Make useful image editing easy, fast, approachable and extensible.**

---

# Features

## 🎛️ Core Photo Editing

The editor includes controls for:

- Brightness
- Contrast
- Saturation
- Sharpness
- Temperature
- Shadows
- Highlights
- Rotation
- Horizontal mirror
- Vertical flip

All adjustments are non-destructive.

Changing a control regenerates the edited image from the original uploaded photograph.

---

# 🪄 Smart Auto Optimize

Not sure where to begin?

Enable:

```text
Smart Auto Optimize
```

PeaBox automatically performs a combination of tonal correction, exposure balancing and sharpening.

It is designed to provide a useful starting point before manual editing.

A simple workflow is:

```text
Upload Photo
      ↓
Smart Auto Optimize
      ↓
Review Result
      ↓
Fine-tune Manually
      ↓
Export
```

---

# 🎞️ Quick Styles

PeaBox Photo Lab provides several built-in photographic styles.

## Clean Pop

Adds a cleaner, brighter and more colourful appearance.

Useful for:

- everyday photography
- products
- travel images
- web content
- social-media posts

---

## Warm Film

Produces a warmer and slightly softer photographic treatment.

Useful for:

- travel
- lifestyle images
- portraits
- landscapes

---

## Cool Editorial

Introduces a cooler colour tone with additional contrast.

Useful for:

- architecture
- business content
- urban photography
- editorial-style images

---

## Mono Punch

Creates a high-contrast monochrome treatment.

Useful for:

- artistic photography
- architecture
- portraits
- dramatic compositions

---

## Vintage Fade

Reduces contrast and colour intensity while introducing warmer tones.

Useful for:

- retro graphics
- travel photos
- lifestyle images
- creative posts

---

# 📐 Crop Presets

PeaBox can automatically center-crop photographs using common aspect ratios.

Available options include:

```text
Original
1:1
4:5
3:2
16:9
9:16
```

## 1:1

Square format.

Useful for:

- profile images
- square posts
- thumbnails
- product photography

---

## 4:5

Portrait-oriented format.

Useful for:

- vertical posts
- product photographs
- people photography

---

## 3:2

Traditional photography-style ratio.

---

## 16:9

Widescreen format.

Useful for:

- website banners
- presentations
- thumbnails
- landscape visuals

---

## 9:16

Vertical format.

Useful for:

- mobile-first content
- stories
- vertical promotional graphics

---

> **Note:** The current crop feature uses center cropping rather than interactive drag-to-select cropping.

---

# Photo Editing Controls

## ☀️ Brightness

Controls the overall brightness of the image.

Move right to brighten the photograph.

Move left to darken it.

---

## ◐ Contrast

Controls the difference between lighter and darker areas.

Higher contrast can make an image appear stronger and more dramatic.

Lower contrast creates a softer appearance.

---

## 🌈 Saturation

Controls colour intensity.

Increase saturation for stronger colours.

Decrease saturation for more muted colours.

---

## 🔍 Sharpness

Adjusts perceived image sharpness.

Use this carefully.

Extremely high values can exaggerate noise and compression artefacts.

---

## 🌡️ Temperature

Changes the overall colour temperature.

Positive values create a warmer appearance.

Negative values create a cooler appearance.

---

## 🌑 Shadows

Adjusts darker areas of the image.

Increasing shadows can help reveal details in dark areas.

---

## ☀️ Highlights

Adjusts brighter areas of the photograph.

This can help balance images with bright regions.

---

# 🎨 Creative Lab

PeaBox includes a collection of creative image effects.

Open:

```text
Creative add-ons
```

Choose an effect and adjust:

```text
Effect Strength
```

---

# 🎯 Selective Colour Pop

Selective Colour Pop keeps colours around a selected hue while shifting other areas toward grayscale.

Controls include:

```text
Colour-pop hue
Hue range
```

A narrower range isolates colours more aggressively.

A wider range keeps more surrounding colours.

Useful for:

- product photography
- advertisements
- posters
- visual storytelling
- creative social posts

---

# 🌗 Duotone

Duotone converts the image into a design based primarily on two colours.

Choose:

```text
Duotone Shadows
Duotone Highlights
```

Example:

```text
Shadows:    #172554
Highlights: #FBBF24
```

This creates a navy-and-gold visual treatment.

Useful for:

- posters
- thumbnails
- presentation graphics
- brand visuals
- album-style artwork

---

# ✨ Dreamy Glow

Adds a soft glowing appearance.

Particularly useful for:

- landscapes
- portraits
- lifestyle photographs
- travel images
- atmospheric photographs

Adjust:

```text
Effect Strength
```

to control the intensity.

---

# ✏️ Pencil Sketch

Transforms a photograph into a sketch-like interpretation.

Reducing the effect strength can produce an interesting mixture of the original photograph and the sketch effect.

---

# 👾 Pixel Art

Transforms the photograph into pixel-style artwork.

Adjust:

```text
Pixel Size
```

Smaller blocks preserve more detail.

Larger blocks create stronger pixelation.

Useful for:

- retro art
- gaming visuals
- avatars
- experimental graphics
- creative posts

---

# 🎯 Focus Vignette

Gradually darkens areas near the edges of the photograph.

This can help focus attention toward the centre of the image.

Increase:

```text
Effect Strength
```

for a stronger vignette.

---

# 🏷️ Branding Tools

PeaBox Photo Lab includes simple tools for preparing images for publishing.

Open:

```text
Brand kit and finishing
```

---

## Watermarks

Enter your desired watermark.

Example:

```text
PeaBox Labs
```

Available positions include:

```text
Bottom right
Bottom left
Top right
Top left
Center
```

You can also change:

```text
Watermark opacity
```

---

## Borders

Add a border to the finished photograph.

Configure:

```text
Border width
Border colour
```

Example:

```text
Width: 2%
Colour: #FFFFFF
```

This creates a simple white frame.

---

# 👀 Before and After Comparison

Open:

```text
Editor
```

Enable:

```text
Before and after view
```

The application displays:

```text
Original          Edited
   ↓                 ↓
Before            After
```

This is particularly useful for judging whether editing has improved the photograph.

---

# 🧰 Creator Toolkit

The **Creator Toolkit** provides additional utilities intended for bloggers, marketers, creators and small businesses.

Open:

```text
Creator Toolkit
```

---

# 🎨 Colour Palette Extractor

PeaBox examines the edited photograph and extracts prominent colours.

Example output:

```text
#172554
#2563EB
#F59E0B
#F8FAFC
#334155
#94A3B8
```

Colours are displayed visually and provided in JSON.

Example:

```json
{
    "palette": [
        "#172554",
        "#2563EB",
        "#F59E0B",
        "#F8FAFC",
        "#334155",
        "#94A3B8"
    ]
}
```

This can be useful for:

- website themes
- presentation themes
- branding
- social-media graphics
- blog design
- complementary designs

---

# 🖼️ Style Proof Sheet

Instead of testing every preset individually, PeaBox can create a comparison sheet.

The sheet includes:

```text
Original
Clean Pop
Warm Film
Cool Editorial
Mono Punch
Vintage Fade
```

Select:

```text
Download style proof sheet
```

PeaBox generates an image containing the different variants.

This makes choosing a photographic style easier.

---

# 📱 Social Format Pack

A single photograph often needs several different sizes for publishing.

PeaBox can automatically create several aspect-ratio variants.

Current formats include:

```text
Square 1:1
Portrait 4:5
Landscape 16:9
Story 9:16
```

Select:

```text
Download social format pack (ZIP)
```

PeaBox generates the images and packages them into a ZIP archive.

Instead of:

```text
Crop
Export
Crop again
Export again
Crop again
Export again
```

you can use:

```text
Edit once
    ↓
Generate Social Pack
    ↓
Download ZIP
```

---

# 🔍 Image Inspector

Open:

```text
Image Inspector
```

The inspector displays information including:

```text
Width
Height
Megapixels
Aspect Ratio
Resolution Health
```

Example:

```text
Width:       4032
Height:      3024
Megapixels:  12.2 MP
Aspect:      1.33:1
```

PeaBox also provides a basic warning when an image may be relatively small for larger exports.

This warning is intended as convenience guidance rather than a universal image-quality standard.

---

# System Requirements

Recommended environment:

```text
Python 3.10+
Windows / Linux / macOS
Modern web browser
```

Main Python dependencies:

```text
Streamlit
Pillow
NumPy
```

Dependencies are listed in:

```text
requirements.txt
```

---

# Installation

You can either clone the repository using Git or download the project as a ZIP file from GitHub.

---

# Clone with Git

```bash
git clone YOUR_REPOSITORY_URL
```

Enter the project directory:

```bash
cd peabox-photo-lab
```

---

# Windows Installation

## Easiest Method

PeaBox includes:

```text
run_windows.bat
```

Double-click this file.

The launcher will:

```text
Create virtual environment
        ↓
Activate environment
        ↓
Install dependencies
        ↓
Start Streamlit
        ↓
Launch PeaBox Photo Lab
```

---

# Manual Windows Installation

Open **Command Prompt** or **PowerShell** inside the project directory.

First check Python:

```powershell
py --version
```

Create a virtual environment:

```powershell
py -3 -m venv .venv
```

---

## Activate from Command Prompt

```cmd
.venv\Scripts\activate
```

---

## Activate from PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start PeaBox:

```powershell
python -m streamlit run app.py
```

---

# ⚠️ Important Note for Windows Users

Do **not** use:

```bash
source .venv/bin/activate
```

inside regular PowerShell or Command Prompt.

That command is intended for Unix-style shells.

Use:

```powershell
.\.venv\Scripts\Activate.ps1
```

in PowerShell.

Or:

```cmd
.venv\Scripts\activate
```

in Command Prompt.

---

# Linux Installation

Open a terminal and enter the project directory:

```bash
cd peabox-photo-lab
```

Make the launcher executable:

```bash
chmod +x run_linux_mac.sh
```

Run:

```bash
./run_linux_mac.sh
```

---

## Manual Linux Installation

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start:

```bash
python -m streamlit run app.py
```

---

# macOS Installation

Open Terminal.

Enter the project directory:

```bash
cd peabox-photo-lab
```

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install:

```bash
python -m pip install -r requirements.txt
```

Start:

```bash
python -m streamlit run app.py
```

Or use:

```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```

---

# Starting PeaBox Photo Lab

Once everything is installed:

```bash
python -m streamlit run app.py
```

Your terminal will display the local Streamlit address.

Open that address in a browser.

---

# User Guide

## Step 1: Upload a photograph

Click:

```text
Browse files
```

Choose an image.

Supported formats in the current application include:

```text
JPG
JPEG
PNG
WebP
```

---

# Step 2: Select a Quick Style

Choose:

```text
None
Clean Pop
Warm Film
Cool Editorial
Mono Punch
Vintage Fade
```

If you want complete manual control, leave this set to:

```text
None
```

---

# Step 3: Try Smart Auto Optimize

Enable:

```text
Smart Auto Optimize
```

Review the result.

You can then fine-tune the photograph manually.

---

# Step 4: Select a Crop

Choose:

```text
Original
1:1
4:5
3:2
16:9
9:16
```

Choose the ratio based on where you plan to use the image.

---

# Step 5: Adjust Lighting

Use:

```text
Brightness
Contrast
Shadows
Highlights
```

An example starting point might be:

```text
Brightness:   +5
Contrast:    +10
Shadows:     +10
Highlights:   -5
```

This is only an example.

Every photograph is different.

---

# Step 6: Adjust Colour

Use:

```text
Saturation
Temperature
```

For warmer photographs:

```text
Temperature → Positive
```

For cooler photographs:

```text
Temperature → Negative
```

---

# Step 7: Adjust Sharpness

Use:

```text
Sharpness
```

Avoid excessive sharpening, particularly on compressed or noisy images.

---

# Step 8: Try a Creative Effect

Open:

```text
Creative add-ons
```

Choose:

```text
Selective Colour Pop
Duotone
Dreamy Glow
Pencil Sketch
Pixel Art
Focus Vignette
```

Adjust:

```text
Effect Strength
```

until you are satisfied with the result.

---

# Step 9: Add Branding

Open:

```text
Brand kit and finishing
```

Configure:

```text
Watermark
Watermark position
Watermark opacity

Border
Border colour
```

---

# Step 10: Inspect the Image

Open:

```text
Image Inspector
```

Review:

```text
Dimensions
Megapixels
Aspect ratio
Resolution health
```

---

# Step 11: Export

Open:

```text
3. Export
```

Select your file format:

```text
JPEG
PNG
WEBP
```

Set quality.

Example:

```text
JPEG
Quality: 92
```

Choose a maximum long edge:

```text
Original
4096
2560
2048
1600
1080
```

Enter your filename.

Example:

```text
my-edited-photo
```

Finally click:

```text
Download edited photo
```

---

# Exporting Images

## JPEG

Suitable for:

- photographs
- blogs
- websites
- social sharing
- general image use

JPEG allows adjustable export quality.

---

## PNG

Useful for:

- lossless PNG output
- graphics
- screenshots
- assets where PNG is preferred

PNG files can be larger than equivalent photographic JPEG or WebP files.

---

## WebP

Useful for:

- websites
- blogs
- modern web workflows

PeaBox provides adjustable WebP quality.

---

# Recommended Workflows

## ⚡ Quick Photo Enhancement

```text
Upload
   ↓
Smart Auto Optimize
   ↓
Clean Pop
   ↓
Fine-tune brightness
   ↓
Export JPEG
```

---

## 🌐 Blog Image

```text
Upload
   ↓
16:9 Crop
   ↓
Smart Auto
   ↓
Adjust Contrast
   ↓
Add Watermark
   ↓
Resize
   ↓
Export JPEG/WebP
```

---

## 📱 Social Publishing

```text
Upload
   ↓
Edit Master Image
   ↓
Creator Toolkit
   ↓
Generate Social Format Pack
   ↓
Download ZIP
```

---

## 🎨 Brand Palette Discovery

```text
Upload Image
   ↓
Edit
   ↓
Creator Toolkit
   ↓
Colour Palette Extractor
   ↓
Copy HEX Values
```

---

## 🖌️ Artistic Image

```text
Upload
   ↓
Creative Add-ons
   ↓
Choose Effect
   ↓
Adjust Strength
   ↓
Add Border
   ↓
Export
```

---

# Privacy

Privacy is an important design principle of PeaBox Photo Lab.

When the application is run locally, processing takes place through the locally running Python application.

The current PeaBox application:

- reads uploaded images for processing
- processes them in the application process
- creates export data in memory
- does not intentionally save uploaded photographs into a persistent application image library
- creates a freshly encoded image for export
- does not copy the original photograph's EXIF metadata into the exported image

---

# EXIF Metadata

The current export process creates a newly encoded image.

Original EXIF metadata is not intentionally copied into the exported image.

This can help avoid unintentionally preserving source metadata in the edited version.

If metadata privacy is critically important, independently inspect sensitive images before publication.

---

# Local vs Remote Deployment

There is an important difference between running PeaBox locally and deploying it to a server.

## Local

```text
Browser
   ↓
Local Streamlit
   ↓
Local Python
   ↓
Image Processing
```

The software and image processing run on your computer.

---

## Remote Deployment

```text
Browser
   ↓
Internet
   ↓
Remote Streamlit Server
   ↓
Image Processing
```

A remotely hosted version necessarily receives uploaded image data on the server.

Remote deployments should therefore consider:

- HTTPS
- authentication
- infrastructure security
- access control
- server logging
- temporary image handling
- retention policies
- backups
- privacy requirements

---

# Project Structure

```text
peabox-photo-lab/
│
├── app.py
├── requirements.txt
├── pyproject.toml
│
├── run_windows.bat
├── run_linux_mac.sh
│
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE
│
├── .gitignore
├── .editorconfig
│
└── .github/
    │
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.yml
    │   ├── feature_request.yml
    │   └── config.yml
    │
    ├── workflows/
    │   └── python-checks.yml
    │
    ├── dependabot.yml
    └── pull_request_template.md
```

---

# Troubleshooting

## Python is not recognized

Try:

```powershell
py --version
```

or:

```powershell
python --version
```

If neither command works, install Python and reopen your terminal.

---

## `source` is not recognized on Windows

Do not use:

```bash
source .venv/bin/activate
```

from Windows Command Prompt or normal PowerShell.

### Command Prompt

Use:

```cmd
.venv\Scripts\activate
```

### PowerShell

Use:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

# PowerShell Blocks Activate.ps1

You can run the virtual environment without activating it.

Install dependencies with:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Then start PeaBox with:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

---

# `streamlit` is not recognized

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Then use:

```bash
python -m streamlit run app.py
```

instead of:

```bash
streamlit run app.py
```

---

# ModuleNotFoundError

Example:

```text
ModuleNotFoundError: No module named 'PIL'
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Make sure you are using the same Python environment that PeaBox uses.

---

# Image Will Not Upload

Check that the file is one of the supported types:

```text
JPG
JPEG
PNG
WebP
```

Try opening the image in another image viewer to ensure the source file is not corrupt.

---

# Large Photographs Feel Slow

High-resolution photographs may require significantly more memory after they are decompressed for editing.

You can try:

- using a smaller copy
- closing unnecessary applications
- reducing output dimensions
- avoiding unnecessarily large source images for web content

---

# Export Looks Different

Check:

```text
Preset
Smart Auto
Brightness
Contrast
Saturation
Temperature
Effect Strength
Export Format
Export Quality
```

For JPEG and WebP, try increasing the quality setting if compression is visibly affecting the result.

---

# Developer Guide

Clone the project:

```bash
git clone YOUR_REPOSITORY_URL
```

Enter the directory:

```bash
cd peabox-photo-lab
```

Create a virtual environment:

```bash
python -m venv .venv
```

---

## Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Linux/macOS

```bash
source .venv/bin/activate
```

---

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Start:

```bash
python -m streamlit run app.py
```

---

# Development Validation

Before committing:

```bash
python -m py_compile app.py
```

Manually test:

```text
JPG Upload
PNG Upload
WebP Upload

JPEG Export
PNG Export
WebP Export

Crop
Rotate
Mirror
Smart Auto
Presets
Creative Effects
Watermark
Borders
Palette Extraction
Proof Sheet
Social Format Pack
Image Inspector
```

---

# Main Technologies

## Python

Provides the primary application and image-processing logic.

## Streamlit

Provides the browser-based application interface.

## Pillow

Provides core image manipulation including enhancement, filtering, colour operations, drawing and image transformations.

PeaBox uses functionality from modules including:

```text
Image
ImageOps
ImageEnhance
ImageFilter
ImageDraw
ImageChops
ImageFont
```

## NumPy

Provides array and pixel-level calculations used for custom image effects.

---

# Contributing

Contributions are welcome.

Interesting contribution areas include:

```text
Creative effects
New presets
Image processing algorithms
Performance
Accessibility
User interface improvements
Automated testing
Documentation
Export formats
Batch processing
Creator utilities
Localization
```

Recommended workflow:

```text
Fork Repository
      ↓
Create Branch
      ↓
Make Changes
      ↓
Test
      ↓
Commit
      ↓
Submit Pull Request
```

Please read:

```text
CONTRIBUTING.md
```

before submitting significant changes.

---

# Bug Reports

Use the included GitHub:

```text
Bug Report
```

issue form.

Please provide:

```text
Operating system
Python version
Browser
Image format
Approximate dimensions
Steps to reproduce
Expected result
Actual result
Error message
```

Do not publicly upload:

```text
Private photographs
Passwords
API keys
Tokens
Credentials
Personal information
```

---

# Feature Requests

Use the:

```text
Feature Request
```

GitHub issue form.

A useful feature request should explain:

1. The user problem
2. The proposed feature
3. The expected user experience
4. Why the feature is valuable
5. Whether it requires external services

---

# Security

If you discover a vulnerability, do not publish sensitive vulnerability details through a regular public issue.

Read:

```text
SECURITY.md
```

and use the repository's configured private security-reporting mechanism where available.

---

# Roadmap

The following are possible future directions rather than commitments.

## Editing

- Interactive crop selection
- Straighten tool
- Resize by exact dimensions
- Exposure
- Curves
- Levels
- HSL adjustment
- Blur controls
- Histogram view

---

## Creator Tools

- Custom export profiles
- Saved brand presets
- Logo watermark upload
- Batch watermarking
- More social-media presets
- Thumbnail generator
- Collage generator
- Contact-sheet customization

---

## Advanced Image Features

Potential future experimentation could include:

- Background removal
- Object segmentation
- Subject-aware adjustments
- Noise reduction
- Image upscaling
- Portrait enhancement
- Local AI-assisted editing
- Intelligent auto-crop

---

## User Experience

Potential improvements include:

- Undo / redo
- Editing history
- User-created presets
- Drag-and-drop workflow
- Keyboard shortcuts
- Dark/light themes
- Localization
- Desktop packaging

---

# Design Philosophy

PeaBox Photo Lab follows five basic principles.

## 1. Simple

Users should not need professional photography knowledge to perform common tasks.

## 2. Useful

Features should solve practical image creation and publishing problems.

## 3. Local-first

Where practical, image processing should remain on the user's machine.

## 4. Creator-friendly

One photograph should easily become multiple publishing assets.

## 5. Open

Developers should be able to understand, modify and extend the application.

---

# GitHub Repository Metadata

## Repository Name

```text
peabox-photo-lab
```

## Display Name

```text
PeaBox Photo Lab
```

## Description

```text
A privacy-first, local photo editor built with Python, Streamlit and Pillow, featuring smart enhancements, creative effects and creator tools.
```

## Suggested Topics

```text
python
streamlit
pillow
photo-editor
image-processing
image-editor
photo-effects
creator-tools
privacy-first
webp
photo-enhancement
open-source
peabox
```

---

# Suggested Release

```text
PeaBox Photo Lab v2.0.0
```

Release title:

```text
PeaBox Photo Lab 2.0 - Creator Toolkit
```

---

# License

PeaBox Photo Lab is distributed under the **MIT License**.

See:

```text
LICENSE
```

for the complete license terms.

---

# PeaBox Labs

PeaBox Photo Lab is part of the **PeaBox** collection of practical creator, publishing, AI and productivity tools.

The PeaBox philosophy is simple:

> **Build useful tools. Keep them approachable. Let people make them their own.**

---

# ⭐ Support PeaBox Photo Lab

If you find PeaBox Photo Lab useful:

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🔧 Contribute improvements
- 🍴 Fork the project
- 📣 Share it with others

---

<div align="center">

# 📷 PeaBox Photo Lab

### Edit. Enhance. Create. Privately.

**Built with Python ❤️**

</div>
