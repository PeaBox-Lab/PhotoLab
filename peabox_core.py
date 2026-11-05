"""PeaBox Photo Lab image-processing core. UI-independent and testable."""
import colorsys
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

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
def corner_tint(im,color,strength):
    if strength<=0:return im
    a=np.asarray(im).astype(float); h,w=a.shape[:2]; y,x=np.ogrid[-1:1:complex(h),-1:1:complex(w)]; r=np.clip(np.sqrt(x*x+y*y),0,1)
    mask=(r**1.6*strength/100*.28)[...,None]; c=np.array(tuple(int(color[i:i+2],16) for i in (1,3,5)),float)
    return Image.fromarray(np.uint8(np.clip(a*(1-mask)+c*mask,0,255)))
def diagonal_overlay(im):
    out=im.copy(); d=ImageDraw.Draw(out); c=(255,180,0); w=max(2,min(out.size)//350); d.line((0,0,out.width,out.height),fill=c,width=w); d.line((out.width,0,0,out.height),fill=c,width=w); return out
def subject_contrast(im):
    g=np.asarray(ImageOps.grayscale(im)).astype(float); h,w=g.shape; cy,cx=h//2,w//2; ry,rx=max(1,h//4),max(1,w//4); center=g[cy-ry:cy+ry,cx-rx:cx+rx].mean(); overall=g.mean(); return float(center-overall)
