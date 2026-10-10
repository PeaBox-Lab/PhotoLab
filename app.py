import io, json, colorsys
from pathlib import Path
import numpy as np
import streamlit as st
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ExifTags

st.set_page_config(page_title="PeaBox Photo Lab",page_icon="📷",layout="wide")
st.markdown("""<style>.block-container{padding-top:1rem;max-width:1550px}.hero{padding:18px 22px;border-radius:20px;background:linear-gradient(120deg,#4f46e5,#0891b2);color:#fff}.hero h1{margin:0}.muted{opacity:.75}</style><div class='hero'><h1>PeaBox Photo Lab 2</h1><p>A friendly, private, non-destructive photo studio powered by Python.</p></div>""",unsafe_allow_html=True)
R=Image.Resampling.LANCZOS

def rgb(im): return ImageOps.exif_transpose(im).convert("RGB")
def crop_ratio(im,r):
    if r=="Original": return im
    a,b=map(float,r.split(':')); t=a/b; c=im.width/im.height
    if c>t:
        w=int(im.height*t); x=(im.width-w)//2; return im.crop((x,0,x+w,im.height))
    h=int(im.width/t); y=(im.height-h)//2; return im.crop((0,y,im.width,y+h))
def temp(im,v):
    a=np.asarray(im).astype(float); k=v/100; a[...,0]*=1+.22*k; a[...,2]*=1-.22*k; a[...,1]*=1+.04*k
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
def tone(im,sh,hi):
    a=np.asarray(im).astype(float)/255; l=a.mean(2,keepdims=True)
    a+=np.clip((.62-l)/.62,0,1)**1.5*(sh/100)*.35
    a+=np.clip((l-.42)/.58,0,1)**1.5*(hi/100)*.28
    return Image.fromarray(np.uint8(np.clip(a*255,0,255)))
def auto(im):
    x=ImageOps.autocontrast(im,cutoff=1,preserve_tone=True); m=np.asarray(x).mean(); x=ImageEnhance.Brightness(x).enhance(float(np.clip(132/max(m,1),.85,1.22)))
    return x.filter(ImageFilter.UnsharpMask(1.3,110,3))
def selective(im,hue,width):
    h=np.asarray(im.convert('HSV'))[...,0].astype(int); t=int(hue/360*255); d=np.minimum(abs(h-t),256-abs(h-t)); m=np.clip(1-d/max(1,int(width/360*255)),0,1)[...,None]
    a=np.asarray(im).astype(float); g=np.asarray(ImageOps.grayscale(im))[...,None]; return Image.fromarray(np.uint8(np.clip(g*(1-m)+a*m,0,255)))
def vignette(im,v):
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; y,x=np.ogrid[-1:1:h*1j,-1:1:w*1j]; q=1-v/100*np.clip((np.sqrt(x*x+y*y)-.2)/1.1,0,1)**1.7
    return Image.fromarray(np.uint8(np.clip(a*q[...,None],0,255)))
def sketch(im):
    g=np.asarray(ImageOps.grayscale(im)).astype(float); b=np.asarray(ImageOps.invert(Image.fromarray(np.uint8(g))).filter(ImageFilter.GaussianBlur(12))).astype(float)
    return Image.fromarray(np.uint8(np.clip(g*255/(256-b),0,255))).convert('RGB')
def pixel(im,n): return im.resize((max(1,im.width//n),max(1,im.height//n)),Image.Resampling.BILINEAR).resize(im.size,Image.Resampling.NEAREST)
def preset(im,n):
    if n=='Clean Pop': return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.12)).enhance(1.12)
    if n=='Warm Film': return ImageEnhance.Color(temp(im,30)).enhance(.9)
    if n=='Cool Editorial': return ImageEnhance.Contrast(temp(im,-25)).enhance(1.1)
    if n=='Mono Punch': return ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.35).convert('RGB')
    if n=='Vintage Fade': return ImageEnhance.Color(ImageEnhance.Contrast(temp(im,15)).enhance(.82)).enhance(.78)
    return im
def watermark(im,text,pos,opacity):
    if not text.strip(): return im
    lay=Image.new('RGBA',im.size); d=ImageDraw.Draw(lay); fs=max(15,im.width//38)
    try:f=ImageFont.truetype('DejaVuSans.ttf',fs)
    except:f=ImageFont.load_default()
    box=d.textbbox((0,0),text,font=f); w,h=box[2],box[3]; p=max(10,fs//2)
    xy={'Bottom right':(im.width-w-p,im.height-h-p),'Bottom left':(p,im.height-h-p),'Top right':(im.width-w-p,p),'Top left':(p,p),'Center':((im.width-w)//2,(im.height-h)//2)}[pos]
    d.rounded_rectangle((xy[0]-p//2,xy[1]-p//3,xy[0]+w+p//2,xy[1]+h+p//3),p//2,fill=(0,0,0,int(opacity*.45))); d.text(xy,text,font=f,fill=(255,255,255,opacity))
    return Image.alpha_composite(im.convert('RGBA'),lay).convert('RGB')
def palette(im,n=6):
    q=im.copy(); q.thumbnail((250,250)); q=q.quantize(colors=n,method=Image.Quantize.MEDIANCUT).convert('RGB'); colors=q.getcolors(q.width*q.height) or []
    return ['#%02x%02x%02x'%c for _,c in sorted(colors,reverse=True)[:n]]
def contact_sheet(images,names,cols=3):
    thumbs=[]
    for im,name in zip(images,names):
        x=im.copy(); x.thumbnail((500,350)); thumbs.append((x,name))
    cellw=max(x.width for x,_ in thumbs)+30; cellh=max(x.height for x,_ in thumbs)+65; rows=(len(thumbs)+cols-1)//cols
    out=Image.new('RGB',(cellw*cols,cellh*rows),'white'); d=ImageDraw.Draw(out)
    for i,(x,n) in enumerate(thumbs):
        px=i%cols*cellw+(cellw-x.width)//2; py=i//cols*cellh+15; out.paste(x,(px,py)); d.text((i%cols*cellw+15,py+x.height+10),n,fill='black')
    return out

if 'compare' not in st.session_state: st.session_state.compare=True
with st.sidebar:
    st.header('1. Choose a photo'); up=st.file_uploader('JPG, PNG or WebP',type=['jpg','jpeg','png','webp'])
    if not up: st.caption('Tip: use a high-resolution original for the best export.')
    st.header('2. Edit')
    pre=st.selectbox('Quick style',['None','Clean Pop','Warm Film','Cool Editorial','Mono Punch','Vintage Fade'])
    smart=st.toggle('Smart Auto Optimize'); aspect=st.selectbox('Crop for a platform',['Original','1:1','4:5','3:2','16:9','9:16'])
    rot=st.select_slider('Rotate',options=[0,90,180,270]); fh=st.toggle('Mirror'); fv=st.toggle('Flip vertically')
    with st.expander('Light and colour',True):
        br=st.slider('Brightness',-100,100,0); co=st.slider('Contrast',-100,100,0); sa=st.slider('Saturation',-100,100,0); sharp=st.slider('Sharpness',-100,100,0); te=st.slider('Temperature',-100,100,0); sh=st.slider('Shadows',-100,100,0); hi=st.slider('Highlights',-100,100,0)
    with st.expander('Creative add-ons'):
        eff=st.selectbox('Effect',['None','Selective Colour Pop','Duotone','Dreamy Glow','Pencil Sketch','Pixel Art','Focus Vignette']); intensity=st.slider('Effect strength',0,100,45); hue=st.slider('Colour-pop hue',0,359,25); hr=st.slider('Hue range',5,90,30); dd=st.color_picker('Duotone shadows','#172554'); dl=st.color_picker('Duotone highlights','#fbbf24'); block=st.slider('Pixel size',3,40,12)
    with st.expander('Brand kit and finishing'):
        border=st.slider('Border width %',0.,8.,0.,.25); bc=st.color_picker('Border colour','#ffffff'); wm=st.text_input('Watermark'); wp=st.selectbox('Watermark position',['Bottom right','Bottom left','Top right','Top left','Center']); wo=st.slider('Watermark opacity',20,255,150)

if not up:
    st.info('Upload a photo to begin. All edits are non-destructive and regenerate from the original.')
    c1,c2,c3,c4=st.columns(4)
    c1.markdown("**Quick workflow**\n\nUpload, pick a preset, refine, and export.")
    c2.markdown("**Creator tools**\n\nSocial crops, watermarking, palette extraction, and contact sheets.")
    c3.markdown("**Creative Lab**\n\nColour pop, duotone, sketch, pixel art, glow, and vignette.")
    c4.markdown("**Privacy**\n\nLocal processing and fresh exports without copied EXIF metadata.")
    st.stop()
try: original=Image.open(up); original.load(); original=rgb(original)
except Exception as e: st.error(f'Could not open this image: {e}'); st.stop()

im=crop_ratio(original,aspect)
if rot: im=im.rotate(-rot,expand=True,resample=Image.Resampling.BICUBIC)
if fh: im=ImageOps.mirror(im)
if fv: im=ImageOps.flip(im)
im=preset(im,pre)
if smart: im=auto(im)
im=ImageEnhance.Brightness(im).enhance(max(.05,1+br/100)); im=ImageEnhance.Contrast(im).enhance(max(0,1+co/100)); im=ImageEnhance.Color(im).enhance(max(0,1+sa/100)); im=ImageEnhance.Sharpness(im).enhance(max(0,1+sharp/50)); im=temp(im,te); im=tone(im,sh,hi)
if eff=='Selective Colour Pop': im=selective(im,hue,hr)
elif eff=='Duotone': im=Image.blend(im,ImageOps.colorize(ImageOps.grayscale(im),dd,dl),intensity/100)
elif eff=='Dreamy Glow': im=Image.blend(im,ImageChops.screen(im,im.filter(ImageFilter.GaussianBlur(max(2,min(im.size)//120)))),intensity/100)
elif eff=='Pencil Sketch': im=Image.blend(im,sketch(im),intensity/100)
elif eff=='Pixel Art': im=Image.blend(im,pixel(im,block),intensity/100)
elif eff=='Focus Vignette': im=vignette(im,intensity)
if border: im=ImageOps.expand(im,border=int(min(im.size)*border/100),fill=bc)
im=watermark(im,wm,wp,wo)

edit_tab, creator_tab, info_tab=st.tabs(['Editor','Creator Toolkit','Image Inspector'])
with edit_tab:
    show=st.toggle('Before and after view',True)
    if show:
        a,b=st.columns(2); a.subheader('Before'); a.image(original,use_container_width=True); b.subheader('After'); b.image(im,use_container_width=True)
    else: st.image(im,use_container_width=True)
    st.caption(f'Original {original.width}×{original.height} | Edited {im.width}×{im.height}')
with creator_tab:
    st.subheader('Colour palette extractor')
    cols=palette(im); blocks=st.columns(len(cols))
    for c,hx in zip(blocks,cols): c.color_picker(hx,hx,disabled=True)
    st.code(json.dumps({'palette':cols},indent=2),language='json')
    st.subheader('Preset proof sheet')
    names=['Original','Clean Pop','Warm Film','Cool Editorial','Mono Punch','Vintage Fade']; proof=contact_sheet([original]+[preset(original,n) for n in names[1:]],names)
    st.image(proof,use_container_width=True)
    pb=io.BytesIO(); proof.save(pb,'JPEG',quality=90); st.download_button('Download style proof sheet',pb.getvalue(),'peabox-style-proof.jpg','image/jpeg')
    st.subheader('Social format pack')
    pack=[]
    for label,ratio in [('Square 1x1','1:1'),('Portrait 4x5','4:5'),('Landscape 16x9','16:9'),('Story 9x16','9:16')]:
        x=crop_ratio(im,ratio); x.thumbnail((1800,1800)); z=io.BytesIO(); x.save(z,'JPEG',quality=92,optimize=True); pack.append((label,z.getvalue()))
    zbuf=io.BytesIO()
    import zipfile
    with zipfile.ZipFile(zbuf,'w',zipfile.ZIP_DEFLATED) as z:
        for label,data in pack: z.writestr(label.lower().replace(' ','-')+'.jpg',data)
    st.download_button('Download social format pack (ZIP)',zbuf.getvalue(),'peabox-social-pack.zip','application/zip')
with info_tab:
    st.subheader('Image health check')
    mp=original.width*original.height/1_000_000; ratio=original.width/original.height
    c1,c2,c3,c4=st.columns(4); c1.metric('Width',original.width); c2.metric('Height',original.height); c3.metric('Megapixels',f'{mp:.1f}'); c4.metric('Aspect',f'{ratio:.2f}:1')
    if min(original.size)<1080: st.warning('This image may look soft in large exports because its shortest side is below 1080 pixels.')
    else: st.success('Resolution is suitable for common web and social exports.')
    st.markdown('**Privacy note:** exported files are newly encoded and do not copy the uploaded file’s EXIF metadata.')

st.divider(); st.subheader('3. Export')
a,b,c,d=st.columns([1,1,1,2]); fmt=a.selectbox('Format',['JPEG','PNG','WEBP']); quality=b.slider('Quality',60,100,92); maxside=c.selectbox('Long edge',['Original',4096,2560,2048,1600,1080]); name=d.text_input('Filename','peabox-edit')
out=im.copy()
if maxside!='Original' and max(out.size)>int(maxside):
    s=int(maxside)/max(out.size); out=out.resize((int(out.width*s),int(out.height*s)),R)
buf=io.BytesIO(); kw={'format':fmt}
if fmt=='JPEG': kw|={'quality':quality,'optimize':True,'progressive':True}
elif fmt=='WEBP': kw|={'quality':quality,'method':6}
else: kw|={'optimize':True}
out.save(buf,**kw); ext={'JPEG':'jpg','PNG':'png','WEBP':'webp'}[fmt]; mime={'JPEG':'image/jpeg','PNG':'image/png','WEBP':'image/webp'}[fmt]
st.download_button('Download edited photo',buf.getvalue(),f'{Path(name).stem}.{ext}',mime,type='primary',use_container_width=True)
st.caption('Keyboard accessibility depends on your browser. Every control has a visible label, and the original is never overwritten.')
