import io
import math
from pathlib import Path

import numpy as np
import streamlit as st
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

st.set_page_config(page_title="PeaBox Photo Lab", page_icon="📷", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; max-width: 1500px;}
[data-testid="stSidebar"] {border-right: 1px solid rgba(128,128,128,.22);}
.hero {padding: 1rem 1.2rem; border-radius: 18px; background: linear-gradient(120deg,#6d28d9,#0ea5e9); color:white; margin-bottom:1rem;}
.hero h1 {margin:0; font-size:2rem}.hero p {margin:.3rem 0 0; opacity:.92}
.small {font-size:.82rem; opacity:.75}
</style>
<div class="hero"><h1>PeaBox Photo Lab</h1><p>Private, local-first photo editing with creative Python-powered effects.</p></div>
""", unsafe_allow_html=True)

RESAMPLE = Image.Resampling.LANCZOS

def clamp(v, lo=0, hi=255):
    return max(lo, min(hi, int(v)))

def ensure_rgb(im):
    if im.mode in ("RGBA", "RGB"):
        return im.copy()
    return im.convert("RGB")

def auto_optimize(im):
    rgb = im.convert("RGB")
    rgb = ImageOps.autocontrast(rgb, cutoff=1, preserve_tone=True)
    arr = np.asarray(rgb).astype(np.float32)
    gray = arr.mean(axis=2)
    mean = float(gray.mean())
    brightness = np.clip(130.0 / max(mean, 1), 0.82, 1.25)
    rgb = ImageEnhance.Brightness(rgb).enhance(float(brightness))
    rgb = ImageEnhance.Color(rgb).enhance(1.06)
    rgb = rgb.filter(ImageFilter.UnsharpMask(radius=1.4, percent=115, threshold=3))
    return rgb

def temperature(im, amount):
    arr = np.asarray(im.convert("RGB")).astype(np.float32)
    k = amount / 100.0
    arr[..., 0] *= (1 + 0.22*k)
    arr[..., 2] *= (1 - 0.22*k)
    arr[..., 1] *= (1 + 0.04*k)
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8), "RGB")

def tint(im, amount):
    arr=np.asarray(im.convert("RGB")).astype(np.float32)
    k=amount/100.0
    arr[...,1] *= (1 - 0.16*k)
    arr[...,0] *= (1 + 0.08*k)
    arr[...,2] *= (1 + 0.08*k)
    return Image.fromarray(np.clip(arr,0,255).astype(np.uint8), "RGB")

def shadows_highlights(im, shadows, highlights):
    arr=np.asarray(im.convert("RGB")).astype(np.float32)/255.0
    lum=arr.mean(axis=2, keepdims=True)
    if shadows:
        mask=np.clip((0.60-lum)/0.60,0,1)**1.5
        arr += mask*(shadows/100.0)*0.38
    if highlights:
        mask=np.clip((lum-0.42)/0.58,0,1)**1.5
        arr += mask*(highlights/100.0)*0.32
    return Image.fromarray(np.clip(arr*255,0,255).astype(np.uint8), "RGB")

def crop_to_aspect(im, ratio):
    if ratio == "Original": return im
    rw,rh=map(float, ratio.split(":"))
    target=rw/rh; current=im.width/im.height
    if current>target:
        nw=int(im.height*target); left=(im.width-nw)//2
        return im.crop((left,0,left+nw,im.height))
    nh=int(im.width/target); top=(im.height-nh)//2
    return im.crop((0,top,im.width,top+nh))

def duotone(im, dark, light):
    return ImageOps.colorize(ImageOps.grayscale(im), black=dark, white=light)

def selective_color(im, hue_deg, width):
    hsv=np.asarray(im.convert("HSV")); hue=hsv[...,0].astype(np.int16)
    target=int((hue_deg%360)/360*255); dist=np.minimum(abs(hue-target),256-abs(hue-target))
    mask=np.clip(1-dist/max(1,int(width/360*255)),0,1)[...,None]
    rgb=np.asarray(im.convert("RGB")).astype(np.float32)
    gray=np.asarray(ImageOps.grayscale(im))[...,None].astype(np.float32)
    out=gray*(1-mask)+rgb*mask
    return Image.fromarray(np.clip(out,0,255).astype(np.uint8),"RGB")

def pixel_art(im, block):
    w=max(1,im.width//block); h=max(1,im.height//block)
    return im.resize((w,h),Image.Resampling.BILINEAR).resize(im.size,Image.Resampling.NEAREST)

def dreamy_glow(im, strength):
    blur=im.filter(ImageFilter.GaussianBlur(radius=max(2, min(im.size)/120)))
    screen=ImageChops.screen(im, blur)
    return Image.blend(im, screen, strength/100.0)

def focus_vignette(im, strength):
    arr=np.asarray(im.convert("RGB")).astype(np.float32)
    h,w=arr.shape[:2]; y,x=np.ogrid[-1:1:h*1j,-1:1:w*1j]
    r=np.sqrt(x*x+y*y); shade=1-(strength/100.0)*np.clip((r-.25)/1.05,0,1)**1.7
    return Image.fromarray(np.clip(arr*shade[...,None],0,255).astype(np.uint8),"RGB")

def edge_sketch(im):
    gray=ImageOps.grayscale(im)
    inv=ImageOps.invert(gray).filter(ImageFilter.GaussianBlur(12))
    a=np.asarray(gray).astype(np.float32); b=np.asarray(inv).astype(np.float32)
    dodge=np.clip(a*255/(255-b+1),0,255).astype(np.uint8)
    return Image.fromarray(dodge,"L").convert("RGB")

def add_border(im, width_pct, color):
    px=int(min(im.size)*width_pct/100)
    return ImageOps.expand(im,border=px,fill=color) if px else im

def add_watermark(im, text, opacity, position):
    if not text.strip(): return im
    layer=Image.new("RGBA", im.size,(0,0,0,0)); draw=ImageDraw.Draw(layer)
    size=max(14,im.width//35)
    try: font=ImageFont.truetype("DejaVuSans.ttf",size)
    except OSError: font=ImageFont.load_default()
    box=draw.textbbox((0,0),text,font=font,stroke_width=1); tw,th=box[2]-box[0],box[3]-box[1]; pad=max(8,size//2)
    spots={"Bottom right":(im.width-tw-pad,im.height-th-pad),"Bottom left":(pad,im.height-th-pad),"Top right":(im.width-tw-pad,pad),"Top left":(pad,pad),"Center":((im.width-tw)//2,(im.height-th)//2)}
    xy=spots[position]
    draw.rounded_rectangle((xy[0]-pad//2,xy[1]-pad//3,xy[0]+tw+pad//2,xy[1]+th+pad//3),radius=pad//2,fill=(0,0,0,clamp(opacity*.55)))
    draw.text(xy,text,font=font,fill=(255,255,255,clamp(opacity)),stroke_width=1,stroke_fill=(0,0,0,clamp(opacity)))
    return Image.alpha_composite(im.convert("RGBA"),layer).convert("RGB")

def preset(im,name):
    if name=="Clean Pop":
        return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.12)).enhance(1.12)
    if name=="Warm Film":
        x=temperature(im,32); x=ImageEnhance.Contrast(x).enhance(.93); return ImageEnhance.Color(x).enhance(.88)
    if name=="Cool Editorial":
        return ImageEnhance.Contrast(temperature(im,-24)).enhance(1.08)
    if name=="Mono Punch":
        return ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.35).convert("RGB")
    if name=="Fade":
        x=ImageEnhance.Contrast(im).enhance(.82); return ImageEnhance.Color(x).enhance(.8)
    return im

with st.sidebar:
    st.header("Edit controls")
    uploaded=st.file_uploader("Upload JPG, PNG or WebP",type=["jpg","jpeg","png","webp"])
    if uploaded:
        st.caption(f"{uploaded.name} · {uploaded.size/1024/1024:.1f} MB")
        preset_name=st.selectbox("Preset",["None","Clean Pop","Warm Film","Cool Editorial","Mono Punch","Fade"])
        auto=st.toggle("Smart Auto Optimize",False,help="Balances contrast, exposure, colour and clarity.")
        with st.expander("Transform",expanded=True):
            aspect=st.selectbox("Center crop",["Original","1:1","4:5","3:2","16:9","9:16"])
            rotate=st.select_slider("Rotate",options=[0,90,180,270],value=0)
            flip_h=st.toggle("Flip horizontal",False); flip_v=st.toggle("Flip vertical",False)
        with st.expander("Light and colour",expanded=True):
            brightness=st.slider("Brightness",-100,100,0); contrast=st.slider("Contrast",-100,100,0)
            saturation=st.slider("Saturation",-100,100,0); sharpness=st.slider("Sharpness",-100,100,0)
            temp=st.slider("Temperature",-100,100,0); tint_v=st.slider("Tint",-100,100,0)
            shadows=st.slider("Shadows",-100,100,0); highlights=st.slider("Highlights",-100,100,0)
        with st.expander("Creative Lab",expanded=False):
            effect=st.selectbox("Effect",["None","Selective Colour Pop","Duotone","Dreamy Glow","Pencil Sketch","Pixel Art","Focus Vignette"])
            hue=st.slider("Colour-pop hue",0,359,25); hue_width=st.slider("Hue range",5,90,30)
            duo_dark=st.color_picker("Duotone shadows","#172554"); duo_light=st.color_picker("Duotone highlights","#fbbf24")
            intensity=st.slider("Effect intensity",0,100,45); block=st.slider("Pixel block size",3,40,12)
        with st.expander("Finish",expanded=False):
            border=st.slider("Border width (%)",0.0,8.0,0.0,.25); border_color=st.color_picker("Border colour","#ffffff")
            watermark=st.text_input("Watermark text",""); wm_pos=st.selectbox("Watermark position",["Bottom right","Bottom left","Top right","Top left","Center"]); wm_op=st.slider("Watermark opacity",20,255,150)
            max_side=st.selectbox("Maximum long edge",["Original",4096,2560,2048,1600,1080])

if not uploaded:
    st.info("Upload a photo from the sidebar to begin. Your image is processed in memory and is not written to disk by the app.")
    st.subheader("What makes it interesting")
    a,b,c=st.columns(3)
    a.markdown("**Smart Auto Optimize**\n\nOne-click tonal correction calibrated from the image histogram.")
    b.markdown("**Creative Lab**\n\nSelective colour, duotone, sketch, pixel art, glow and focus vignette.")
    c.markdown("**Privacy-first export**\n\nExports freshly encoded pixels, removing original EXIF metadata by default.")
    st.stop()

try:
    original=Image.open(uploaded); original.load(); original=ImageOps.exif_transpose(original)
except Exception as exc:
    st.error(f"Could not read this image: {exc}"); st.stop()

im=ensure_rgb(original)
im=crop_to_aspect(im,aspect)
if rotate: im=im.rotate(-rotate,expand=True,resample=Image.Resampling.BICUBIC)
if flip_h: im=ImageOps.mirror(im)
if flip_v: im=ImageOps.flip(im)
im=preset(im,preset_name)
if auto: im=auto_optimize(im)
im=ImageEnhance.Brightness(im).enhance(max(.05,1+brightness/100))
im=ImageEnhance.Contrast(im).enhance(max(0,1+contrast/100))
im=ImageEnhance.Color(im).enhance(max(0,1+saturation/100))
im=ImageEnhance.Sharpness(im).enhance(max(0,1+sharpness/50))
im=temperature(im,temp); im=tint(im,tint_v); im=shadows_highlights(im,shadows,highlights)
if effect=="Selective Colour Pop": im=selective_color(im,hue,hue_width)
elif effect=="Duotone": im=Image.blend(im,duotone(im,duo_dark,duo_light),intensity/100)
elif effect=="Dreamy Glow": im=dreamy_glow(im,intensity)
elif effect=="Pencil Sketch": im=Image.blend(im,edge_sketch(im),intensity/100)
elif effect=="Pixel Art": im=Image.blend(im,pixel_art(im,block),intensity/100)
elif effect=="Focus Vignette": im=focus_vignette(im,intensity)
if max_side!="Original" and max(im.size)>int(max_side):
    scale=int(max_side)/max(im.size); im=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),RESAMPLE)
im=add_border(im,border,border_color); im=add_watermark(im,watermark,wm_op,wm_pos)

left,right=st.columns(2)
with left:
    st.subheader("Original"); st.image(original,use_container_width=True); st.caption(f"{original.width} × {original.height} · {original.mode}")
with right:
    st.subheader("Edited"); st.image(im,use_container_width=True); st.caption(f"{im.width} × {im.height} · metadata stripped on export")

st.divider(); st.subheader("Export")
c1,c2,c3,c4=st.columns([1,1,1,2])
fmt=c1.selectbox("Format",["JPEG","PNG","WEBP"]); quality=c2.slider("Quality",60,100,92); filename=c3.text_input("Filename","peabox_edit")
export=io.BytesIO(); save_im=im.convert("RGB") if fmt in ("JPEG","WEBP") else im
kwargs={"format":fmt}
if fmt=="JPEG": kwargs.update(quality=quality,optimize=True,progressive=True)
elif fmt=="WEBP": kwargs.update(quality=quality,method=6)
elif fmt=="PNG": kwargs.update(optimize=True)
save_im.save(export,**kwargs)
ext={"JPEG":"jpg","PNG":"png","WEBP":"webp"}[fmt]; mime={"JPEG":"image/jpeg","PNG":"image/png","WEBP":"image/webp"}[fmt]
c4.download_button("Download edited photo",export.getvalue(),file_name=f"{Path(filename).stem}.{ext}",mime=mime,type="primary",use_container_width=True)
st.caption("Tip: all edits are non-destructive. Change any control to regenerate from the original upload.")
