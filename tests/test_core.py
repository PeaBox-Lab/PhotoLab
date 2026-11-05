import io
import numpy as np
from PIL import Image
import peabox_core as c

def sample(w=96,h=64):
    x=np.linspace(0,255,w,dtype=np.uint8); a=np.zeros((h,w,3),dtype=np.uint8); a[:,:,0]=x; a[:,:,1]=128; a[:,:,2]=255-x; return Image.fromarray(a,'RGB')

def assert_rgb(im): assert isinstance(im,Image.Image) and im.mode=='RGB' and im.width>0 and im.height>0

def test_resize_and_crop():
    im=sample(); assert c.crop_ratio(im,'1:1').size==(64,64); r=c.resize_exact(im,50,50,True); assert max(r.size)<=50

def test_core_adjustments_smoke():
    im=sample(); funcs=[lambda x:c.temp(x,20),lambda x:c.tone(x,20,-20),lambda x:c.sepia(x,60),lambda x:c.channel_balance(x,110,90,100),lambda x:c.exposure_ev(x,.5),lambda x:c.gamma_adjust(x,1.2),lambda x:c.white_balance_gray_world(x,50),lambda x:c.dehaze(x,30),lambda x:c.micro_contrast(x,30),lambda x:c.defringe(x,20),lambda x:c.orton(x,20),lambda x:c.color_density(x,20),lambda x:c.selective_saturation(x,180,30,25),lambda x:c.local_dodge_burn(x,50,50,20,20,'Dodge'),lambda x:c.tilt_shift(x,50,30,20),lambda x:c.radial_focus(x,50,50,25,20),lambda x:c.center_light(x,50,50,30,20),lambda x:c.edge_fade(x,20,'#000000'),lambda x:c.horizontal_gradient(x,'#112233','#ddeeff',20),lambda x:c.corner_tint(x,'#223344',20)]
    for f in funcs: assert_rgb(f(im))

def test_analysis_contracts():
    im=sample(); assert c.focus_score(im)>=0; assert c.noise_score(im)>=0; assert 0<=c.entropy_score(im)<=8; assert len(c.dynamic_range(im))==3; assert len(c.clipping_stats(im))==2; assert c.resolution_health(im)[1]>0; assert len(c.export_recommendation(im))==3

def test_export_formats():
    im=sample()
    for fmt,kw in [('JPEG',{'quality':90}),('PNG',{}),('WEBP',{'quality':85})]:
        b=io.BytesIO(); im.save(b,format=fmt,**kw); assert len(b.getvalue())>100
