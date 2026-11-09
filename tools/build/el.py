"""Small helpers that emit Elementor (classic containers + widgets) JSON.

Every element produced here is a normal, editable Elementor container or widget.
Colours reference the kit's global colours so they can be changed site-wide.
"""
import hashlib
import itertools

_counter = itertools.count(1)
_seed = 'pv'


def set_seed(seed):
    global _seed, _counter
    _seed = seed
    _counter = itertools.count(1)


def eid():
    return hashlib.md5(f'{_seed}-{next(_counter)}'.encode()).hexdigest()[:7]


# ---------------------------------------------------------------- media
SITE = 'https://pyhtaanvok.fi-c.seravo.com'
MEDIA = {}  # name -> (id, url); filled by build.py


def media(name):
    i, u = MEDIA[name]
    return {'id': i, 'url': u, 'source': 'library'}


def svg_icon(name):
    i, u = MEDIA[name]
    return {'value': {'id': i, 'url': u}, 'library': 'svg'}


# ---------------------------------------------------------------- colours
COLORS = {  # global id -> hex
    'primary': '#1F5F99', 'secondary': '#0B2E4F', 'text': '#3A4854', 'accent': '#F2B53A',
    'pvsky': '#5FA8D3', 'pvcream': '#F7F6F2', 'pvink': '#14202B', 'pvgrey': '#4A5966',
    'pvmist': '#E8F1F7', 'pvice': '#D6E8F4', 'pvpale': '#A9D1EA', 'pvline': '#C9D6E0',
    'pvwhite': '#FFFFFF', 'pvdeep': '#082440',
}
HEX2ID = {v.upper(): k for k, v in COLORS.items()}


def color(settings, key, value):
    """Set a colour control; use the global colour when the value is a palette colour."""
    if value is None:
        return settings
    v = value.upper() if value.startswith('#') else value
    settings[key] = value
    if v in HEX2ID:
        settings.setdefault('__globals__', {})[key] = f'globals/colors?id={HEX2ID[v]}'
    return settings


# ---------------------------------------------------------------- units
def px(n):
    return {'unit': 'px', 'size': n, 'sizes': []}


def unit(v):
    """Number -> px, '1.5em' style strings -> unit, anything else -> custom (e.g. clamp())."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return {'unit': 'px', 'size': v, 'sizes': []}
    for u in ('em', 'rem', '%', 'vw', 'vh', 'deg'):
        if v.endswith(u):
            try:
                return {'unit': u, 'size': float(v[:-len(u)]), 'sizes': []}
            except ValueError:
                break
    if v.endswith('px'):
        try:
            return {'unit': 'px', 'size': float(v[:-2]), 'sizes': []}
        except ValueError:
            pass
    return {'unit': 'custom', 'size': v, 'sizes': []}


def dims(t, r=None, b=None, l=None):
    r = t if r is None else r
    b = t if b is None else b
    l = r if l is None else l
    vals = [t, r, b, l]
    if all(isinstance(x, (int, float)) for x in vals):
        return {'unit': 'px', 'top': str(t), 'right': str(r), 'bottom': str(b), 'left': str(l), 'isLinked': len(set(vals)) == 1}
    s = [f'{x}px' if isinstance(x, (int, float)) else x for x in vals]
    return {'unit': 'custom', 'top': s[0], 'right': s[1], 'bottom': s[2], 'left': s[3], 'isLinked': False}


def gap(row, col=None):
    col = row if col is None else col
    if isinstance(row, (int, float)) and isinstance(col, (int, float)):
        return {'unit': 'px', 'column': str(col), 'row': str(row), 'isLinked': row == col, 'size': col}
    r = f'{row}px' if isinstance(row, (int, float)) else row
    c = f'{col}px' if isinstance(col, (int, float)) else col
    return {'unit': 'custom', 'column': c, 'row': r, 'isLinked': r == c, 'size': c}


def typo(prefix, size=None, weight=None, lh=None, ls=None, transform=None, family='Poppins'):
    s = {f'{prefix}_typography': 'custom', f'{prefix}_font_family': family}
    if size is not None:
        s[f'{prefix}_font_size'] = unit(size)
    if weight is not None:
        s[f'{prefix}_font_weight'] = str(weight)
    if lh is not None:
        s[f'{prefix}_line_height'] = {'unit': 'em', 'size': lh, 'sizes': []} if isinstance(lh, (int, float)) else unit(lh)
    if ls is not None:
        s[f'{prefix}_letter_spacing'] = {'unit': 'em', 'size': ls, 'sizes': []}
    if transform:
        s[f'{prefix}_text_transform'] = transform
    return s


def shadow(h, v, blur, spread, col, inset=False):
    s = {'box_shadow_box_shadow_type': 'yes',
         'box_shadow_box_shadow': {'horizontal': h, 'vertical': v, 'blur': blur, 'spread': spread, 'color': col}}
    if inset:
        s['box_shadow_box_shadow_position'] = 'inset'
    return s


# ---------------------------------------------------------------- elements
def con(*children, d='column', gap_=0, pad=None, justify=None, align=None, wrap=False, width=None, boxed=None,
        bg=None, minh=None, radius=None, cls=None, tag=None, link=None, grow=None, abs_=None, z=None,
        overflow=None, margin=None, extra=None, isinner=True):
    s = {'content_width': 'boxed' if boxed else 'full', 'flex_direction': d, 'flex_gap': gap(*gap_) if isinstance(gap_, tuple) else gap(gap_)}
    if boxed:
        s['boxed_width'] = unit(boxed)
    if width is not None:
        s['width'] = unit(width)
    if pad is not None:
        s['padding'] = dims(*pad) if isinstance(pad, tuple) else dims(pad)
    if margin is not None:
        s['margin'] = dims(*margin) if isinstance(margin, tuple) else dims(margin)
    if justify:
        s['flex_justify_content'] = justify
    if align:
        s['flex_align_items'] = align
    if wrap:
        s['flex_wrap'] = 'wrap'
    if bg:
        s['background_background'] = 'classic'
        color(s, 'background_color', bg)
    if minh is not None:
        s['min_height'] = unit(minh)
    if radius is not None:
        s['border_radius'] = dims(*radius) if isinstance(radius, tuple) else dims(radius)
    if cls:
        s['css_classes'] = cls
    if tag:
        s['html_tag'] = tag
    if link:
        s['html_tag'] = 'a'
        s['link'] = {'url': link, 'is_external': '', 'nofollow': '', 'custom_attributes': ''}
    if grow:  # (basis, grow) – the design's auto-fit grid columns
        s['_flex_size'] = 'custom'
        s['_flex_grow'] = grow
        s['_flex_shrink'] = 1
    if abs_:
        s['position'] = 'absolute'
        s.update(offsets(abs_))
    if z is not None:
        s['z_index'] = z
    if overflow:
        s['overflow'] = overflow
    if extra:
        s.update(extra)
    return {'id': eid(), 'elType': 'container', 'isInner': isinner, 'settings': s, 'elements': [c for c in children if c]}


def offsets(o):
    """o = dict with any of left/right/top/bottom -> value (number px or '6%')."""
    s = {}
    if 'right' in o:
        s['_offset_orientation_h'] = 'end'
        s['_offset_x_end'] = unit(o['right'])
    elif 'left' in o:
        s['_offset_orientation_h'] = 'start'
        s['_offset_x'] = unit(o['left'])
    if 'bottom' in o:
        s['_offset_orientation_v'] = 'end'
        s['_offset_y_end'] = unit(o['bottom'])
    elif 'top' in o:
        s['_offset_orientation_v'] = 'start'
        s['_offset_y'] = unit(o['top'])
    return s


def widget(wtype, settings):
    return {'id': eid(), 'elType': 'widget', 'widgetType': wtype, 'isInner': False, 'settings': settings, 'elements': []}


def common(s, cls=None, margin=None, pad=None, width=None, abs_=None, z=None, bg=None, radius=None, grow=None, align_self=None):
    if cls:
        s['_css_classes'] = cls
    if margin is not None:
        s['_margin'] = dims(*margin) if isinstance(margin, tuple) else dims(margin)
    if pad is not None:
        s['_padding'] = dims(*pad) if isinstance(pad, tuple) else dims(pad)
    if width == 'auto':
        s['_element_width'] = 'auto'
    elif width is not None:
        s['_element_width'] = 'initial'
        s['_element_custom_width'] = unit(width)
    if abs_:
        s['_position'] = 'absolute'
        s.update(offsets(abs_))
    if z is not None:
        s['_z_index'] = z
    if bg:
        s['_background_background'] = 'classic'
        color(s, '_background_color', bg)
    if radius is not None:
        s['_border_radius'] = dims(*radius) if isinstance(radius, tuple) else dims(radius)
    if grow:
        s['_flex_size'] = 'custom'
        s['_flex_grow'] = grow
        s['_flex_shrink'] = 1
    if align_self:
        s['_flex_align_self'] = align_self
    return s


def heading(text, size, weight=600, lh=1.5, ls=None, col=None, tag='h2', transform=None, align=None, link=None, **kw):
    s = {'title': text, 'header_size': tag}
    s.update(typo('typography', size, weight, lh, ls, transform))
    color(s, 'title_color', col)
    if align:
        s['align'] = align
    if link:
        s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return widget('heading', common(s, **kw))


def text(html, size=16, lh=1.6, col=None, weight=None, align=None, **kw):
    s = {'editor': html}
    s.update(typo('typography', size, weight, lh))
    color(s, 'text_color', col)
    if align:
        s['align'] = align
    return widget('text-editor', common(s, **kw))


def button(label, url, size=15, weight=600, ls=0.04, transform='uppercase', fg=None, bg=None, hfg=None, hbg=None,
           pad=(14, 26), radius=6, icon=None, icon_pos='left', underline=False, align=None, **kw):
    s = {'text': label, 'link': {'url': url, 'is_external': '', 'nofollow': ''}, 'size': 'sm'}
    s.update(typo('typography', size, weight, None, ls, transform))
    s['typography_line_height'] = {'unit': 'em', 'size': 1.5, 'sizes': []}
    color(s, 'button_text_color', fg)
    if bg:
        s['background_background'] = 'classic'
        color(s, 'background_color', bg)
    else:
        s['background_background'] = 'classic'
        s['background_color'] = 'rgba(0,0,0,0)'
    color(s, 'hover_color', hfg)
    if hbg:
        s['button_background_hover_background'] = 'classic'
        color(s, 'button_background_hover_color', hbg)
    s['text_padding'] = dims(*pad) if isinstance(pad, tuple) else dims(pad)
    s['border_radius'] = dims(radius)
    if icon:
        s['selected_icon'] = icon
        s['icon_align'] = 'row' if icon_pos == 'left' else 'row-reverse'
    if align:
        s['align'] = align
    return widget('button', common(s, **kw))


def image(name, width=None, align='left', link=None, **kw):
    s = {'image': media(name), 'image_size': 'full', 'align': align}
    if width is not None:
        s['width'] = unit(width)
    if link:
        s['link_to'] = 'custom'
        s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return widget('image', common(s, **kw))


def icon(name, size, col=None, align='center', **kw):
    s = {'selected_icon': svg_icon(name), 'size': unit(size), 'align': align, 'view': 'default'}
    color(s, 'primary_color', col)
    return widget('icon', common(s, **kw))


def bg_image(s, name, size='cover', pos='center center', repeat='no-repeat'):
    s['background_background'] = 'classic'
    s['background_image'] = media(name)
    s['background_size'] = size
    s['background_position'] = pos
    s['background_repeat'] = repeat
    return s


# ---------------------------------------------------------------- design patterns
def photo(name, radius, place, z=None):
    """Rounded photo card with the design's bottom gradient, shadow and hairline (pv-photo)."""
    c = con(abs_=place['pos'], width=place['w'], minh=place['h'], radius=radius, cls='pv-photo', z=z,
            extra={**shadow(0, 28, 56, -18, 'rgba(31,95,153,.55)'),
                   'background_overlay_background': 'gradient',
                   'background_overlay_color': 'rgba(11,46,79,0)',
                   'background_overlay_color_stop': {'unit': '%', 'size': 50, 'sizes': []},
                   'background_overlay_color_b': 'rgba(11,46,79,.42)',
                   'background_overlay_color_b_stop': {'unit': '%', 'size': 100, 'sizes': []},
                   'background_overlay_gradient_type': 'linear',
                   'background_overlay_gradient_angle': {'unit': 'deg', 'size': 180, 'sizes': []}})
    bg_image(c['settings'], name)
    return c


def blob(col, dur, delay, place):
    cls = f'pv-blob pv-dur-{dur}' + (f' pv-delay-m{-delay}' if delay else '')
    return con(abs_=place['pos'], width=place['w'], minh=place['h'], bg=col, cls=cls)


def edge(prev_bg, svg, dur, top=True):
    c = con(minh='clamp(40px,5vw,72px)', bg=prev_bg, cls=f'pv-edge pv-dur-{dur}',
            margin=(0, 0, -2, 0) if top else (-2, 0, 0, 0), isinner=False)
    c['settings']['background_image'] = media(svg)
    c['settings']['background_repeat'] = 'repeat-x'
    return c


def lines(colname, dur, w, h, variant, margin=None, opacity=None, cls=''):
    c = con(width=w, minh=h, cls=f'pv-lines pv-lines--{variant} pv-dur-{dur} {cls}'.strip(), margin=margin,
            extra={'_flex_size': 'none'})
    c['settings']['background_background'] = 'classic'
    c['settings']['background_image'] = media(f'pv-lines-{colname}')
    c['settings']['background_repeat'] = 'repeat-x'
    if opacity is not None:
        c['settings']['css_classes'] += f' pv-op-{int(round(opacity * 100))}'
    return c


def pill(text_, fg, bg, size=12, ls=0.08, pad=(6, 12), weight=600):
    return heading(text_, size, weight, 1.5, ls, fg, tag='span', transform='uppercase',
                   bg=bg, radius=999, pad=pad, width='auto', align_self='flex-start')
