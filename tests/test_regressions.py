from PIL import Image
import peabox_core as c

def test_tiny_and_extreme_dimensions_do_not_crash():
    for size in [(1,1),(2,50),(50,2),(400,20),(20,400)]:
        im=Image.new('RGB',size,(120,130,140)); assert c.resize_exact(im,1,1,True).width>=1; assert c.pixel(im,8).size==size

def test_effects_do_not_mutate_original():
    im=Image.new('RGB',(32,32),(100,120,140)); before=im.tobytes(); c.sepia(im,80); c.center_light(im,50,50,20,50); assert im.tobytes()==before
