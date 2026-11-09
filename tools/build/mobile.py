"""Phone-size (Elementor "mobile" breakpoint, < 768px) values for the home page and footer.

Everything here is written into Elementor's own responsive settings (keys ending in
`_mobile`), so each value shows up under the phone icon in the Elementor panel and can be
edited there. Desktop and tablet values are untouched.

Goals: no single-word last lines, buttons that sit side by side, photos in landscape
proportions instead of tall narrow crops, and a shorter page (quick links as a 2x2 grid).
"""
from el import unit, dims

# desktop font-size spec -> phone font size (px)
HEADING_SIZES = {
    'clamp(40px,5.6vw,68px)': 36,   # hero H1: two lines "Pyhtää Water / Cooperative"
    19: 15,                         # hero subtitle on one line (balanced 2 lines on the narrowest phones)
    'clamp(28px,3.6vw,40px)': 26,   # "Water Testing Results Are Available"
    'clamp(24px,2.8vw,32px)': 21,   # announcement heading
    'clamp(28px,3.4vw,40px)': 26,   # "Meter Readings and Contact Information", "Contact"
    20: 18,                         # news article titles
    'clamp(30px,3.8vw,44px)': 28,   # billing heading
    'clamp(22px,2.6vw,30px)': 19,   # long "We kindly ask you..." heading
    18: 15,                         # quick-link titles in the 2x2 grid
    'clamp(22px,2.4vw,26px)': 21,   # contact card names
    30: 24,                         # EUR 2 badge
}
TEXT_SIZES = {17: 16, 16: 15, 15: 14.5}

# photo areas: desktop min-height spec -> phone height (landscape photos)
VISUAL_HEIGHTS = {
    'clamp(380px,46vw,540px)': 300,  # hero collage
    340: 230,                        # announcement meter photo
    'clamp(340px,40vw,500px)': 250,  # meter readings photo
    'clamp(360px,40vw,500px)': 260,  # news + contact-details photos
}


def _size_key(v):
    if not v:
        return None
    s = v.get('size')
    return s if v.get('unit') == 'custom' else (int(s) if isinstance(s, (int, float)) and float(s).is_integer() else s)


def tune(elements, scope='home'):
    for e in elements:
        st = e['settings']
        if e['elType'] == 'container':
            cls = st.get('css_classes', '')
            mh = _size_key(st.get('min_height'))
            if st.get('position') != 'absolute' and mh in VISUAL_HEIGHTS:
                st['min_height_mobile'] = unit(VISUAL_HEIGHTS[mh])
            if 'pv-quick' in cls.split():               # 2x2 quick links
                st['width_mobile'] = unit('calc(50% - 8px)')
                st['padding_mobile'] = dims(20, 8, 16, 8)
                st['flex_gap_mobile'] = {'unit': 'px', 'column': '10', 'row': '10', 'isLinked': True, 'size': 10}
            if 'pv-quick__drop' in cls:
                st['width_mobile'] = unit(76)
                st['min_height_mobile'] = unit(76)
                st['margin_mobile'] = dims(8, 0, 0, 0)
            if _size_key(st.get('width')) == 132:          # EUR 2 badge
                st['width_mobile'] = unit(104)
                st['min_height_mobile'] = unit(104)
        elif e['elType'] == 'widget':
            w = e['widgetType']
            if w == 'heading':
                k = _size_key(st.get('typography_font_size'))
                if k in HEADING_SIZES:
                    st['typography_font_size_mobile'] = unit(HEADING_SIZES[k])
            elif w == 'text-editor':
                k = _size_key(st.get('typography_font_size'))
                if k in TEXT_SIZES:
                    st['typography_font_size_mobile'] = unit(TEXT_SIZES[k])
            elif w == 'button' and scope == 'home':
                k = _size_key(st.get('typography_font_size'))
                if k in (14, 15):
                    st['typography_font_size_mobile'] = unit(12.5)
                    if st.get('typography_letter_spacing', {}).get('size', 0) >= 0.04:
                        st['typography_letter_spacing_mobile'] = {'unit': 'em', 'size': 0.03, 'sizes': []}
                    pad = st.get('text_padding', {})
                    if pad.get('right') == '8':                      # text-link style buttons
                        st['text_padding_mobile'] = dims(12, 4)
                    elif pad.get('right') == '20':                   # contact chips
                        st['text_padding_mobile'] = dims(11, 16)
                    else:                                            # filled buttons
                        st['text_padding_mobile'] = dims(12, 16)
            elif w == 'icon' and _size_key(st.get('size')) == 50:    # quick-link icons
                st['size_mobile'] = unit(38)
            elif w == 'copyright':
                st['caption_typography_font_size_mobile'] = unit(13)
        tune(e['elements'], scope)
    return elements
