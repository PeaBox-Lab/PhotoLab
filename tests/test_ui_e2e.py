import os
from streamlit.testing.v1 import AppTest

os.environ['PEABOX_TEST_MODE']='1'
APP='app.py'

def run(at):
    at.run(timeout=30)
    assert not at.exception, [str(x.value) for x in at.exception]
    return at

def by_label(items,label):
    return next(x for x in items if x.label==label)

def test_full_ui_renders_and_output_controls_exist():
    at=run(AppTest.from_file(APP,default_timeout=30))
    assert len(at.selectbox)>=12
    assert len(at.slider)>=82
    assert len(at.toggle)>=10
    assert len(at.color_picker)>=16
    assert len(at.text_input)>=3
    assert len(at.get('file_uploader'))==1
    assert any(x.label=='Export preset group' for x in at.selectbox)
    assert any(x.label=='Filename' for x in at.text_input)

def test_every_selectbox_menu_action():
    at=run(AppTest.from_file(APP,default_timeout=30))
    labels=[x.label for x in at.selectbox]
    actions=0
    for label in labels:
        widget=by_label(at.selectbox,label)
        options=list(widget.options)
        for option in options:
            by_label(at.selectbox,label).select(option)
            run(at); actions+=1
    assert actions>=100

def test_every_select_slider_action():
    at=run(AppTest.from_file(APP,default_timeout=30))
    controls=at.get('select_slider')
    assert controls
    for option in list(controls[0].options):
        at.get('select_slider')[0].set_value(int(option)); run(at)

def test_every_toggle_button_state():
    at=run(AppTest.from_file(APP,default_timeout=30))
    labels=[x.label for x in at.toggle]
    for label in labels:
        by_label(at.toggle,label).set_value(True); run(at)
        by_label(at.toggle,label).set_value(False); run(at)

def test_every_slider_minimum_and_maximum():
    at=run(AppTest.from_file(APP,default_timeout=30))
    labels=[x.label for x in at.slider]
    for label in labels:
        w=by_label(at.slider,label); original=w.value; low=w.proto.min; high=w.proto.max
        by_label(at.slider,label).set_value(low); run(at)
        by_label(at.slider,label).set_value(high); run(at)
        by_label(at.slider,label).set_value(original); run(at)

def test_all_text_and_color_actions():
    at=run(AppTest.from_file(APP,default_timeout=30))
    for label in [x.label for x in at.text_input]:
        by_label(at.text_input,label).set_value('PeaBox UI test'); run(at)
        by_label(at.text_input,label).set_value(''); run(at)
    for label in [x.label for x in at.color_picker]:
        by_label(at.color_picker,label).set_value('#123456'); run(at)

def test_conditional_custom_export_dimensions_and_formats():
    at=run(AppTest.from_file(APP,default_timeout=30))
    by_label(at.toggle,'Custom export dimensions').set_value(True); run(at)
    assert len(at.number_input)==2
    by_label(at.number_input,'Width (px)').set_value(640); run(at)
    by_label(at.number_input,'Height (px)').set_value(480); run(at)
    for fmt in ['JPEG','PNG','WEBP']:
        by_label(at.selectbox,'Format').select(fmt); run(at)

def test_export_group_exposes_every_preset():
    at=run(AppTest.from_file(APP,default_timeout=30))
    by_label(at.selectbox,'Export preset group').select('All presets'); run(at)
    preset=by_label(at.selectbox,'Export preset')
    assert len(preset.options)>=50
    for option in list(preset.options):
        by_label(at.selectbox,'Export preset').select(option); run(at)
