import io, json, colorsys
from pathlib import Path
import numpy as np
import streamlit as st
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps, ExifTags

st.set_page_config(page_title="PeaBox Photo Lab",page_icon="📷",layout="wide")
st.markdown("""<style>.block-container{padding-top:1rem;max-width:1550px}.hero{padding:18px 22px;border-radius:20px;background:linear-gradient(120deg,#4f46e5,#0891b2);color:#fff}.hero h1{margin:0}.muted{opacity:.75}</style><div class='hero'><h1>PeaBox Photo Lab v0.2.27</h1><p>A friendly, private, non-destructive photo studio powered by Python.</p></div>""",unsafe_allow_html=True)
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
def resize_exact(im,w,h,keep=True):
    if keep:
        cp=im.copy(); cp.thumbnail((w,h),Image.Resampling.LANCZOS); return cp
    return im.resize((w,h),Image.Resampling.LANCZOS)

def grayscale(im): return ImageOps.grayscale(im).convert("RGB")
def sepia(im,strength=70):
    g=np.asarray(ImageOps.grayscale(im)).astype(float)
    a=np.stack([g*1.07+12,g*.94+4,g*.76],axis=2)
    toned=Image.fromarray(np.uint8(np.clip(a,0,255)))
    return Image.blend(im,toned,strength/100)
def posterize(im,bits): return ImageOps.posterize(im,max(1,min(8,int(bits))))
def solarize(im,threshold): return ImageOps.solarize(im,int(threshold))
def channel_balance(im,r,g,b):
    a=np.asarray(im).astype(float); a[...,0]*=r/100; a[...,1]*=g/100; a[...,2]*=b/100
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
def split_tone(im,shadow_hue,highlight_hue,strength):
    if strength<=0: return im
    a=np.asarray(im).astype(float); lum=a.mean(2)/255.0
    sh=np.array(tuple(int(c*255) for c in colorsys.hsv_to_rgb(shadow_hue/360,0.55,1.0)))
    hi=np.array(tuple(int(c*255) for c in colorsys.hsv_to_rgb(highlight_hue/360,0.45,1.0)))
    sw=np.clip((0.55-lum)/0.55,0,1)[...,None]; hw=np.clip((lum-0.45)/0.55,0,1)[...,None]
    k=strength/100*0.35; out=a*(1-k*(sw+hw))+sh*sw*k+hi*hw*k
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def matte(im,amount):
    if amount<=0: return im
    a=np.asarray(im).astype(float)/255.0; floor=amount/100*0.12; a=floor+(1-floor)*a
    return Image.fromarray(np.uint8(np.clip(a*255,0,255)))
def film_grain(im,amount):
    if amount<=0: return im
    a=np.asarray(im).astype(np.int16); rng=np.random.default_rng(27); noise=rng.normal(0,amount/100*18,a.shape[:2])[...,None]
    return Image.fromarray(np.uint8(np.clip(a+noise,0,255)))
def lens_vignette(im,amount,softness=60):
    if amount<=0: return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]
    y,x=np.ogrid[-1:1:complex(h),-1:1:complex(w)]; r=np.sqrt(x*x+y*y)
    edge=np.clip((r-(softness/100)*0.7)/max(0.05,1-(softness/100)*0.7),0,1)[...,None]
    a*=1-edge*(amount/100)*0.75
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
def add_date_stamp(im,text,position='Bottom right'):
    if not text: return im
    out=im.copy(); d=ImageDraw.Draw(out); size=max(14,int(min(out.size)*0.035))
    try: font=ImageFont.truetype('DejaVuSans.ttf',size)
    except: font=ImageFont.load_default()
    box=d.textbbox((0,0),text,font=font); tw,th=box[2]-box[0],box[3]-box[1]; pad=max(8,size//3)
    coords={'Bottom right':(out.width-tw-pad,out.height-th-pad),'Bottom left':(pad,out.height-th-pad),'Top right':(out.width-tw-pad,pad),'Top left':(pad,pad)}
    x,y=coords[position]; d.rounded_rectangle((x-pad//2,y-pad//2,x+tw+pad//2,y+th+pad//2),radius=pad//2,fill=(0,0,0,150)); d.text((x,y),text,font=font,fill='white')
    return out
def soft_focus(im,amount):
    if amount<=0: return im
    blurred=im.filter(ImageFilter.GaussianBlur(max(.2,amount/18)))
    return Image.blend(im,blurred,min(.7,amount/140))
def edge_enhance(im,amount):
    if amount<=0: return im
    return Image.blend(im,im.filter(ImageFilter.DETAIL),min(1,amount/100))
def pixel_dimensions(im): return f"{im.width} x {im.height}", im.width*im.height/1_000_000
def sharpen_edges(im,amount):
    if amount<=0: return im
    edges=im.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return Image.blend(im,edges,min(.65,amount/150))
def color_boost(im,vibrance):
    if vibrance<=0: return im
    a=np.asarray(im).astype(float); mx=a.max(2); mn=a.min(2); sat=(mx-mn)/(mx+1e-6)
    boost=(1-sat)[...,None]*(vibrance/100)*0.5
    gray=a.mean(2,keepdims=True); out=a+(a-gray)*boost
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def exposure_ev(im,ev):
    if abs(ev)<1e-9: return im
    return ImageEnhance.Brightness(im).enhance(2**ev)
def gamma_adjust(im,gamma):
    if abs(gamma-1.0)<1e-9: return im
    inv=1.0/max(.1,gamma); lut=[int(((i/255.0)**inv)*255) for i in range(256)]
    return im.point(lut*3)
def tint_shift(im,value):
    if value==0: return im
    a=np.asarray(im).astype(float); k=value/100.0
    a[...,1]*=1-.16*max(k,0)+.10*max(-k,0); a[...,0]*=1+.10*max(k,0); a[...,2]*=1+.08*max(k,0)
    return Image.fromarray(np.uint8(np.clip(a,0,255)))
def auto_levels(im,cutoff=1):
    return ImageOps.autocontrast(im,cutoff=max(0,min(10,int(cutoff))))
def white_balance_gray_world(im,strength):
    if strength<=0: return im
    a=np.asarray(im).astype(float); means=a.reshape(-1,3).mean(0); target=means.mean(); gains=target/np.maximum(means,1e-6)
    corrected=a*gains; k=strength/100.0; out=a*(1-k)+corrected*k
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def fade_highlights(im,amount):
    if amount<=0: return im
    a=np.asarray(im).astype(float); lum=a.mean(2,keepdims=True)/255.0; mask=np.clip((lum-.55)/.45,0,1)
    gray=np.full_like(a,235.0); k=amount/100*.25; out=a*(1-mask*k)+gray*(mask*k)
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def micro_contrast(im,amount):
    if amount<=0:return im
    blur=np.asarray(im.filter(ImageFilter.GaussianBlur(4))).astype(float); a=np.asarray(im).astype(float); k=amount/100*.7
    return Image.fromarray(np.uint8(np.clip(a+(a-blur)*k,0,255)))
def dehaze(im,amount):
    if amount<=0: return im
    a=np.asarray(im).astype(float); dark=a.min(2,keepdims=True); haze=np.percentile(dark,85); k=amount/100*.45
    out=(a-haze*k)/max(.35,1-k)
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def bloom(im,amount):
    if amount<=0: return im
    bright=ImageEnhance.Brightness(im).enhance(1.12).filter(ImageFilter.GaussianBlur(max(2,amount/16)))
    return Image.blend(im,bright,min(.35,amount/300))
def color_cast_score(im):
    a=np.asarray(im).astype(float).reshape(-1,3).mean(0); spread=float(a.max()-a.min())
    return a,spread
def clarity_mask(im,amount):
    if amount<=0: return im
    base=np.asarray(im).astype(float); blur=np.asarray(im.filter(ImageFilter.GaussianBlur(8))).astype(float)
    k=amount/100*.5; return Image.fromarray(np.uint8(np.clip(base+(base-blur)*k,0,255)))
def shadow_color(im,hue,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); lum=a.mean(2)/255; mask=np.clip((.55-lum)/.55,0,1)[...,None]
    color=np.array(colorsys.hsv_to_rgb(hue/360,.35,1.0))*255; k=strength/100*.22
    return Image.fromarray(np.uint8(np.clip(a*(1-mask*k)+color*mask*k,0,255)))
def highlight_color(im,hue,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); lum=a.mean(2)/255; mask=np.clip((lum-.45)/.55,0,1)[...,None]
    color=np.array(colorsys.hsv_to_rgb(hue/360,.28,1.0))*255; k=strength/100*.18
    return Image.fromarray(np.uint8(np.clip(a*(1-mask*k)+color*mask*k,0,255)))
def chromatic_pop(im,amount):
    if amount<=0:return im
    a=np.asarray(im).astype(float); mx=a.max(2,keepdims=True); mn=a.min(2,keepdims=True); chroma=mx-mn
    mask=np.clip(chroma/90,0,1); mean=a.mean(2,keepdims=True); k=amount/100*.45
    return Image.fromarray(np.uint8(np.clip(a+(a-mean)*mask*k,0,255)))
def soft_skin(im,amount):
    if amount<=0:return im
    smooth=im.filter(ImageFilter.GaussianBlur(max(.5,amount/25))); return Image.blend(im,smooth,min(.45,amount/220))
def crop_safe_area(im,percent):
    p=max(0,min(20,percent))/100; x=int(im.width*p); y=int(im.height*p); return (x,y,im.width-x,im.height-y)
def luminance_mask_preview(im,mode,opacity=55):
    a=np.asarray(im).astype(float); lum=.2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]
    if mode=='Highlights': mask=np.clip((lum-150)/105,0,1)
    elif mode=='Shadows': mask=np.clip((105-lum)/105,0,1)
    else: mask=1-np.clip(np.abs(lum-128)/128,0,1)
    overlay=np.zeros_like(a); overlay[...,0]=255; overlay[...,1]=80
    k=(mask*(opacity/100)*.65)[...,None]
    return Image.fromarray(np.uint8(np.clip(a*(1-k)+overlay*k,0,255)))
def monochrome_mix(im,r,g,b):
    a=np.asarray(im).astype(float); total=max(1,r+g+b); gray=(a[...,0]*r+a[...,1]*g+a[...,2]*b)/total
    return Image.fromarray(np.uint8(np.clip(gray,0,255))).convert('RGB')
def rgb_curve(im,black,white):
    if black==0 and white==255:return im
    lo=min(black,white-1); hi=max(white,lo+1); a=np.asarray(im).astype(float)
    return Image.fromarray(np.uint8(np.clip((a-lo)*255/(hi-lo),0,255)))
def color_temperature_auto(im,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); means=a.reshape(-1,3).mean(0); rb=means[0]-means[2]; shift=np.clip(rb/80,-1,1)*strength/100
    out=a.copy(); out[...,0]*=1-.12*shift; out[...,2]*=1+.12*shift
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def focus_score(im):
    g=np.asarray(ImageOps.grayscale(im)).astype(float); gx=np.diff(g,axis=1); gy=np.diff(g,axis=0)
    return float((gx.var()+gy.var())/2)
def defringe(im,amount):
    if amount<=0:return im
    a=np.asarray(im).astype(float); mean=a.mean(2,keepdims=True); chroma=a-mean; mx=a.max(2)-a.min(2); mask=(mx>70)[...,None]
    k=amount/100*.45; out=np.where(mask,a-chroma*k,a)
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def orton(im,amount):
    if amount<=0:return im
    glow=ImageEnhance.Brightness(im).enhance(1.08).filter(ImageFilter.GaussianBlur(max(1.5,amount/18)))
    return Image.blend(im,glow,min(.38,amount/260))
def dynamic_range(im):
    g=np.asarray(ImageOps.grayscale(im)).astype(float); p1,p99=np.percentile(g,[1,99]); return float(p1),float(p99),float(p99-p1)
def haze_glow_balance(im,amount):
    if amount==0:return im
    a=np.asarray(im).astype(float); blur=np.asarray(im.filter(ImageFilter.GaussianBlur(12))).astype(float); k=abs(amount)/100*.35
    out=a+(a-blur)*k if amount>0 else a*(1-k)+blur*k
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def color_density(im,amount):
    if amount==0:return im
    a=np.asarray(im).astype(float); gray=a.mean(2,keepdims=True); k=amount/100*.35
    return Image.fromarray(np.uint8(np.clip(a+(a-gray)*k,0,255)))
def clipping_stats(im):
    a=np.asarray(im).astype(float); return float((a<=3).mean()*100),float((a>=252).mean()*100)
def selective_saturation(im,hue,width,amount):
    if amount==0:return im
    a=np.asarray(im).astype(float)/255; mx=a.max(2); mn=a.min(2); d=mx-mn+1e-9
    h=np.zeros(mx.shape); m=mx==a[...,0]; h[m]=((a[...,1]-a[...,2])/d)[m]%6; m=mx==a[...,1]; h[m]=((a[...,2]-a[...,0])/d+2)[m]; m=mx==a[...,2]; h[m]=((a[...,0]-a[...,1])/d+4)[m]; h*=60
    dist=np.minimum(abs(h-hue),360-abs(h-hue)); mask=np.clip(1-dist/max(1,width),0,1)[...,None]; gray=a.mean(2,keepdims=True); k=amount/100
    out=a+(a-gray)*mask*k if amount>0 else a+(a-gray)*mask*k*.8
    return Image.fromarray(np.uint8(np.clip(out*255,0,255)))
def noise_score(im):
    g=np.asarray(ImageOps.grayscale(im)).astype(float); smooth=np.asarray(ImageOps.grayscale(im).filter(ImageFilter.GaussianBlur(1.2))).astype(float)
    return float(np.std(g-smooth))
def local_dodge_burn(im,xpct,ypct,radius,strength,mode):
    if strength<=0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; yy,xx=np.ogrid[:h,:w]; cx=w*xpct/100; cy=h*ypct/100; rad=max(1,min(w,h)*radius/100)
    mask=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*rad*rad))[...,None]; delta=255*(strength/100)*.28*mask
    out=a+delta if mode=='Dodge' else a-delta
    return Image.fromarray(np.uint8(np.clip(out,0,255)))
def entropy_score(im):
    h=np.asarray(ImageOps.grayscale(im).histogram(),dtype=float); p=h/h.sum(); p=p[p>0]; return float(-(p*np.log2(p)).sum())
def tilt_shift(im,center,width,strength):
    if strength<=0:return im
    blur=np.asarray(im.filter(ImageFilter.GaussianBlur(max(1,strength/12)))).astype(float); a=np.asarray(im).astype(float); h,w=a.shape[:2]
    y=np.linspace(0,100,h)[:,None]; dist=np.abs(y-center); mask=np.clip((dist-width/2)/max(1,30-width/2),0,1)[...,None]
    return Image.fromarray(np.uint8(np.clip(a*(1-mask)+blur*mask,0,255)))
def border_frame(im,size,color):
    if size<=0:return im
    px=max(1,int(min(im.size)*size/100)); return ImageOps.expand(im,border=px,fill=color)
def compression_hint(im):
    ent=entropy_score(im); noise=noise_score(im);
    return ('High',93) if ent>7.3 or noise>10 else (('Medium',86) if ent>6 else ('Low',78))
def radial_focus(im,xpct,ypct,radius,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); blur=np.asarray(im.filter(ImageFilter.GaussianBlur(max(1,strength/12)))).astype(float); h,w=a.shape[:2]
    yy,xx=np.ogrid[:h,:w]; cx=w*xpct/100; cy=h*ypct/100; rad=max(1,min(w,h)*radius/100); dist=np.sqrt((xx-cx)**2+(yy-cy)**2)
    mask=np.clip((dist-rad)/(rad*.8+1),0,1)[...,None]
    return Image.fromarray(np.uint8(np.clip(a*(1-mask)+blur*mask,0,255)))
def color_wash(im,color,strength):
    if strength<=0:return im
    c=tuple(int(color[i:i+2],16) for i in (1,3,5)); layer=Image.new('RGB',im.size,c)
    return Image.blend(im,layer,min(.35,strength/285))
def resolution_health(im):
    mp=im.width*im.height/1_000_000
    if mp>=12:return 'Large',mp
    if mp>=4:return 'Medium',mp
    return 'Small',mp
def center_light(im,xpct,ypct,radius,strength):
    if strength==0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; yy,xx=np.ogrid[:h,:w]; cx=w*xpct/100; cy=h*ypct/100; rad=max(1,min(w,h)*radius/100)
    mask=np.exp(-((xx-cx)**2+(yy-cy)**2)/(2*rad*rad))[...,None]; delta=255*(strength/100)*.22*mask
    return Image.fromarray(np.uint8(np.clip(a+delta,0,255)))
def cast_neutrality(im):
    a=np.asarray(im).astype(float).reshape(-1,3).mean(0); avg=a.mean(); dev=float(np.mean(np.abs(a-avg)))
    return dev
def export_recommendation(im):
    level,q=compression_hint(im); rc,mp=resolution_health(im)
    edge='4096' if mp>=8 else ('2560' if mp>=3 else '1600')
    return level,q,edge
def graduated_filter(im,amount,direction,color):
    if amount<=0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]
    ramp=np.linspace(1,0,h)[:,None] if direction=='Top' else np.linspace(0,1,h)[:,None]
    if direction=='Left': ramp=np.tile(np.linspace(1,0,w)[None,:],(h,1))
    elif direction=='Right': ramp=np.tile(np.linspace(0,1,w)[None,:],(h,1))
    else: ramp=np.tile(ramp,(1,w))
    c=np.array(tuple(int(color[i:i+2],16) for i in (1,3,5)),dtype=float); k=(ramp*amount/100*.35)[...,None]
    return Image.fromarray(np.uint8(np.clip(a*(1-k)+c*k,0,255)))
def grayscale_balance(im):
    a=np.asarray(im).astype(float); lum=.2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]; return float(lum.mean()),float(np.median(lum))
def edge_fade(im,amount,color):
    if amount<=0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; y,x=np.ogrid[-1:1:complex(h),-1:1:complex(w)]; r=np.clip(np.sqrt(x*x+y*y),0,1)
    mask=(r**2*amount/100*.45)[...,None]; c=np.array(tuple(int(color[i:i+2],16) for i in (1,3,5)),dtype=float)
    return Image.fromarray(np.uint8(np.clip(a*(1-mask)+c*mask,0,255)))
def thirds_overlay(im):
    out=im.copy(); d=ImageDraw.Draw(out); color=(255,215,0); width=max(2,min(out.size)//350)
    for x in (out.width//3,2*out.width//3): d.line((x,0,x,out.height),fill=color,width=width)
    for y in (out.height//3,2*out.height//3): d.line((0,y,out.width,y),fill=color,width=width)
    return out
def orientation_advice(im):
    ratio=im.width/im.height
    if ratio>1.35:return 'Landscape','Ideal for banners, desktop wallpapers, and presentation slides.'
    if ratio<.8:return 'Portrait','Ideal for stories, phone wallpapers, and portrait posts.'
    return 'Balanced','Well suited to square/social crops and general-purpose exports.'
def horizontal_gradient(im,left,right,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; lc=np.array(tuple(int(left[i:i+2],16) for i in (1,3,5)),float); rc=np.array(tuple(int(right[i:i+2],16) for i in (1,3,5)),float)
    t=np.linspace(0,1,w)[None,:,None]; layer=lc*(1-t)+rc*t; layer=np.tile(layer,(h,1,1)); k=strength/100*.28
    return Image.fromarray(np.uint8(np.clip(a*(1-k)+layer*k,0,255)))
def horizon_overlay(im):
    out=im.copy(); d=ImageDraw.Draw(out); y=out.height//2; width=max(2,min(out.size)//350); d.line((0,y,out.width,y),fill=(0,220,255),width=width)
    return out
def aspect_advisor(im):
    r=im.width/im.height; options={'1:1':1,'4:5':.8,'3:2':1.5,'16:9':16/9}; name,val=min(options.items(),key=lambda kv:abs(kv[1]-r)); return name,abs(r-val)
def image_stats(im):
    a=np.asarray(im).astype(float)
    lum=.2126*a[...,0]+.7152*a[...,1]+.0722*a[...,2]
    return float(lum.mean()),float(lum.std()),float((lum<20).mean()*100),float((lum>235).mean()*100)
def preset(im,n):
    if n=='Clean Pop': return ImageEnhance.Color(ImageEnhance.Contrast(im).enhance(1.12)).enhance(1.12)
    if n=='Warm Film': return ImageEnhance.Color(temp(im,30)).enhance(.9)
    if n=='Cool Editorial': return ImageEnhance.Contrast(temp(im,-25)).enhance(1.1)
    if n=='Mono Punch': return ImageEnhance.Contrast(ImageOps.grayscale(im)).enhance(1.35).convert('RGB')
    if n=='Vintage Fade': return ImageEnhance.Color(ImageEnhance.Contrast(temp(im,15)).enhance(.82)).enhance(.78)
    if n=='Portrait Soft': return ImageEnhance.Color(im.filter(ImageFilter.GaussianBlur(.35))).enhance(1.04)
    if n=='Cinematic': return ImageEnhance.Contrast(temp(im,-10)).enhance(1.18)
    if n=='High Key': return ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.12)).enhance(.92)
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
    pre=st.selectbox('Quick style',['None','Clean Pop','Warm Film','Cool Editorial','Mono Punch','Vintage Fade','Portrait Soft','Cinematic','High Key'])
    smart=st.toggle('Smart Auto Optimize'); aspect=st.selectbox('Crop for a platform',['Original','1:1','4:5','3:2','16:9','9:16'])
    rot=st.select_slider('Rotate',options=[0,90,180,270]); fh=st.toggle('Mirror'); fv=st.toggle('Flip vertically')
    bw=st.toggle('Black & white'); neg=st.toggle('Negative'); sep=st.slider('Sepia',0,100,0); poster_bits=st.selectbox('Posterize',['Off',6,5,4,3,2]); solar=st.slider('Solarize',0,255,0,help='0 disables solarize; higher values set the inversion threshold.')
    with st.expander('Light and colour',True):
        br=st.slider('Brightness',-100,100,0); co=st.slider('Contrast',-100,100,0); sa=st.slider('Saturation',-100,100,0); sharp=st.slider('Sharpness',-100,100,0); te=st.slider('Temperature',-100,100,0); sh=st.slider('Shadows',-100,100,0); hi=st.slider('Highlights',-100,100,0); clarity=st.slider('Clarity',0,100,0); denoise=st.slider('Noise reduction',0,5,0)
        st.caption('RGB channel mixer'); red_mix=st.slider('Red channel',50,150,100); green_mix=st.slider('Green channel',50,150,100); blue_mix=st.slider('Blue channel',50,150,100)
        st.caption('Creative finishing'); matte_amt=st.slider('Matte / fade',0,100,0); grain_amt=st.slider('Film grain',0,100,0); split_amt=st.slider('Split tone strength',0,100,0); shadow_hue=st.slider('Shadow hue',0,360,220); highlight_hue=st.slider('Highlight hue',0,360,35)
        st.caption('Lens finishing'); lens_vig=st.slider('Lens vignette',0,100,0); lens_soft=st.slider('Vignette softness',10,100,60); soft_amt=st.slider('Soft focus',0,100,0); detail_amt=st.slider('Fine detail',0,100,0)
        st.caption('Pro adjustments'); exposure=st.slider('Exposure (EV)',-2.0,2.0,0.0,0.1); vibrance=st.slider('Vibrance',0,100,0); edge_amt=st.slider('Edge sharpen',0,100,0)
        gamma=st.slider('Gamma',0.5,2.0,1.0,0.05); tint=st.slider('Tint (green to magenta)',-100,100,0); auto_levels_on=st.toggle('Auto Levels'); auto_cutoff=st.slider('Auto Levels cutoff',0,10,1)
        wb_strength=st.slider('Auto white balance',0,100,0); micro_amt=st.slider('Micro contrast',0,100,0); fade_hi=st.slider('Highlight fade',0,100,0); dehaze_amt=st.slider('Dehaze',0,100,0); bloom_amt=st.slider('Bloom / glow',0,100,0)
        texture_amt=st.slider('Texture clarity',0,100,0); shadow_color_amt=st.slider('Shadow color strength',0,100,0); shadow_color_hue=st.slider('Shadow color hue',0,360,210); highlight_color_amt=st.slider('Highlight color strength',0,100,0); highlight_color_hue=st.slider('Highlight color hue',0,360,40)
        chroma_amt=st.slider('Chromatic pop',0,100,0); skin_soft=st.slider('Soft skin',0,100,0)
        mono_mix_on=st.toggle('Monochrome channel mixer'); mono_r=st.slider('Mono red',0,200,30); mono_g=st.slider('Mono green',0,200,59); mono_b=st.slider('Mono blue',0,200,11)
        st.caption('Tone range'); black_pt=st.slider('Black point',0,80,0); white_pt=st.slider('White point',175,255,255); auto_temp=st.slider('Auto temperature correction',0,100,0)
        defringe_amt=st.slider('Defringe / chromatic cleanup',0,100,0); orton_amt=st.slider('Orton glow',0,100,0); presence=st.slider('Presence / atmospheric clarity',-100,100,0); density=st.slider('Color density',-100,100,0)
        st.caption('Targeted colour'); target_hue=st.slider('Target hue',0,360,200); target_width=st.slider('Hue range width',5,90,30); target_sat=st.slider('Target saturation',-100,100,0)
        st.caption('Local dodge / burn'); db_mode=st.selectbox('Local tool',['Off','Dodge','Burn']); db_x=st.slider('Local X %',0,100,50); db_y=st.slider('Local Y %',0,100,50); db_radius=st.slider('Local radius %',5,50,20); db_strength=st.slider('Local strength',0,100,0)
        st.caption('Tilt-shift'); ts_strength=st.slider('Tilt-shift strength',0,100,0); ts_center=st.slider('Focus band center %',0,100,50); ts_width=st.slider('Focus band width %',5,70,30)
        st.caption('Radial focus'); radial_strength=st.slider('Radial blur strength',0,100,0); radial_x=st.slider('Radial focus X %',0,100,50); radial_y=st.slider('Radial focus Y %',0,100,50); radial_radius=st.slider('Radial focus radius %',5,50,25)
        st.caption('Color wash'); wash_strength=st.slider('Color wash strength',0,100,0); wash_color=st.color_picker('Color wash color','#F2B880')
        st.caption('Center light'); center_light_strength=st.slider('Center light strength',-100,100,0); center_light_x=st.slider('Center light X %',0,100,50); center_light_y=st.slider('Center light Y %',0,100,50); center_light_radius=st.slider('Center light radius %',5,60,30)
        st.caption('Graduated filter'); grad_amount=st.slider('Graduated filter strength',0,100,0); grad_direction=st.selectbox('Graduated filter direction',['Top','Bottom','Left','Right']); grad_color=st.color_picker('Graduated filter color','#6C8EBF')
        st.caption('Edge fade'); edge_fade_amount=st.slider('Edge fade strength',0,100,0); edge_fade_color=st.color_picker('Edge fade color','#000000')
        st.caption('Gradient toning'); gradient_strength=st.slider('Gradient toning strength',0,100,0); gradient_left=st.color_picker('Gradient left color','#355C7D'); gradient_right=st.color_picker('Gradient right color','#F8B195')
        st.caption('Frame'); frame_size=st.slider('Frame size %',0,10,0); frame_color=st.color_picker('Frame color','#FFFFFF')
        st.caption('Date / caption stamp'); stamp_text=st.text_input('Stamp text',placeholder='2026-11-05 or a short caption'); stamp_pos=st.selectbox('Stamp position',['Bottom right','Bottom left','Top right','Top left'])
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
if bw: im=grayscale(im)
if neg: im=ImageOps.invert(im)
if sep: im=sepia(im,sep)
if poster_bits!='Off': im=posterize(im,poster_bits)
if solar: im=solarize(im,solar)
im=channel_balance(im,red_mix,green_mix,blue_mix)
im=matte(im,matte_amt)
im=split_tone(im,shadow_hue,highlight_hue,split_amt)
im=film_grain(im,grain_amt)
im=lens_vignette(im,lens_vig,lens_soft)
im=soft_focus(im,soft_amt)
im=edge_enhance(im,detail_amt)
im=exposure_ev(im,exposure)
im=color_boost(im,vibrance)
im=sharpen_edges(im,edge_amt)
im=gamma_adjust(im,gamma)
im=tint_shift(im,tint)
if auto_levels_on: im=auto_levels(im,auto_cutoff)
im=white_balance_gray_world(im,wb_strength)
im=micro_contrast(im,micro_amt)
im=fade_highlights(im,fade_hi)
im=dehaze(im,dehaze_amt)
im=bloom(im,bloom_amt)
im=clarity_mask(im,texture_amt)
im=shadow_color(im,shadow_color_hue,shadow_color_amt)
im=highlight_color(im,highlight_color_hue,highlight_color_amt)
im=chromatic_pop(im,chroma_amt)
im=soft_skin(im,skin_soft)
if mono_mix_on: im=monochrome_mix(im,mono_r,mono_g,mono_b)
im=rgb_curve(im,black_pt,white_pt)
im=color_temperature_auto(im,auto_temp)
im=defringe(im,defringe_amt)
im=orton(im,orton_amt)
im=haze_glow_balance(im,presence)
im=color_density(im,density)
im=selective_saturation(im,target_hue,target_width,target_sat)
if db_mode!='Off': im=local_dodge_burn(im,db_x,db_y,db_radius,db_strength,db_mode)
im=tilt_shift(im,ts_center,ts_width,ts_strength)
im=radial_focus(im,radial_x,radial_y,radial_radius,radial_strength)
im=color_wash(im,wash_color,wash_strength)
im=center_light(im,center_light_x,center_light_y,center_light_radius,center_light_strength)
im=graduated_filter(im,grad_amount,grad_direction,grad_color)
im=edge_fade(im,edge_fade_amount,edge_fade_color)
im=horizontal_gradient(im,gradient_left,gradient_right,gradient_strength)
im=border_frame(im,frame_size,frame_color)
im=add_date_stamp(im,stamp_text,stamp_pos)
im=preset(im,pre)
if smart: im=auto(im)
im=ImageEnhance.Brightness(im).enhance(max(.05,1+br/100)); im=ImageEnhance.Contrast(im).enhance(max(0,1+co/100)); im=ImageEnhance.Color(im).enhance(max(0,1+sa/100)); im=ImageEnhance.Sharpness(im).enhance(max(0,1+sharp/50)); im=temp(im,te); im=tone(im,sh,hi)
if denoise: im=im.filter(ImageFilter.MedianFilter(size=denoise*2+1))
if clarity: im=im.filter(ImageFilter.UnsharpMask(radius=2,percent=60+clarity*2,threshold=3))
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
    mask_mode=st.selectbox('Luminance mask preview',['Off','Highlights','Midtones','Shadows']); mask_opacity=st.slider('Mask overlay opacity',10,100,55) if mask_mode!='Off' else 55
    after_preview=luminance_mask_preview(im,mask_mode,mask_opacity) if mask_mode!='Off' else im
    show_thirds=st.toggle('Show rule-of-thirds grid'); after_preview=thirds_overlay(after_preview) if show_thirds else after_preview
    show_horizon=st.toggle('Show horizon guide'); after_preview=horizon_overlay(after_preview) if show_horizon else after_preview
    if show:
        a,b=st.columns(2); a.subheader('Before'); a.image(original,use_container_width=True); b.subheader('After'); b.image(after_preview,use_container_width=True)
    else: st.image(after_preview,use_container_width=True)
    st.caption(f'Original {original.width}×{original.height} | Edited {im.width}×{im.height}')
with creator_tab:
    st.subheader('Colour palette extractor')
    cols=palette(im); blocks=st.columns(len(cols))
    for c,hx in zip(blocks,cols): c.color_picker(hx,hx,disabled=True)
    st.code(json.dumps({'palette':cols},indent=2),language='json')
    st.subheader('Preset proof sheet')
    names=['Original','Clean Pop','Warm Film','Cool Editorial','Mono Punch','Vintage Fade','Portrait Soft','Cinematic','High Key']; proof=contact_sheet([original]+[preset(original,n) for n in names[1:]],names)
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
    st.subheader('Exposure analysis')
    mean_luma,contrast,shadows_pct,highlights_pct=image_stats(im)
    e1,e2,e3,e4=st.columns(4); e1.metric('Mean luminance',f'{mean_luma:.0f}/255'); e2.metric('Contrast spread',f'{contrast:.1f}'); e3.metric('Deep shadows',f'{shadows_pct:.1f}%'); e4.metric('Bright highlights',f'{highlights_pct:.1f}%')
    if shadows_pct>20: st.warning('A large portion of the image is near black. Consider raising Shadows.')
    if highlights_pct>20: st.warning('A large portion of the image is very bright. Consider lowering Highlights.')
    if shadows_pct<=20 and highlights_pct<=20: st.success('Exposure distribution looks balanced for general editing.')
    st.subheader('Color cast analysis')
    channel_means,cast_spread=color_cast_score(im)
    c1,c2,c3,c4=st.columns(4); c1.metric('Red mean',f'{channel_means[0]:.0f}'); c2.metric('Green mean',f'{channel_means[1]:.0f}'); c3.metric('Blue mean',f'{channel_means[2]:.0f}'); c4.metric('Channel spread',f'{cast_spread:.1f}')
    if cast_spread>35: st.info('Noticeable channel imbalance detected. Try Auto White Balance or Temperature/Tint correction.')
    else: st.success('No strong global color cast detected.')
    st.subheader('Focus analysis')
    focus=focus_score(im); st.metric('Edge focus score',f'{focus:.1f}')
    if focus<80: st.info('Low edge contrast detected. Fine Detail, Clarity, or Edge Sharpen may help if the source is slightly soft.')
    elif focus>800: st.info('Very high edge contrast detected. Review sharpening to avoid halos or crunchy detail.')
    else: st.success('Edge focus score is in a useful general editing range.')
    st.subheader('Dynamic range')
    dr_low,dr_high,dr_span=dynamic_range(im); d1,d2,d3=st.columns(3); d1.metric('1st percentile',f'{dr_low:.0f}'); d2.metric('99th percentile',f'{dr_high:.0f}'); d3.metric('Tonal span',f'{dr_span:.0f}/255')
    if dr_span<120: st.info('Compressed tonal span detected. Auto Levels, Contrast, or Dehaze can increase separation.')
    elif dr_span>235: st.info('Very wide tonal span detected. Check highlight and shadow clipping before export.')
    else: st.success('Dynamic range is broadly distributed for general photo editing.')
    st.subheader('Clipping check')
    black_clip,white_clip=clipping_stats(im); q1,q2=st.columns(2); q1.metric('Near-black channels',f'{black_clip:.2f}%'); q2.metric('Near-white channels',f'{white_clip:.2f}%')
    if black_clip>5 or white_clip>5: st.warning('Clipping risk detected. Review Exposure, Black/White Point, Highlights, and Shadows.')
    else: st.success('No material channel clipping detected at the 5% review threshold.')
    st.subheader('Noise analysis')
    noise=noise_score(im); st.metric('Texture / noise score',f'{noise:.2f}')
    if noise>12: st.info('High fine-grain activity detected. Consider Noise Reduction before strong sharpening.')
    elif noise<2: st.info('Very smooth image detected. Avoid excessive denoising or softening.')
    else: st.success('Fine-detail noise level is moderate for general editing.')
    st.subheader('Image complexity')
    entropy=entropy_score(im); st.metric('Tonal entropy',f'{entropy:.2f} bits')
    if entropy<5.5: st.info('Low tonal complexity detected. This is common for graphics, skies, or minimalist images; use aggressive compression carefully around gradients.')
    elif entropy>7.5: st.info('High tonal complexity detected. Prefer higher-quality JPEG/WebP settings to preserve fine detail.')
    else: st.success('Tonal complexity is moderate and suitable for standard export presets.')
    st.subheader('Compression advisor')
    compression_class,suggested_quality=compression_hint(im); st.metric('Suggested JPEG/WebP quality',str(suggested_quality)); st.caption(f'Image compression class: {compression_class}. This suggestion uses tonal entropy and fine-detail activity.')
    st.subheader('Resolution advisor')
    resolution_class,megapixels=resolution_health(im); st.metric('Image size class',resolution_class); st.caption(f'{megapixels:.2f} MP at {im.width} x {im.height} px. Large images are best for print/master exports; smaller images are better suited to web/social presets.')
    st.subheader('Smart export recommendation')
    rec_class,rec_quality,rec_edge=export_recommendation(im); neutrality=cast_neutrality(im); r1,r2,r3=st.columns(3); r1.metric('Recommended quality',str(rec_quality)); r2.metric('Suggested long edge',f'{rec_edge}px'); r3.metric('Color neutrality',f'{neutrality:.1f}')
    st.caption(f'Profile: {rec_class} compression need. Recommendations combine resolution, tonal complexity, and detail activity.')
    mean_gray,median_gray=grayscale_balance(im); st.subheader('Luminance balance'); l1,l2=st.columns(2); l1.metric('Mean luminance',f'{mean_gray:.0f}/255'); l2.metric('Median luminance',f'{median_gray:.0f}/255')
    if abs(mean_gray-median_gray)>25: st.info('The image has an uneven luminance distribution. Review local lighting, shadows, or highlights if that is not intentional.')
    else: st.success('Mean and median luminance are reasonably aligned.')
    st.subheader('Composition advisor')
    orientation,orientation_tip=orientation_advice(im); st.metric('Current orientation',orientation); st.caption(orientation_tip)
    nearest_aspect,aspect_error=aspect_advisor(im); a1,a2=st.columns(2); a1.metric('Nearest common ratio',nearest_aspect); a2.metric('Ratio deviation',f'{aspect_error:.3f}')

st.divider(); st.subheader('3. Export')
preset_export=st.selectbox('Export preset',['Custom','Web High Quality','Social 1080','Archive PNG','Email Compact','4K Display','Privacy PNG','Photo Print','Phone Wallpaper','Square Profile','Messaging','Web Thumbnail','Portfolio','Low Bandwidth','Presentation HD','Presentation 4K','Blog Optimized','Master JPEG','Gallery WebP','Quick Share','Social High Quality','Proof JPEG','Mobile WebP','Client Review','Contact Sheet Web','Lossless Master','Desktop Wallpaper','Fast Preview','Marketplace','Tiny Web','Portfolio Master','Chat Optimized','Email Small','Web Hero','Detailed Web','Draft Proof','Print Proof','Ultra Web','Retina Web','Original Backup','Smart Web','High Res JPEG','Editorial Web','Archive JPEG','Story Portrait','Slide Ready','Cinematic Web','Social Master'])
defaults={'Custom':('JPEG',92,'Original'),'Web High Quality':('WEBP',90,2048),'Social 1080':('JPEG',90,1080),'Archive PNG':('PNG',100,'Original'),'Email Compact':('JPEG',82,1600),'4K Display':('JPEG',94,4096),'Privacy PNG':('PNG',100,'Original'),'Photo Print':('JPEG',96,'Original'),'Phone Wallpaper':('JPEG',92,2560),'Square Profile':('JPEG',92,1080),'Messaging':('JPEG',85,1600),'Web Thumbnail':('WEBP',82,1080),'Portfolio':('WEBP',94,2560),'Low Bandwidth':('WEBP',72,1600),'Presentation HD':('JPEG',92,2048),'Presentation 4K':('JPEG',94,4096),'Blog Optimized':('WEBP',88,2048),'Master JPEG':('JPEG',98,'Original'),'Gallery WebP':('WEBP',92,2048),'Quick Share':('JPEG',80,1080),'Social High Quality':('JPEG',94,2048),'Proof JPEG':('JPEG',75,1600),'Mobile WebP':('WEBP',84,1600),'Client Review':('JPEG',88,2048),'Contact Sheet Web':('WEBP',86,2048),'Lossless Master':('PNG',100,'Original'),'Desktop Wallpaper':('JPEG',93,4096),'Fast Preview':('WEBP',76,1080),'Marketplace':('JPEG',90,2048),'Tiny Web':('WEBP',68,1080),'Portfolio Master':('JPEG',97,4096),'Chat Optimized':('WEBP',78,1600),'Email Small':('JPEG',76,1080),'Web Hero':('WEBP',91,2560),'Detailed Web':('WEBP',95,2560),'Draft Proof':('JPEG',70,1600),'Print Proof':('JPEG',95,4096),'Ultra Web':('WEBP',96,4096),'Retina Web':('WEBP',93,4096),'Original Backup':('PNG',100,'Original'),'Smart Web':('WEBP',90,2560),'High Res JPEG':('JPEG',96,4096),'Editorial Web':('WEBP',92,2560),'Archive JPEG':('JPEG',99,'Original'),'Story Portrait':('JPEG',92,2560),'Slide Ready':('JPEG',93,2048),'Cinematic Web':('WEBP',94,2560),'Social Master':('JPEG',96,2560)}[preset_export]
a,b,c,d=st.columns([1,1,1,2]); formats=['JPEG','PNG','WEBP']; fmt=a.selectbox('Format',formats,index=formats.index(defaults[0])); quality=b.slider('Quality',60,100,defaults[1]); edges=['Original',4096,2560,2048,1600,1080]; maxside=c.selectbox('Long edge',edges,index=edges.index(defaults[2])); name=d.text_input('Filename','peabox-edit')
custom_size=st.toggle('Custom export dimensions'); keep_ratio=True
if custom_size:
    r1,r2,r3=st.columns(3); out_w=r1.number_input('Width (px)',1,12000,int(im.width)); out_h=r2.number_input('Height (px)',1,12000,int(im.height)); keep_ratio=r3.toggle('Keep aspect ratio',value=True)
    im=resize_exact(im,int(out_w),int(out_h),keep_ratio)
out=im.copy()
if maxside!='Original' and max(out.size)>int(maxside):
    s=int(maxside)/max(out.size); out=out.resize((int(out.width*s),int(out.height*s)),R)
buf=io.BytesIO(); kw={'format':fmt}
if fmt=='JPEG': kw|={'quality':quality,'optimize':True,'progressive':True}
elif fmt=='WEBP': kw|={'quality':quality,'method':6}
else: kw|={'optimize':True}
out.save(buf,**kw); ext={'JPEG':'jpg','PNG':'png','WEBP':'webp'}[fmt]; mime={'JPEG':'image/jpeg','PNG':'image/png','WEBP':'image/webp'}[fmt]
dims,mp=pixel_dimensions(out); st.caption(f'Output: {dims} px | {mp:.2f} MP | {fmt} | Quality {quality if fmt != "PNG" else "lossless"} | Encoded size: {len(buf.getvalue())/1024:.1f} KB')
st.download_button('Download edited photo',buf.getvalue(),f'{Path(name).stem}.{ext}',mime,type='primary',use_container_width=True)
st.caption('Keyboard accessibility depends on your browser. Every control has a visible label, and the original is never overwritten.')
