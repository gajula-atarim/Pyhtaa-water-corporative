"""Build Elementor JSON for the Pyhtää Water Cooperative header, footer and home page.

Source of truth: "Home Page v4.dc.html" from the design zip. Font sizes, spacing,
colours and breakpoints are copied from it; the design's CSS grid
`repeat(auto-fit, minmax(min(100%, Xpx), 1fr))` is reproduced with wrapping flex
rows whose children have width X and flex-grow 1, so columns stack at the same
widths as the design without per-breakpoint overrides.

Usage: python3 build.py media.json  -> writes ../data/*.json
"""
import json
import os
import sys

import el
from el import (button, blob, con, edge, heading, icon, image, lines, photo, pill, text, widget, common,
                shadow, dims, unit, color, typo, svg_icon)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data')

PAGES = {}  # title -> url


def url(title):
    return PAGES[title]


TEL_PM = 'tel:+358413298271'
TEL_SEC = 'tel:+358503308896'
MAIL = 'mailto:pyhtaanvok@gmail.com'
PDF = 'https://pyhtaanvok.fi/wp-content/uploads/sites/1503/2026/11/Yhteystiedot.pdf'

SKY_BTN = dict(fg='#0B2E4F', bg='#5FA8D3', hfg='#FFFFFF', hbg='#1F5F99')
COL2 = lambda basis, *kids, **kw: con(*kids, width=basis, grow=1, **kw)  # auto-fit grid column


# ============================================================== HOME
def hero():
    left = COL2(420,
        heading('Business ID: Y 2605405-8', 14, 400, 1.5, col='#4A5966', tag='span'),
        heading('Pyhtää Water Cooperative', 'clamp(40px,5.6vw,68px)', 600, 1.05, -0.02, '#0B2E4F', tag='h1'),
        heading('Home page of Pyhtää Water Cooperative', 19, 400, 1.5, col='#3A4854', tag='p'),
        con(button('Water quality results', url('Water quality results'), fg='#14202B', bg='#F2B53A', hfg='#FFFFFF', hbg='#0B2E4F', pad=(14, 26)),
            button('Price list', url('Price list'), fg='#0B2E4F', hfg='#0B2E4F', pad=(14, 8), cls='pv-link-btn'),
            d='row', gap_=12, wrap=True),
        lines('yellow', 5, 'min(100%,380px)', 44, 'hero', margin=(12, 0, 0, 0)),
        gap_=22)
    right = COL2(420,
        blob('#5FA8D3', 12, 0, {'pos': {'right': '-6%', 'top': '-6%'}, 'w': '58%', 'h': '58%'}),
        photo('hero-lake', 28, {'pos': {'right': 0, 'top': 0}, 'w': '78%', 'h': '64%'}),
        photo('hero-tap', 24, {'pos': {'left': 0, 'bottom': 0}, 'w': '56%', 'h': '46%'}),
        minh='clamp(380px,46vw,540px)')
    return con(con(left, right, d='row', wrap=True, gap_=48, align='center'),
               boxed=1136, pad=('clamp(40px,6vw,80px)', 32, 'clamp(48px,6vw,80px)', 32), tag='section', isinner=False,
               extra={'_element_id': 'hero'})


def statement():
    return con(
        image('pv-sun-drop', 180, align='center'),
        heading('Water Testing Results Are Available', 'clamp(28px,3.6vw,40px)', 600, 1.25, -0.015, '#14202B', align='center'),
        text(f'<p>The water testing results have arrived and can be found <a href="{url("Water quality results")}" style="font-weight:600">here</a>.</p>', 17, 1.6, '#3A4854', align='center'),
        button('Water quality results', url('Water quality results'), ls=0.06, pad=(16, 36), radius=2, align='center', cls='pv-lift', **SKY_BTN),
        boxed=836, gap_=24, align='center', tag='section', cls='pv-reveal', isinner=False,
        pad=('clamp(40px,6vw,72px)', 32, 'clamp(64px,8vw,104px)', 32))


QUICK = [('Water quality results', 'pv-icon-drop'), ('Price list', 'pv-icon-euro'),
         ('Meter readings', 'pv-icon-meter'), ('Contact', 'pv-icon-phone')]


def quick_card(title, ic):
    drop = con(icon(ic, 50, '#0B2E4F'), width=100, minh=100, bg='rgba(255,255,255,.5)',
               radius=('50%', 0, '50%', '50%'), justify='center', align='center', cls='pv-teardrop pv-quick__drop',
               margin=(14, 0, 0, 0), extra={'_flex_size': 'none'})
    return con(drop,
               heading(title, 18, 600, 1.3, col='#14202B', tag='span', align='center'),
               lines('navy', 4, 96, 22, 'quick', cls='pv-quick__wave'),
               width=160, grow=1, link=url(title), pad=(28, 16, 24, 16), radius=24, gap_=14, align='center',
               cls='pv-quick')


def notice_band():
    visual = COL2(360,
        blob('#5FA8D3', 14, -4, {'pos': {'left': '-6%', 'bottom': '-6%'}, 'w': '70%', 'h': '64%'}),
        photo('water-meter', 28, {'pos': {'left': 0, 'top': 0}, 'w': '94%', 'h': '100%'}),
        minh=340)
    copy = COL2(360,
        con(heading('Announcement', 12, 600, 1.5, 0.08, '#FFFFFF', tag='span', transform='uppercase',
                    bg='#14202B', radius=999, pad=(6, 12), width='auto'),
            heading('August 14, 2026', 14, 500, 1.5, col='#14202B', tag='span', width='auto'),
            d='row', gap_=12, align='center', wrap=True),
        heading('Due to increased costs, the Board of Directors decided at its meeting on August 12, 2026, to increase prices!',
                'clamp(24px,2.8vw,32px)', 600, 1.25, -0.01, '#14202B', cls='pv-pretty'),
        text('<p>The updated price list can be found on the dedicated tab.</p>', 16, 1.6, '#14202B'),
        text('<p>An SMS notification will also be sent to all shareholders whose contact details are available with the secretary.</p>', 16, 1.6, '#14202B'),
        button('Updated price list', url('Price list'), size=14, fg='#FFFFFF', bg='#14202B', hfg='#FFFFFF', hbg='#0B2E4F', pad=(14, 24)),
        gap_=18)
    quick = con(*[quick_card(t, i) for t, i in QUICK], d='row', wrap=True, gap_=16,
                pad=('clamp(8px,2vw,16px)', 0, 0, 0), cls='pv-quick-group pv-stagger')
    inner = con(con(visual, copy, d='row', wrap=True, gap_='clamp(32px,5vw,56px)', align='center'),
                quick, boxed=1136, gap_='clamp(32px,5vw,56px)', pad=('clamp(32px,5vw,64px)', 32), cls='pv-reveal')
    return con(edge('#F7F6F2', 'pv-edge-yellow-0', 28, top=True), inner,
               edge('#F2B53A', 'pv-edge-cream-8', 34, top=False),
               bg='#F2B53A', tag='section', isinner=False, extra={'_element_id': 'notice'})


def step(n, t):
    circle = con(heading(n, 16, 600, 1, col='#1F5F99', tag='span', align='center'),
                 width=40, minh=40, bg='#E8F1F7', radius=999, justify='center', align='center',
                 extra={'_flex_size': 'none'})
    return con(circle, text(f'<p>{t}</p>', 16, 1.6, '#3A4854', pad=(7, 0, 0, 0), grow=1),
               d='row', gap_=14, align='flex-start')


def meter_readings():
    left = COL2(420,
        heading('Meter Readings and Contact Information', 'clamp(28px,3.4vw,40px)', 600, 1.15, -0.015, '#0B2E4F'),
        con(step('1', 'Please submit your water meter readings to the secretary in June.'),
            step('2', 'Readings from remote-reading meters do not need to be submitted manually.'),
            step('3', 'Please refer to the pictures under the Meter Readings tab for instructions.'), gap_=14),
        button('Meter readings', url('Meter readings'), size=14, pad=(14, 24), **SKY_BTN),
        lines('blue', 6, 'min(100%,300px)', 40, 'md'),
        gap_=22)
    right = COL2(420,
        blob('#F2B53A', 13, -7, {'pos': {'left': '-4%', 'bottom': '-6%'}, 'w': '64%', 'h': '70%'}),
        photo('member-home', 28, {'pos': {'right': 0, 'top': 0}, 'w': '90%', 'h': '94%'}),
        minh='clamp(340px,40vw,500px)')
    return con(con(left, right, d='row', wrap=True, gap_='clamp(40px,6vw,80px)', align='center'),
               boxed=1136, pad=('clamp(64px,8vw,112px)', 32), tag='section', cls='pv-reveal', isinner=False)


def article(title, body):
    return con(heading(title, 20, 600, 1.5, col='#FFFFFF', tag='h3'),
               text(body, 15, 1.65, '#D6E8F4'), gap_=8, tag='article')


def announcements():
    left = COL2(420,
        article('The Water Cooperative Is Switching to E-Invoicing',
                '<p>Please remember to subscribe to e-invoices! By doing so, you can avoid the €5 additional fee charged for paper invoices. Instructions for subscribing to e-invoices can be found on the reverse side of your previous invoice. If you would like to receive invoices by post (with an additional €5 fee), please contact the secretary.</p>'),
        article('The Cooperative Has Replaced Mechanical Water Meters with Remote-Reading Meters',
                '<p>A few shareholders could not be reached, so their meters will be replaced at a later date. Meters were replaced where they were located in heated spaces to avoid any risk of freezing.</p>'),
        article('Information About the New Property Manager',
                f'<p>Please be informed that the Water Cooperative has appointed a new property manager. Matti Härkänen, phone: <a href="{TEL_PM}" style="color:#ffffff;font-weight:600">041 329 8271</a>.</p>'),
        gap_=32)
    badge = con(heading('€2', 30, 600, 1, col='#0B2E4F', tag='span', align='center'),
                heading('per e-invoice', 12, 500, 1.3, col='#0B2E4F', tag='span', align='center', margin=(4, 0, 0, 0)),
                abs_={'right': 0, 'bottom': -24}, width=132, minh=132, bg='#5FA8D3', radius=999, justify='center',
                align='center', z=2,
                extra={'border_border': 'solid', 'border_width': dims(4), 'border_color': '#FFFFFF',
                       **shadow(0, 12, 28, 0, 'rgba(0,0,0,.25)')})
    right = COL2(420,
        blob('#F2B53A', 15, -2, {'pos': {'right': '-6%', 'top': '-6%'}, 'w': '46%', 'h': '42%'}),
        photo('billing', 8, {'pos': {'left': '4%', 'top': 0}, 'w': '92%', 'h': '100%'}),
        badge, minh='clamp(360px,40vw,500px)')
    inner = con(con(left, right, d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center', cls='pv-reveal'),
                boxed=1136, gap_=40, pad=('clamp(32px,5vw,64px)', 32))
    return con(edge('#F7F6F2', 'pv-edge-navy-m6', 30), inner, edge('#0B2E4F', 'pv-edge-cream-6', 26, top=False),
               bg='#0B2E4F', tag='section', isinner=False, extra={'_element_id': 'news'})


def price_card(dark):
    if dark:
        return con(
            blob('#1F5F99', 12, -2, {'pos': {'right': -36, 'top': -36}, 'w': 150, 'h': 150}),
            pill('Avoid the €5 additional fee', '#14202B', '#F2B53A', ls=0.06),
            heading('E-invoice', 16, 500, 1.5, col='#A9D1EA', tag='span', margin=(12, 0, 0, 0)),
            heading('€2', 'clamp(56px,6vw,76px)', 600, 1, -0.03, '#FFFFFF', tag='span'),
            heading('per e-invoice', 14, 400, 1.5, col='#D6E8F4', tag='span'),
            width=220, grow=1, bg='#0B2E4F', radius=32, pad=(32, 28), gap_=14, overflow='hidden',
            extra=shadow(0, 28, 56, -20, 'rgba(11,46,79,.6)'))
    return con(
        pill('€5 additional fee', '#4A5966', '#E8F1F7', ls=0.06),
        heading('Paper invoice by post', 16, 500, 1.5, col='#4A5966', tag='span', margin=(12, 0, 0, 0)),
        heading('€5', 'clamp(56px,6vw,76px)', 600, 1, -0.03, '#4A5966', tag='span'),
        heading('per paper invoice. If you would like to receive invoices by post, please contact the secretary.', 14, 400, 1.5, col='#4A5966', tag='span'),
        width=220, grow=1, bg='#FFFFFF', radius=32, pad=(32, 28), gap_=14,
        extra={'border_border': 'dashed', 'border_width': dims(2), 'border_color': '#C9D6E0'})


def fact(title, body):
    return con(heading(title, 'clamp(22px,2.4vw,28px)', 600, 1.15, -0.01, '#1F5F99', tag='span'),
               heading(body, 14, 400, 1.5, col='#3A4854', tag='span'),
               width=240, grow=1, gap_=6, pad=(22, 24), radius=24, bg='#FFFFFF',
               extra=shadow(0, 16, 36, -22, 'rgba(11,46,79,.35)'))


def billing():
    left = COL2(440,
        heading('Billing', 13, 600, 1.5, 0.08, '#1F5F99', tag='span', transform='uppercase'),
        heading('Please remember to subscribe to e-invoices!', 'clamp(30px,3.8vw,44px)', 600, 1.12, -0.015, '#0B2E4F'),
        text('<p>Invoices sent by email are generated through the billing software, so please remember to check your spam folder. If you have any questions or concerns regarding your invoices, please contact the secretary.</p>', 16, 1.7, '#3A4854'),
        text('<p>Instructions for subscribing to e-invoices can be found on the reverse side of your previous invoice.</p>', 16, 1.7, '#3A4854'),
        con(button('Price list', url('Price list'), size=14, pad=(14, 24), **SKY_BTN),
            button('Contact the secretary', TEL_SEC, size=14, fg='#0B2E4F', hfg='#0B2E4F', pad=(14, 8), cls='pv-link-btn'),
            d='row', wrap=True, gap_=12, margin=(4, 0, 0, 0)),
        lines('sky', 6, 'min(100%,300px)', 40, 'md', margin=(4, 0, 0, 0)),
        gap_=20)
    right = COL2(440, price_card(True), price_card(False), d='row', wrap=True, gap_=16, align='stretch', cls='pv-stagger')
    row1 = con(left, right, d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center', cls='pv-reveal')
    row2 = con(fact('12 or 4 times per year', 'The billing frequency will remain unchanged'),
               fact('Twice a year', 'Billing takes place twice a year or according to the agreed arrangement.'),
               fact('Actual readings', 'For customers with remote-reading meters, invoices are always based on actual meter readings.'),
               d='row', wrap=True, gap_=16, cls='pv-stagger')
    return con(row1, row2, boxed=1136, pad=('clamp(64px,8vw,112px)', 32), gap_='clamp(32px,4vw,48px)', tag='section',
               isinner=False, extra={'_element_id': 'billing'})


def contact_details():
    visual = COL2(420,
        blob('#5FA8D3', 14, -3, {'pos': {'left': '-6%', 'top': '-6%'}, 'w': '46%', 'h': '42%'}),
        photo('cabin-lake', 28, {'pos': {'left': '4%', 'top': 0}, 'w': '92%', 'h': '100%'}),
        minh='clamp(360px,40vw,500px)')
    copy = COL2(420,
        heading('Meter Readings and Contact Information', 13, 600, 1.5, 0.08, '#1F5F99', tag='span', transform='uppercase'),
        heading('We kindly ask you to provide the Cooperative with your mobile phone number so that we can send you notifications in exceptional situations when necessary (no other messages will be sent).',
                'clamp(22px,2.6vw,30px)', 600, 1.35, -0.01, '#0B2E4F', cls='pv-pretty'),
        text('<p>We also request your email address, if you have one.</p>', 16, 1.7, '#3A4854'),
        con(heading('Data Protection', 15, 600, 1.5, col='#0B2E4F', tag='span'),
            text(f'<p>For matters relating to data protection, you can contact us at: <a href="{MAIL}" style="font-weight:600">pyhtaanvok(at)gmail.com</a></p>', 16, 1.7, '#3A4854'),
            gap_=6, pad=(16, 0, 0, 0),
            extra={'border_border': 'solid', 'border_width': {'unit': 'px', 'top': '1', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': False}, 'border_color': '#C9D6E0'}),
        lines('sky', 7, 'min(100%,300px)', 40, 'md', margin=(8, 0, 0, 0)),
        gap_=20)
    inner = con(con(visual, copy, d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center'),
                boxed=1136, pad=('clamp(32px,5vw,64px)', 32), cls='pv-reveal')
    return con(edge('#F7F6F2', 'pv-edge-mist-4', 30), inner, edge('#E8F1F7', 'pv-edge-cream-m4', 27, top=False),
               bg='#E8F1F7', tag='section', isinner=False, extra={'_element_id': 'details'})


def contact_card(dark):
    if dark:
        ini, ini_bg, role, role_fg, role_bg, sub, sub_col, name, fg, lc, ldur, num, cbg, cfg, tel, sh = (
            'MH', '#F2B53A', 'Property Manager', '#D6E8F4', 'rgba(255,255,255,.12)',
            'Fault Reports, New Water Connections and Emergency Assistance', '#A9D1EA',
            'Property Manager: Matti Härkänen', '#FFFFFF', 'sky', 6, '041 329 8271', '#F2B53A', '#14202B', TEL_PM,
            'rgba(11,46,79,.55)')
        bg = '#0B2E4F'
    else:
        ini, ini_bg, role, role_fg, role_bg, sub, sub_col, name, fg, lc, ldur, num, cbg, cfg, tel, sh = (
            'MS', '#5FA8D3', 'Secretary', '#1F5F99', '#E8F1F7',
            'Billing, Change of Address and Other Enquiries/Notifications', '#4A5966',
            'Secretary: Mona Sissi', '#0B2E4F', 'yellow', 7, '050 330 8896', '#1F5F99', '#FFFFFF', TEL_SEC,
            'rgba(11,46,79,.25)')
        bg = '#FFFFFF'
    top = con(con(heading(ini, 18, 600, 1, col='#0B2E4F', tag='span', align='center'),
                  width=64, minh=64, bg=ini_bg, radius=('50%', 0, '50%', '50%'), justify='center', align='center',
                  cls='pv-teardrop', extra={'_flex_size': 'none'}),
              heading(role, 12, 600, 1.5, 0.08, role_fg, tag='span', transform='uppercase', bg=role_bg, radius=999,
                      pad=(7, 14), width='auto'),
              d='row', justify='space-between', align='center', gap_=12)
    mid = con(heading(sub, 15, 400, 1.5, col=sub_col, tag='span'),
              heading(name, 'clamp(22px,2.4vw,26px)', 600, 1.5, -0.01, fg, tag='span'), gap_=6)
    bottom = con(heading(num, 'clamp(26px,3vw,34px)', 600, 1.5, -0.01, fg, tag='span', cls='pv-nowrap'),
                 con(icon('pv-icon-phone-line', 26, cfg), width=56, minh=56, bg=cbg, radius=999, justify='center',
                     align='center', extra={'_flex_size': 'none'}),
                 d='row', justify='space-between', align='center', gap_=16, margin=('auto', 0, 0, 0))
    return con(top, mid, lines(lc, ldur, 160, 30, 'card', opacity=.8), bottom,
               width=360, grow=1, link=tel, bg=bg, radius=32, pad='clamp(24px,3vw,36px)', gap_=28, overflow='hidden',
               cls='pv-contact-card', extra=shadow(0, 24, 48, -20, sh))


def contact():
    chip = lambda label, href: button(label, href, size=15, ls=0, transform='none', fg='#0B2E4F', bg='#E8F1F7',
                                      hfg='#0B2E4F', hbg='#D6E8F4', pad=(12, 20), radius=999)
    return con(
        image('pv-sun-drop', 180, align='center'),
        heading('Contact', 'clamp(28px,3.4vw,40px)', 600, 1.5, -0.015, '#0B2E4F', align='center'),
        con(contact_card(True), contact_card(False), d='row', wrap=True, gap_=20),
        con(chip('Other contact details (PDF) ↓', PDF), chip('pyhtaanvok@gmail.com →', MAIL),
            d='row', wrap=True, gap_=12, justify='center'),
        boxed=936, pad=('clamp(64px,8vw,112px)', 32), gap_=28, align='center', tag='section', cls='pv-reveal',
        isinner=False, extra={'_element_id': 'contact'})


def home():
    el.set_seed('home')
    return [hero(), statement(), notice_band(), meter_readings(), announcements(), billing(), contact_details(), contact()]


# ============================================================== HEADER
def site_logo(img, size):
    """UAE Site Logo widget with a custom image."""
    s = {'site_logo_fallback': 'yes', 'custom_image': el.media(img), 'site_logo_size_size': 'full',
         'width': unit(size), 'align': 'left', 'link_to': 'default'}
    return widget('site-logo', s)


def header():
    el.set_seed('header')
    logo = con(site_logo('pv-logo-drop', 42),
               con(heading('Pyhtään', 19, 600, 1, -0.01, '#FFFFFF', tag='span', link=el.SITE + '/'),
                   heading('vesiosuuskunta', 14, 400, 1, col='#D6E8F4', tag='span', link=el.SITE + '/', margin=(3, 0, 0, 0))),
               d='row', gap_=10, align='center', cls='pv-logo', extra={'_flex_size': 'none'})
    phone = button('041 329 8271', TEL_PM, size=15, ls=0, transform='none', fg='#14202B', bg='#F2B53A', hfg='#0B2E4F',
                   hbg='#FFFFFF', pad=(5, 18, 5, 5), radius=999, icon=svg_icon('pv-icon-phone-solid'), cls='pv-phone-pill')
    phone['settings']['button_css_id'] = ''
    phone['settings']['link']['custom_attributes'] = 'aria-label|Fault reports: call 041 329 8271'
    menu_btn = button('Menu', '#menu', size=15, ls=0, transform='none', fg='#0B2E4F', bg='#FFFFFF', hfg='#0B2E4F',
                      hbg='#E8F1F7', pad=(7, 8, 7, 20), radius=999, cls='pv-menu-toggle')
    nav = con(phone, menu_btn, d='row', gap_=8, align='center', tag='nav', extra={'_flex_size': 'none'})
    pill_ = con(logo, nav, d='row', justify='space-between', align='center', wrap=True, gap_=(16, 32),
                bg='#1F5F99', radius=999, pad=(12, 12, 12, 22), cls='pv-header-pill', boxed=None, width='min(100%,1136px)',
                extra=shadow(0, 14, 34, 0, 'rgba(11,46,79,.22)'))

    # ---- drawer
    dlogo = con(site_logo('pv-logo-drop', 38),
                con(heading('Pyhtään', 17, 600, 1, col='#FFFFFF', tag='span'),
                    heading('vesiosuuskunta', 13, 400, 1, col='#D6E8F4', tag='span', margin=(3, 0, 0, 0))),
                d='row', gap_=10, align='center')
    close = button('×', '#close', size=22, weight=400, ls=0, transform='none', fg='#FFFFFF', hfg='#1F5F99',
                   hbg='#FFFFFF', pad=(0, 0), radius=999, cls='pv-menu-close',
                   )
    close['settings'].update({'border_border': 'solid', 'border_width': dims(2), 'border_color': 'rgba(255,255,255,.6)',
                              'typography_line_height': {'unit': 'px', 'size': 44, 'sizes': []}})
    close['settings']['_element_width'] = 'initial'
    close['settings']['_element_custom_width'] = unit(48)
    nav_menu = widget('navigation-menu', {
        'menu': 'main-menu', 'layout': 'vertical', 'navmenu_align': 'left', 'dropdown': 'none', 'submenu_icon': 'arrow',
        'pointer': 'none', 'padding_horizontal_menu_item': unit(4), 'padding_vertical_menu_item': unit(15),
        'menu_space_between': unit(0), 'menu_row_space': unit(0),
        **typo('menu_typography', 'clamp(15px,2.05vh,21px)', 500, 1.5),
        'color_menu_item': '#FFFFFF', 'color_menu_item_hover': '#F2B53A', 'color_menu_item_active': '#FFFFFF',
        '_css_classes': 'pv-drawer-nav'})
    def dcard(sub, name, num, href, bg, fg, subcol, hbg):
        c = con(con(heading(sub, 13, 400, 1.5, col=subcol, tag='span', cls='pv-drawer-desc'),
                    heading(name, 15, 600, 1.5, col=fg, tag='span'), grow=1, width=0),
                heading(num, 17, 600, 1.5, col=fg, tag='span', cls='pv-nowrap', width='auto'),
                d='row', justify='space-between', align='center', gap_=12, link=href, bg=bg, radius=20,
                pad=('clamp(8px,1.4vh,14px)', 18), cls='pv-drawer-card')
        c['settings'].update({'background_hover_background': 'classic', 'background_hover_color': hbg})
        return c
    contacts = con(dcard('Fault Reports, New Water Connections and Emergency Assistance', 'Property Manager: Matti Härkänen',
                         '041 329 8271', TEL_PM, '#F2B53A', '#14202B', '#14202B', '#FFFFFF'),
                   dcard('Billing, Change of Address and Other Enquiries/Notifications', 'Secretary: Mona Sissi',
                         '050 330 8896', TEL_SEC, 'rgba(255,255,255,.12)', '#FFFFFF', '#D6E8F4', 'rgba(255,255,255,.22)'),
                   gap_=10)
    # flexible spacer between the menu and the contact cards; the wavy lines sit in the middle of the free space
    waves = con(lines('yellow', 6, 200, 34, 'drawer', opacity=.7, cls='pv-drawer-lines'),
                justify='center', align='center', minh=0, overflow='hidden', cls='pv-drawer-spacer',
                extra={'_flex_size': 'custom', '_flex_grow': 1, '_flex_shrink': 1})
    drawer = con(con(dlogo, close, d='row', justify='space-between', align='center', gap_=12),
                 nav_menu, waves, contacts,
                 bg='#1F5F99', radius=(28, 0, 0, 28),
                 pad=('clamp(12px,2vh,20px)', 'clamp(20px,4vw,32px)', 'clamp(12px,2.8vh,28px)', 'clamp(20px,4vw,32px)'),
                 gap_='clamp(8px,2.8vh,28px)', cls='pv-drawer', tag='aside', extra=shadow(-20, 0, 60, 0, 'rgba(11,46,79,.35)'))
    overlay = con(bg='rgba(11,46,79,.5)', cls='pv-overlay')
    root = con(pill_, overlay, drawer, pad=(14, 32, 0, 32), align='center', tag='div', isinner=False, cls='pv-header')
    return [root]


# ============================================================== FOOTER
def footer():
    el.set_seed('footer')
    logo = con(site_logo('pv-logo-drop-footer', 52),
               con(heading('Pyhtään', 24, 600, 1, -0.01, '#FFFFFF', tag='span', link=el.SITE + '/'),
                   heading('vesiosuuskunta', 16, 400, 1, col='#A9D1EA', tag='span', link=el.SITE + '/', margin=(4, 0, 0, 0))),
               d='row', gap_=14, align='center')
    info = widget('icon-list', {
        'icon_list': [
            {'_id': 'a1', 'text': 'Ritvalanpolku 22 (c/o Sissi)<br>49240 Purola', 'selected_icon': svg_icon('pv-icon-pin')},
            {'_id': 'a2', 'text': 'pyhtaanvok@gmail.com', 'selected_icon': svg_icon('pv-icon-mail'),
             'link': {'url': MAIL, 'is_external': '', 'nofollow': ''}},
        ],
        'space_between': unit(12), 'icon_size': unit(18), 'text_indent': unit(10), 'icon_self_align': 'left',
        'icon_self_vertical_align': 'flex-start', 'icon_vertical_offset': unit(2),
        'icon_color': '#5FA8D3', 'text_color': '#D6E8F4', 'text_color_hover': '#F2B53A',
        **typo('icon_typography', 15, 400, 1.5), '_css_classes': 'pv-footer-info'})
    color(info['settings'], 'icon_color', '#5FA8D3')
    color(info['settings'], 'text_color', '#D6E8F4')
    left = con(logo, lines('yellow', 6, 'min(100%,220px)', 32, 'foot', opacity=.85),
               con(info, heading('Business ID: Y 2605405-8', 14, 400, 1.5, col='#A9D1EA', tag='span'), gap_=12),
               width=280, grow=1, gap_=22)
    nav = widget('navigation-menu', {
        'menu': 'main-menu', 'layout': 'vertical', 'navmenu_align': 'left', 'dropdown': 'none', 'pointer': 'none',
        'padding_horizontal_menu_item': unit(0), 'padding_vertical_menu_item': unit(13),
        'menu_space_between': unit(0), 'menu_row_space': unit(0),
        **typo('menu_typography', 16, 500, 1.5),
        'color_menu_item': '#FFFFFF', 'color_menu_item_hover': '#F2B53A', 'color_menu_item_active': '#FFFFFF',
        '_css_classes': 'pv-footer-nav'})
    right = con(nav, width=480, grow=2, tag='nav')
    main = con(con(left, right, d='row', wrap=True, gap_=(40, 'clamp(32px,5vw,72px)'), align='flex-start'),
               boxed=1136, pad=('clamp(16px,2vw,24px)', 32, 'clamp(40px,5vw,64px)', 32))
    copyright_ = widget('copyright', {'shortcode': 'Copyright © [hfe_current_year] · Pyhtään vesiosuuskunta',
                                      'align': 'left', '_css_classes': 'pv-copyright', '_element_width': 'auto',
                                      'text_color': '#A9D1EA', **typo('caption_typography', 14, 400, 1.5)})
    login = button('Log in', 'https://pyhtaanvok.fi-c.seravo.com/wp-admin/', size=14, weight=400, ls=0, transform='none',
                   fg='#A9D1EA', hfg='#FFFFFF', hbg='#123C63', pad=(8, 14), radius=999)
    top = button('Top of Page ↑', '#top', size=14, ls=0, transform='none', fg='#14202B', bg='#F2B53A', hfg='#14202B',
                 hbg='#F2B53A', pad=(8, 16), radius=999, cls='pv-top-btn')
    bar = con(con(copyright_, con(login, top, d='row', gap_=10, align='center'),
                  d='row', wrap=True, justify='space-between', align='center', gap_=12),
              boxed=1136, pad=(16, 32), bg='#082440')
    float_top = button('', '#top', size=15, ls=0, transform='none', fg='#FFFFFF', bg='#1F5F99', hfg='#14202B', hbg='#F2B53A',
                       pad=(15, 15), radius=999, icon=svg_icon('pv-icon-arrow-up'), cls='pv-totop-float')
    float_top['settings']['link']['custom_attributes'] = 'aria-label|Scroll to top,title|Scroll to top'
    float_top['settings'].update(shadow(0, 12, 28, -8, 'rgba(11,46,79,.5)'))
    float_top['settings']['button_box_shadow_box_shadow_type'] = 'yes'
    float_top['settings']['button_box_shadow_box_shadow'] = float_top['settings'].pop('box_shadow_box_shadow')
    float_top['settings'].pop('box_shadow_box_shadow_type')
    root = con(edge('#F7F6F2', 'pv-edge-navy-0', 32), main, bar, float_top, bg='#0B2E4F', overflow='hidden',
               tag='div', isinner=False, cls='pv-footer')
    return [root]


def auto_widths(elements, parent_row=False):
    """Nested containers default to 100% width; inside a row they must size to their content."""
    for e in elements:
        if e['elType'] == 'container':
            st = e['settings']
            if parent_row and 'width' not in st and st.get('position') != 'absolute':
                st['width'] = unit('auto')
            # Elementor wraps every container on mobile by default; only the design's auto-fit rows may wrap
            wrap = st.get('flex_wrap', 'nowrap')
            st.setdefault('flex_wrap', wrap)
            st.setdefault('flex_wrap_tablet', wrap)
            st.setdefault('flex_wrap_mobile', wrap)
            if 'width' in st:  # Elementor defaults tablet/mobile container width to 100%; keep the design's sizing
                st.setdefault('width_tablet', st['width'])
                st.setdefault('width_mobile', st['width'])
            auto_widths(e['elements'], st.get('flex_direction') == 'row')
    return elements


def main():
    data = json.load(open(sys.argv[1]))
    el.MEDIA.update({k: tuple(v) for k, v in data['media'].items() if isinstance(v, list)})
    PAGES.update({k: v[1] for k, v in data['pages'].items()})
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (('home', home), ('header', header), ('footer', footer)):
        json.dump(auto_widths(fn()), open(os.path.join(OUT, f'{name}.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
        print(name, os.path.getsize(os.path.join(OUT, f'{name}.json')))


if __name__ == '__main__':
    main()
