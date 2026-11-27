"""Inner pages of the Pyhtää Water Cooperative site, as editable Elementor containers and widgets.

Source of truth: the page designs in the design zip (Price List, Contact, Board Pages, Pump
Maintenance, Water Information, Shareholders, Water Quality Results), translated to Finnish.
They reuse the home page building blocks (build.py / el.py): the same header and footer
templates, the contact section, wave edges, blobs, drifting lines and scroll-reveal classes.
Inner-page links stay '#' placeholders (same rule as the home page); document links point to
the cooperative's existing files on pyhtaanvok.fi.

Usage: python3 pages.py ../data/site.json  -> writes ../data/page-<slug>.json
"""
import json
import os
import re
import sys

import el
import build
from build import COL2, SKY_BTN, contact, step, _m, _t, url, auto_widths
from el import (button, blob, con, edge, heading, icon, image, lines, photo, pill, text, shadow, dims, unit, gap,
                svg_icon, bg_image)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data')
UP = 'https://pyhtaanvok.fi/wp-content/uploads/sites/1503/'

NAVY, BLUE, SKY, SUN, INK, MIST, CREAM, GREY, TXT = ('#0B2E4F', '#1F5F99', '#5FA8D3', '#F2B53A', '#14202B',
                                                      '#E8F1F7', '#F7F6F2', '#4A5966', '#3A4854')
H1 = 'clamp(40px,5.4vw,76px)'
H2 = 'clamp(28px,3.4vw,40px)'
H2_BIG = 'clamp(30px,3.8vw,50px)'
CARD_SHADOW = shadow(0, 16, 36, -22, 'rgba(11,46,79,.35)')
FI_MONTH = ['tammi', 'helmi', 'maalis', 'huhti', 'touko', 'kesä', 'heinä', 'elo', 'syys', 'loka', 'marras', 'joulu']


# ------------------------------------------------------------------ shared blocks
def white_card(*kids, width=None, grow=None, pad=(26, 24), radius=24, gap_=12, **kw):
    return con(*kids, bg='#FFFFFF', radius=radius, pad=pad, gap_=gap_, width=width, grow=grow,
               extra={**CARD_SHADOW, **kw.pop('extra', {})}, **kw)


def drop_icon(name, bg, col, size=44, isz=20):
    """Teardrop badge with an icon (same shape as the quick links)."""
    return con(icon(name, isz, col), width=size, minh=size, bg=bg, radius=('50%', 0, '50%', '50%'),
               justify='center', align='center', cls='pv-teardrop pv-icon-circle', extra={'_flex_size': 'none'})


def num_circle(n, bg=MIST, col=BLUE, size=36, fs=15):
    return con(heading(str(n), fs, 600, 1, col=col, tag='span', align='center'), width=size, minh=size, bg=bg,
               radius=999, justify='center', align='center', extra={'_flex_size': 'none'})


def arrow_circle(bg, col, size=34):
    return con(icon('pv-icon-arrow-ur', 16, col), width=size, minh=size, bg=bg, radius=999, justify='center',
               align='center', cls='pv-icon-circle', extra={'_flex_size': 'none'})


def chip(label, href, fg=NAVY, bg='#FFFFFF', hbg=MIST):
    return button(label, href, size=13, ls=0, transform='none', fg=fg, bg=bg, hfg=NAVY, hbg=hbg, pad=(9, 16),
                  radius=999)


def eyebrow(t, col=BLUE, align=None):
    return heading(t, 13, 600, 1.5, 0.08, col, tag='span', transform='uppercase', align=align)


def crumb(current):
    return text(f'<p><a href="{url("Home")}">Pyhtään vesiosuuskunta</a> / {current}</p>', 14, 1.5, BLUE,
                cls='pv-crumb')


def sun_title(title, col=NAVY):
    return [image('pv-sun-drop', 150, align='center'),
            heading(title, H2, 600, 1.2, -0.015, col, align='center')]


def section(*kids, bg=None, boxed=1136, pad=('clamp(56px,7vw,96px)', 32), gap_='clamp(28px,4vw,44px)', sid=None,
            align=None, cls='pv-reveal', edges=None):
    inner = con(*kids, boxed=boxed, pad=pad, gap_=gap_, align=align, cls=cls, isinner=not edges)
    if not edges:
        inner['settings']['html_tag'] = 'section'
        if bg:
            inner['settings']['background_background'] = 'classic'
            el.color(inner['settings'], 'background_color', bg)
        if sid:
            inner['settings']['_element_id'] = sid
        return inner
    top, bottom = edges
    outer = con(*([top] if top else []), inner, *([bottom] if bottom else []), bg=bg, tag='section', isinner=False,
                extra={'_element_id': sid} if sid else None)
    return outer


def page_hero(current, title, extras, photo_name, title_size=H1, overlay=None):
    """Mist-blue page hero: breadcrumb, H1, extra widgets and wavy lines; photo + blob on the right."""
    left = COL2(420, crumb(current), heading(title, title_size, 600, 1.05, -0.02, NAVY, tag='h1'), *extras,
                lines('yellow', 5, 'min(100%,170px)', 28, 'md'), gap_=20)
    right = COL2(420,
                 blob(SKY, 12, 0, {'pos': {'right': '-4%', 'top': '-7%'}, 'w': '46%', 'h': '58%'}),
                 photo(photo_name, 28, {'pos': {'right': 0, 'top': 0}, 'w': '92%', 'h': '100%'}),
                 *(overlay or []),
                 minh='clamp(300px,30vw,420px)', extra={'min_height_mobile': unit(230)})
    inner = con(con(left, right, d='row', wrap=True, gap_=48, align='center'), boxed=1136,
                pad=('clamp(28px,4vw,56px)', 32, 'clamp(28px,3vw,40px)', 32))
    return con(inner, edge(MIST, 'pv-edge-cream-m4', 27, top=False), bg=MIST, tag='section', isinner=False,
               extra={'_element_id': 'sivun-alku'})


def photo_area(name, minh, blob_col=SUN, blob_place=None, radius=28):
    bp = blob_place or {'pos': {'left': '-5%', 'bottom': '-7%'}, 'w': '62%', 'h': '64%'}
    return COL2(380, blob(blob_col, 13, -4, bp),
                photo(name, radius, {'pos': {'right': 0, 'top': 0}, 'w': '94%', 'h': '94%'}),
                minh=minh, extra={'min_height_mobile': unit(240)})


def finnish_date(s):
    """'2 October 2026' -> '2.10.2026' (other strings are translated by WQ_TEXT)."""
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    m = re.fullmatch(r'(\d{1,2}) (\w+) (\d{4})', s.strip())
    if m and m.group(2).lower() in months:
        return f'{int(m.group(1))}.{months.index(m.group(2).lower()) + 1}.{m.group(3)}'
    return s


# ================================================================== HINNASTO
def price_list():
    el.set_seed('page-hinnasto')
    pdf = UP + '2026/08/Liittym%C3%A4-ja-palveluhinnasto-3-2026.pdf'
    pdf_card = con(drop_icon('pv-icon-euro', SUN, NAVY, 40, 18),
                   heading('Voimassa oleva liittymä- ja palveluhinnasto – 3-2026', 15, 600, 1.35, col=NAVY, tag='span',
                           grow=1),
                   con(icon('pv-icon-download', 16, '#FFFFFF'), width=30, minh=30, bg=BLUE, radius=999,
                       justify='center', align='center', cls='pv-icon-circle', extra={'_flex_size': 'none'}),
                   d='row', gap_=14, align='center', link=pdf, bg='#FFFFFF', radius=18, pad=(14, 16),
                   width='min(100%,440px)', cls='pv-link-card', extra=CARD_SHADOW)
    hero = page_hero('Hinnasto', 'Hinnasto', [pdf_card], 'pl-hero')

    resp = [('pv-icon-pipe', BLUE, '#FFFFFF',
             'Pyhtään vesiosuuskunta (PVOK) vastaa putki- ja laiteasennuksista liittymissopimuksen mukaiseen '
             'vastuurajaan asti.'),
            ('pv-icon-house', SUN, NAVY, 'Kiinteistön omistaja vastaa omista asennuksistaan, sekä uusista että vanhoista.'),
            ('pv-icon-pen', SKY, NAVY,
             'Jos PVOK on tehnyt asiakkaalle asennuksia liittymissopimuksessa määritellyn vastuurajan ulkopuolelle, '
             'PVOK vastaa asentajana myös niistä kohtuullisen ajan.')]
    cards = con(*[white_card(drop_icon(i, b, c), text(f'<p>{t}</p>', 15, 1.6, TXT), width=240, grow=1, gap_=18)
                  for i, b, c, t in resp], d='row', wrap=True, gap_=16, cls='pv-stagger')
    responsibility = section(heading('Kuka vastaa kustannuksista?', H2, 600, 1.2, -0.015, NAVY), cards,
                             sid='vastuu')

    def who(tag, tag_fg, tag_bg, title, body, ph, blob_col, reverse):
        copy = COL2(380, pill(tag, tag_fg, tag_bg),
                    heading(title, 'clamp(26px,3vw,38px)', 600, 1.2, -0.015, NAVY, tag='h3'),
                    text(f'<p>{body}</p>', 18, 1.6, TXT),
                    lines('blue' if not reverse else 'sky', 6, 'min(100%,200px)', 30, 'md'), gap_=16)
        vis = photo_area(ph, 'clamp(280px,28vw,360px)', blob_col)
        row = con(*((copy, vis) if reverse else (vis, copy)), d='row', wrap=True, gap_='clamp(32px,5vw,64px)',
                  align='center')
        if reverse:
            row['settings']['flex_direction_mobile'] = 'column-reverse'
        return row
    who_pays = section(*sun_title('Kuka maksaa?'),
                       who('PVOK', BLUE, MIST, 'Laite hajoaa iän vuoksi tai on viallinen',
                           'PVOK (vesiosuuskunta) maksaa korjaus- tai vaihtokustannukset.', 'pl-pvok', SUN, False),
                       who('Osakas', INK, '#FCE6B8', 'Laite hajoaa tai vaurioituu osakkaan toiminnan vuoksi',
                           'Kustannuksista vastaa osakas.', 'pl-shareholder', SUN, True),
                       sid='kuka-maksaa', gap_='clamp(40px,6vw,72px)')
    example = section(pill('Esimerkki', '#FFFFFF', INK),
                      heading('Pumppu tukkeutuu siivousliinasta tai muusta pumppuun joutuneesta vierasesineestä, '
                              'eikä pumppua ole koskaan puhdistettu. Tällaisessa tapauksessa kustannuksista vastaa '
                              'osakas.', 'clamp(20px,2.2vw,28px)', 500, 1.45, col=INK, tag='p', align='center',
                              cls='pv-balance'),
                      lines('navy', 6, 'min(100%,200px)', 30, 'md'),
                      bg=SUN, boxed=860, gap_=22, align='center', sid='esimerkki',
                      edges=(edge(CREAM, 'pv-edge-yellow-0', 28), edge(SUN, 'pv-edge-cream-8', 34, top=False)))
    return [hero, responsibility, who_pays, example, contact()]


# ================================================================== YHTEYSTIEDOT
def contact_page():
    el.set_seed('page-yhteystiedot')

    def person(role, name, num, tel, dark, email=None):
        fg = '#FFFFFF' if dark else NAVY
        btns = [button(num, tel, size=14, ls=0, transform='none', fg=INK if dark else '#FFFFFF',
                       bg=SUN if dark else BLUE, hfg=NAVY, hbg='#FFFFFF' if dark else MIST, pad=(9, 16), radius=999,
                       icon=svg_icon('pv-icon-phone-solid'))]
        if email:
            btns.append(button('Sähköposti', email, size=14, ls=0, transform='none', fg=NAVY, bg=MIST, hfg=NAVY,
                               hbg='#D6E8F4', pad=(9, 16), radius=999, icon=svg_icon('pv-icon-mail')))
        return con(eyebrow(role, SUN if dark else BLUE), heading(name, 22, 600, 1.3, col=fg, tag='span'),
                   con(*btns, d='row', wrap=True, gap_=8, margin=(6, 0, 0, 0)),
                   width=200, grow=1, bg=NAVY if dark else '#FFFFFF', radius=22, pad=(22, 20), gap_=8,
                   extra=CARD_SHADOW)
    people = con(person('Kiinteistönhoito', 'Matti Härkänen', '041 329 8271', build.TEL_PM, True),
                 person('Sihteeri', 'Mona Sissi', '050 330 8896', build.TEL_SEC, False, build.MAIL),
                 d='row', wrap=True, gap_=12, margin=(8, 0, 0, 0))
    info = con(heading('Pyhtään vesiosuuskunta', 14, 600, 1.4, 0.06, NAVY, tag='span', transform='uppercase'),
               heading('Y-tunnus 2605405-8', 13, 400, 1.5, col=GREY, tag='span'),
               el.widget('icon-list', {
                   'icon_list': [
                       {'_id': 'c1', 'text': 'pyhtaanvok(at)gmail.com', 'selected_icon': svg_icon('pv-icon-mail'),
                        'link': {'url': build.MAIL, 'is_external': '', 'nofollow': ''}},
                       {'_id': 'c2', 'text': 'Ritvalanpolku 22 (c/o Sissi)<br>49240 Purola',
                        'selected_icon': svg_icon('pv-icon-pin')}],
                   'space_between': unit(8), 'icon_size': unit(16), 'text_indent': unit(8),
                   'icon_self_vertical_align': 'flex-start', 'icon_color': BLUE, 'text_color': NAVY,
                   **el.typo('icon_typography', 14, 500, 1.45)}),
               abs_={'left': 0, 'bottom': -36}, width='min(100%,300px)', bg='#FFFFFF', radius=20, pad=(18, 20),
               gap_=6, z=3, cls='pv-float-card', extra=CARD_SHADOW)
    hero = page_hero('Yhteystiedot', 'Yhteystiedot', [people], 'ct-hero', overlay=[info])

    others = ['Hannu Rinne', 'Markku Teikari', 'Mauri Savolainen', 'Sampsa Halme', 'Hilkka Smids']
    member_rows = [con(num_circle(''.join(w[0] for w in n.split()), MIST, BLUE, 30, 11),
                       heading(n, 16, 600, 1.4, col=NAVY, tag='span'), d='row', gap_=10, align='center')
                   for n in others]
    board = section(
        con(heading('Hallitus', 'clamp(32px,4vw,56px)', 600, 1.1, -0.02, NAVY), lines('sky', 6, 160, 30, 'md'),
            d='row', justify='space-between', align='center', wrap=True, gap_=16),
        con(white_card(eyebrow('Puheenjohtaja'), heading('Erosi omasta pyynnöstään', 17, 400, 1.5, col=TXT, tag='span'),
                       width=240, grow=1),
            con(eyebrow('Varapuheenjohtaja', SUN), heading('Jane Salama', 24, 600, 1.3, col='#FFFFFF', tag='span'),
                con(button('050 330 3453', 'tel:+358503303453', size=14, ls=0, transform='none', fg=INK, bg=SUN,
                           hfg=NAVY, hbg='#FFFFFF', pad=(9, 16), radius=999, icon=svg_icon('pv-icon-phone-solid')),
                    button('Sähköposti', 'mailto:jane.salama@pakkipub.com', size=14, ls=0, transform='none', fg=NAVY,
                           bg='#FFFFFF', hfg=NAVY, hbg=MIST, pad=(9, 16), radius=999, icon=svg_icon('pv-icon-mail')),
                    d='row', wrap=True, gap_=8),
                heading('jane.salama (at) pakkipub.com', 13, 400, 1.5, col='#D6E8F4', tag='span'),
                width=240, grow=1, bg=BLUE, radius=24, pad=(26, 24), gap_=12, extra=CARD_SHADOW),
            white_card(eyebrow('Muut hallituksen jäsenet'), *member_rows, width=240, grow=1, gap_=10),
            d='row', wrap=True, gap_=16, align='stretch', cls='pv-stagger'),
        con(blob(SUN, 14, -3, {'pos': {'right': '-6%', 'top': '-30%'}, 'w': '28%', 'h': '150%'}),
            con(eyebrow('Tilintarkastaja', SUN), heading('Anni Laamanen', 'clamp(24px,2.6vw,34px)', 600, 1.2,
                                                           col='#FFFFFF', tag='span'),
                heading('HT-tilintarkastaja', 17, 400, 1.5, col='#D6E8F4', tag='span'), gap_=6),
            button('Sähköinen Tilintarkastus Pyhtää Oy', '#', size=14, ls=0, transform='none', fg='#FFFFFF',
                   bg='rgba(255,255,255,.12)', hfg='#FFFFFF', hbg='rgba(255,255,255,.2)', pad=(12, 18), radius=999),
            d='row', wrap=True, justify='space-between', align='center', gap_=18, bg=NAVY, radius=28,
            pad=('clamp(24px,3vw,34px)', 'clamp(22px,3vw,30px)'), overflow='hidden',
            extra=shadow(0, 24, 48, -20, 'rgba(11,46,79,.55)')),
        sid='hallitus', pad=('clamp(72px,8vw,104px)', 32, 'clamp(64px,8vw,104px)', 32))
    return [hero, board]


# ================================================================== HALLITUS (password protected)
def board_page():
    el.set_seed('page-hallitus')
    hero = page_hero('Hallitus', 'Hallituksen sivut',
                     [text('<p>Tälle sivulle kootaan hallituksen materiaalit, kuten kokousten pöytäkirjat ja muut '
                           'hallituksen asiakirjat.</p>', 18, 1.6, TXT)], 'sh-meetings')
    docs = section(heading('Hallituksen asiakirjat', H2, 600, 1.2, -0.015, NAVY),
                   white_card(text('<p>Asiakirjat lisätään tähän. Lisää jokainen asiakirja omana linkkinään.</p>',
                                   16, 1.6, TXT)), sid='asiakirjat')
    return [hero, docs]


# ================================================================== PUMPPAAMON HUOLTO
def pump_page():
    el.set_seed('page-pumppaamo')
    intro = white_card(
        con(con(width=8, minh=8, bg=SUN, radius=999, margin=(9, 0, 0, 0), extra={'_flex_size': 'none'}),
            heading('Kiinteistöpumppaamo tarvitsee säännöllistä huoltoa!', 17, 600, 1.4, col=NAVY, tag='span'),
            d='row', gap_=10, align='flex-start'),
        text('<p>Pumppaamon pitkän käyttöiän varmistaa parhaiten säännöllinen huolto. Pumppaamon ja uimurikytkinten '
             'pesu sekä sähköautomatiikan kunnon tarkistus tulee tehdä aina tarvittaessa, kuitenkin vähintään kerran '
             'vuodessa. Alusta asti kannattaa ottaa tavaksi avata pumppaamon kansi silloin tällöin ja varmistaa, että '
             'kaikki on kunnossa!</p>', 15, 1.65, TXT), width='min(100%,460px)', gap_=10)
    badge = con(eyebrow('Vähintään', INK), heading('kerran vuodessa', 24, 600, 1.1, col=INK, tag='span'),
                abs_={'left': '-4%', 'bottom': -28}, bg=SUN, radius=18, pad=(14, 18), gap_=2, z=3,
                cls='pv-float-card', width='auto', extra=shadow(0, 16, 32, -14, 'rgba(11,46,79,.45)'))
    hero = page_hero('Pumppaamon huolto', 'Pumppaamon huolto-ohjeet', [intro], 'pm-hero',
                     title_size='clamp(36px,4.4vw,60px)', overlay=[badge])

    ok = ['Tiski- ja pyykkivedet', 'Peseytymisvedet', 'WC:n huuhteluvedet']
    allowed = section(*sun_title('Mitä pumppaamoon saa laittaa ja mitä ei?'),
                      heading('Pumppaamoon saa laittaa vain:', 18, 600, 1.4, col=BLUE, tag='p', align='center'),
                      con(*[white_card(drop_icon('pv-icon-check', MIST, BLUE, 64, 24),
                                       heading(t, 17, 600, 1.35, col=NAVY, tag='span', align='center'),
                                       lines('sky', 6, 90, 20, 'quick'),
                                       width=200, grow=1, align='center', gap_=14, pad=(28, 18))
                            for t in ok], d='row', wrap=True, gap_=14, cls='pv-stagger', width='min(100%,820px)'),
                      align='center', sid='mita-saa-laittaa')

    bad = ['Vanupuikot tai vanulaput', 'Hiukset', 'Hammaslanka, hammasharjat, muovipussit', 'Rasvat tai öljyt',
           'Terveyssiteet, tamponit, vaipat tai pikkuhousunsuojat',
           'Desinfiointipyyhkeet, käsipyyhkeet, nenäliinat tai talouspaperi', 'Ruoantähteet tai kahvinporot',
           'Tupakantumpit, kondomit', 'WC-paperirullan hylsyt', 'Lääkkeet',
           'Bensiini, tärpätti, liuottimet, öljyt, emäkset ja hapot', 'Maalit, liimat',
           'Hiekka, kissanhiekka, multa', 'Paperipyyhkeet, sanomalehdet', 'Perunan- ja hedelmänkuoret']

    def bad_list(items, sid):
        return el.widget('icon-list', {
            'icon_list': [{'_id': f'{sid}{i}', 'text': t, 'selected_icon': svg_icon('pv-icon-drop')}
                          for i, t in enumerate(items)],
            'space_between': unit(10), 'icon_size': unit(12), 'text_indent': unit(10),
            'icon_self_vertical_align': 'flex-start', 'icon_vertical_offset': unit(4), 'icon_color': INK,
            'text_color': INK, 'divider': 'yes', 'divider_color': 'rgba(20,32,43,.18)',
            **el.typo('icon_typography', 15, 400, 1.45), '_css_classes': 'pv-bad-list',
            '_element_width': 'initial', '_element_custom_width': unit(260), '_flex_size': 'custom',
            '_flex_grow': 1, '_flex_shrink': 1})
    nature_note = con(con(heading('!', 20, 700, 1, col=INK, tag='span', align='center'), width=36, minh=36, bg=SUN,
                          radius=999, justify='center', align='center', extra={'_flex_size': 'none'}),
                      heading('Viemäriin joutuneet jätteet päätyvät häiritsemään luontoa', 15, 600, 1.35,
                              col='#FFFFFF', tag='span'),
                      d='row', gap_=10, align='center', abs_={'right': '-4%', 'bottom': -20}, bg=INK, radius=16,
                      pad=(12, 14), z=3, width='min(90%,280px)', cls='pv-float-card')
    nature = COL2(320, blob(SKY, 14, -4, {'pos': {'left': '-6%', 'bottom': '-6%'}, 'w': '60%', 'h': '60%'}),
                  photo('pm-nature', 28, {'pos': {'left': 0, 'top': 0}, 'w': '96%', 'h': '96%'}), nature_note,
                  minh='clamp(320px,32vw,440px)', extra={'min_height_mobile': unit(260)})
    sewer = section(con(nature,
                        COL2(420, pill('Huomioi', '#FFFFFF', INK),
                             heading('Nämä eivät kuulu viemäriin:', 'clamp(24px,2.6vw,32px)', 600, 1.25, col=INK),
                             con(bad_list(bad[:8], 'a'), bad_list(bad[8:], 'b'), d='row', wrap=True, gap_=24),
                             gap_=16),
                        d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center'),
                    bg=SUN, sid='ei-viemariin',
                    edges=(edge(CREAM, 'pv-edge-yellow-0', 28), edge(SUN, 'pv-edge-cream-8', 34, top=False)))

    wash_steps = ['Puutarhaletkulla', 'Pesuaineena voi käyttää tavallista astianpesuainetta',
                  'Poista uimurikytkimiin ja muihin rakenteisiin kertynyt rasva',
                  'Katkaise virta sähkökeskuksen pääkytkimestä',
                  'Täytä säiliö puhtaalla vedellä niin, että sen sisällä oleva vaakasuora, sinikahvainen '
                  'palloventtiili peittyy']
    wash = section(con(COL2(420, heading('Pese pumppaamo:', 'clamp(30px,3.6vw,48px)', 600, 1.1, -0.02, NAVY),
                            *[white_card(con(num_circle(i + 1), text(f'<p>{t}</p>', 15, 1.5, TXT, grow=1),
                                             d='row', gap_=14, align='center'), pad=(12, 16), radius=16)
                              for i, t in enumerate(wash_steps)], gap_=10),
                       photo_area('pm-wash', 'clamp(320px,34vw,460px)', SUN,
                                  {'pos': {'right': '-5%', 'bottom': '-6%'}, 'w': '52%', 'h': '56%'}),
                       d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center'),
                   sid='pesu')

    def pdf_card(title, href, bg, fg, dbg, dcol):
        return con(drop_icon('pv-icon-doc', dbg, dcol, 40, 18),
                   heading(title, 'clamp(18px,1.8vw,22px)', 600, 1.3, col=fg, tag='span'),
                   heading('Avaa PDF ↗', 13, 600, 1.4, col=fg, tag='span'),
                   width=300, grow=1, link=href, bg=bg, radius=24, pad=(26, 26), gap_=12, cls='pv-link-card',
                   extra=CARD_SHADOW)
    docs = section(con(pdf_card('Ohjeet käyttötauon ja talven jälkeen', UP + '2020/09/Tauko-k%C3%A4yt%C3%B6ss%C3%A4.pdf',
                                SUN, INK, '#FFFFFF', NAVY),
                       pdf_card('Tarkemmat ohjeet pumppaamoille',
                                UP + '2020/09/Polar-8-9-10-k%C3%A4ytt%C3%B6-ja-as.ohjeet-10.2013-1.pdf',
                                BLUE, '#FFFFFF', SKY, NAVY),
                       d='row', wrap=True, gap_=16, cls='pv-stagger'),
                   pad=(0, 32, 'clamp(16px,2vw,24px)', 32), sid='ohjeet')
    return [hero, allowed, sewer, wash, docs, contact()]


# ================================================================== YLEISTÄ TIETOA VEDESTÄ
def water_info():
    el.set_seed('page-vesi')
    jumps = con(chip('Talousvesi', '#talousvesi'), chip('Veden käyttö', '#veden-kaytto'),
                chip('Keskikulutus', '#keskikulutus'), chip('Kulutuksen vähentäminen', '#vahentaminen'),
                d='row', wrap=True, gap_=8)
    hero = page_hero('Yleistä tietoa vedestä', 'Yleistä tietoa vedestä', [jumps], 'wi-hero')

    steps = [('pv-icon-factory', BLUE, '#FFFFFF', 'Kuivalan tekopohjavesilaitos, Utti, Valkeala'),
             ('pv-icon-tower', SKY, NAVY, 'Tavastilan, Karhuvuoren ja Siltakylän vesitornit'),
             ('pv-icon-network', SUN, NAVY, 'Vesijohtoverkosto'),
             ('pv-icon-house', NAVY, '#FFFFFF', 'Asiakkaat')]
    flow = con(*[con(con(icon(i, 24, c), width=60, minh=60, bg=b, radius=999, justify='center', align='center',
                         cls='pv-icon-circle', extra={'_flex_size': 'none'}),
                     pill(f'Vaihe {n + 1}', BLUE, MIST, size=11),
                     heading(t, 15, 600, 1.35, col=NAVY, tag='span', align='center'),
                     width=170, grow=1, align='center', gap_=10)
                 for n, (i, b, c, t) in enumerate(steps)],
               d='row', wrap=True, gap_=16, cls='pv-stagger pv-flow')
    for s_ in flow['elements']:
        s_['elements'][1]['settings']['_flex_align_self'] = 'center'
    notes = con(con(drop_icon('pv-icon-drop', SKY, NAVY, 40, 18),
                    text('<p>Laadukas talousvesi toimitetaan kiinteistöille vesijohtoverkoston kautta. Kiinteistöillä '
                         'käytön jälkeen jätevesi palaa viemäriverkostoon.</p>', 16, 1.6, '#FFFFFF'),
                    width=340, grow=1, bg=NAVY, radius=24, pad=(28, 26), gap_=16, extra=CARD_SHADOW),
                con(drop_icon('pv-icon-drop', SUN, NAVY, 40, 18),
                    text('<p>Hulevedet johdetaan lähimpään vesistöön (avo-ojaan), ja jätevedet puhdistetaan '
                         'jätevedenpuhdistamolla.</p>', 16, 1.6, TXT),
                    width=340, grow=1, bg=MIST, radius=24, pad=(28, 26), gap_=16),
                d='row', wrap=True, gap_=16, cls='pv-stagger')
    drinking = section(eyebrow('Kymen Vesi Oy', align='center'),
                       heading('Talousvesi', H2_BIG, 600, 1.15, -0.015, NAVY, align='center'),
                       text('<p>Pyhtään vesiosuuskunnan toiminta-alueelle toimitettava talousvesi tulee Kymen Vesi Oy:n '
                            'kautta Kymenlaakson Vesi Oy:n Kuivalan tekopohjavesilaitokselta Utista, Valkealasta.</p>'
                            '<p>Vesi kulkee Tavastilan, Karhuvuoren ja Siltakylän vesitornien kautta '
                            'vesijohtoverkostoon ja edelleen asiakkaille.</p>', 17, 1.7, TXT, align='center',
                            width='min(100%,760px)'),
                       flow, notes, align='center', sid='talousvesi', gap_=24)

    uses = [('56', 'Henkilökohtainen hygienia', 'Suihkussa käynti kuluttaa vähemmän vettä kuin kylpyammeessa kylpeminen.', SKY),
            ('40', 'WC:n huuhtelu', 'Vuotava WC-istuin voi maksaa noin 4 € päivässä.', SUN),
            ('27', 'Pyykinpesu', 'Toimittamamme vesi on pehmeää (2–2,2 °dH). Vältä liiallista pesuaineen käyttöä.', SKY),
            ('10', 'Ruoanvalmistus', '', SKY),
            ('20', 'Astianpesu', 'Vältä astioiden pesua tai huuhtelua jatkuvasti valuvan hanan alla.', SKY),
            ('7', 'Muu käyttö', 'Puutarhan kastelu voi kuluttaa yllättävän paljon vettä.', SKY)]

    def use_tile(n, title, body, dcol):
        drop = con(heading(n, 26, 700, 1, col=NAVY, tag='span', align='center'),
                   heading('litraa', 10, 500, 1, col=NAVY, tag='span', align='center'),
                   width=76, minh=76, bg=dcol, radius=('50%', 0, '50%', '50%'), justify='center', align='center',
                   gap_=2, cls='pv-teardrop', extra={'_flex_size': 'none'})
        kids = [drop, heading(title, 19, 600, 1.3, col='#FFFFFF', tag='span', align='center'),
                heading(f'{n} litraa/hlö/vrk', 14, 500, 1.4, col=SUN, tag='span', align='center')]
        if body:
            kids.append(heading(body, 14, 400, 1.55, col='#D6E8F4', tag='span', align='center'))
        return con(*kids, width=240, grow=1, bg='rgba(255,255,255,.06)', radius=24, pad=(28, 22), gap_=10,
                   align='center')
    use = section(con(heading('Näin käytämme vettä', H2_BIG, 600, 1.15, -0.015, '#FFFFFF'),
                      lines('blue', 6, 160, 30, 'md'), d='row', wrap=True, justify='space-between', align='center',
                      gap_=16),
                  con(*[use_tile(*u) for u in uses], d='row', wrap=True, gap_=16, cls='pv-stagger'),
                  bg=NAVY, sid='veden-kaytto',
                  edges=(edge(CREAM, 'pv-edge-navy-m6', 30), edge(NAVY, 'pv-edge-cream-6', 26, top=False)))

    stats = [('Omakotitalot', '135'), ('Rivitalot', '150'), ('Kerrostalot', '170')]
    avg = section(*sun_title('Talousveden keskikulutus'),
                  con(*[white_card(heading(l, 16, 500, 1.4, col=GREY, tag='span', align='center'),
                                   heading(v, 'clamp(48px,5vw,64px)', 600, 1, -0.02, BLUE, tag='span', align='center'),
                                   heading('litraa/asukas/vrk', 14, 400, 1.4, col=GREY, tag='span', align='center'),
                                   width=200, grow=1, align='center', gap_=8, pad=(26, 18))
                        for l, v in stats], d='row', wrap=True, gap_=14, cls='pv-stagger',
                      width='min(100%,820px)'),
                  align='center', sid='keskikulutus')

    tips = ['Seuraa vedenkulutustasi viikoittain.', 'Käytä luotettavia ja helppokäyttöisiä vesikalusteita ja -laitteita.',
            'Asenna rivi- ja kerrostaloihin huoneistokohtaiset vesimittarit.', 'Korjaa vuotavat hanat viipymättä.',
            'Säädä WC-huuhtelun vesimäärää.', 'Vähennä puutarhan kastelua.']
    tip_rows = [con(num_circle(i + 1, NAVY, '#FFFFFF', 30, 13), text(f'<p>{t}</p>', 15, 1.5, INK, weight=500, grow=1),
                    d='row', gap_=12, align='center', bg='rgba(255,255,255,.55)', radius=14, pad=(10, 14))
                for i, t in enumerate(tips)]
    reduce = section(con(photo_area('wi-reduce', 'clamp(300px,30vw,400px)', SKY),
                         COL2(420, heading('Näin voit vähentää vedenkulutusta', H2, 600, 1.2, -0.015, INK),
                              *tip_rows, gap_=10),
                         d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='center'),
                     bg=SUN, sid='vahentaminen',
                     edges=(edge(CREAM, 'pv-edge-yellow-0', 28), edge(SUN, 'pv-edge-cream-8', 34, top=False)))
    return [hero, drinking, use, avg, reduce, contact()]


# ================================================================== OSAKKAAT
def shareholders():
    el.set_seed('page-osakkaat')
    jumps = con(chip('Kokoukset', '#kokoukset'), chip('Tiedotteet', '#tiedotteet'),
                chip('Liittymisehdot', '#liittymisehdot'), chip('Sopimuspohjat', '#sopimuspohjat'),
                chip('Toimintakertomukset', '#toimintakertomukset'), d='row', wrap=True, gap_=8)
    hero = page_hero('Osakkaat', 'Osakkaiden sivut', [jumps], 'sh-hero')

    meetings = [('27', 5, '2025', '2025/08/2025-Pyht%C3%A4%C3%A4n-Vok-varsinainen-kokous-p%C3%B6yt%C3%A4kirja-allek_.pdf'),
                ('18', 4, '2023', '2023/05/18042023-Pyht%C3%A4%C3%A4n-VOK-varsinainen-kokous-p%C3%B6yt%C3%A4kirja.pdf'),
                ('24', 5, '2022', '2022/05/24052022-Pyht%C3%A4%C3%A4n-Vok-varsinainen-kokous-p%C3%B6yt%C3%A4kirja-allek..pdf'),
                ('23', 9, '2021', '2021/10/23092021-Pyht%C3%A4%C3%A4n-Vok-varsinainen-kokous-p%C3%B6yt%C3%A4kirja.pdf'),
                ('23', 6, '2020', '2020/08/Varsinainen-kokous-23.6.2020-.pdf')]
    rows = [con(con(heading(d, 24, 700, 1, col=NAVY, tag='span', align='center'),
                    heading(FI_MONTH[m - 1].upper(), 10, 600, 1.2, 0.06, GREY, tag='span', align='center'),
                    width=54, gap_=2, align='center', extra={'_flex_size': 'none'}),
                con(heading(y, 20, 600, 1.2, col=NAVY, tag='span'),
                    heading(f'Pyhtään vesiosuuskunta – varsinaisen kokouksen pöytäkirja {int(d)}.{m}.{y}', 13, 400,
                            1.45, col=TXT, tag='span'), gap_=2, grow=1, width=0),
                arrow_circle(MIST, BLUE),
                d='row', gap_=14, align='center', link=UP + f, bg='#FFFFFF', radius=18, pad=(16, 18),
                cls='pv-link-card', extra=CARD_SHADOW)
            for d, m, y, f in meetings]
    meet = section(con(COL2(300, eyebrow('Varsinaisten kokousten pöytäkirjat'),
                            heading('Kokoukset', 'clamp(32px,4vw,56px)', 600, 1.1, -0.02, NAVY),
                            lines('blue', 6, 'min(100%,160px)', 30, 'md'),
                            con(blob(SUN, 13, -4, {'pos': {'left': '-8%', 'bottom': '-10%'}, 'w': '60%', 'h': '62%'}),
                                photo('sh-meetings', 24, {'pos': {'right': 0, 'top': 0}, 'w': '96%', 'h': '96%'}),
                                minh=220, margin=(12, 0, 0, 0)),
                            gap_=14),
                       COL2(440, *rows, gap_=10, cls='pv-stagger'),
                       d='row', wrap=True, gap_='clamp(32px,5vw,64px)', align='flex-start'),
                   sid='kokoukset')

    anns = [('17', 'Marraskuu 2024', '2024/11/Tiedote-17.11.2024.pdf', True),
            ('19', 'Syyskuu 2024', '2024/10/asiakaskirje-2024.pdf', False),
            ('30', 'Syyskuu 2022', '2022/11/Pvok-tiedote.pdf', False)]
    ann_cards = [con(con(pill('Tiedote', '#FFFFFF', INK), arrow_circle('#FFFFFF' if hl else SUN, NAVY),
                         d='row', justify='space-between', align='center'),
                     heading(d, 'clamp(48px,5vw,64px)', 600, 1, -0.03, NAVY if hl else BLUE, tag='span',
                             margin=(18, 0, 0, 0)),
                     heading(my, 16, 600, 1.3, col=INK, tag='span'),
                     width=220, grow=1, link=UP + f, bg=SUN if hl else '#FFFFFF', radius=24, pad=(22, 22), gap_=6,
                     cls='pv-link-card', extra=CARD_SHADOW)
                 for d, my, f, hl in anns]
    ann = section(con(heading('Tiedotteet', 'clamp(32px,4vw,56px)', 600, 1.1, -0.02, NAVY),
                      lines('yellow', 6, 160, 30, 'md'), d='row', wrap=True, justify='space-between', align='center',
                      gap_=16),
                  con(*ann_cards, d='row', wrap=True, gap_=16, cls='pv-stagger'), sid='tiedotteet',
                  pad=(0, 32, 'clamp(56px,7vw,96px)', 32))

    terms = [('Liittymisehdot', 'Liittymisehdot 29.8.2023', '2023/12/LIITTYMISEHDOT-29.8.2023-1.pdf', 'blue'),
             ('Liittymishakemus', 'Liittymishakemuslomake', '2022/09/Liittymishakemus-kaavake.doc', 'sun'),
             ('Vesiosuuskunnan säännöt', 'Pyhtään vesiosuuskunnan säännöt',
              '2023/05/PYHT%C3%84%C3%84N-VESIOSUUSKUNNAN-S%C3%84%C3%84NN%C3%96T.pdf', 'blue')]
    term_cards = [con(drop_icon('pv-icon-doc', '#FFFFFF' if c == 'sun' else SKY, NAVY, 40, 18),
                      eyebrow(e, INK if c == 'sun' else SKY),
                      heading(t, 'clamp(18px,1.8vw,22px)', 600, 1.3, col=INK if c == 'sun' else '#FFFFFF', tag='span'),
                      arrow_circle('#FFFFFF' if c == 'sun' else SKY, NAVY),
                      width=240, grow=1, link=UP + f, bg=SUN if c == 'sun' else 'rgba(255,255,255,.08)', radius=24,
                      pad=(24, 22), gap_=10, cls='pv-link-card')
                  for e, t, f, c in terms]
    band = section(con(*term_cards, d='row', wrap=True, gap_=16, cls='pv-stagger'), bg=NAVY, sid='liittymisehdot',
                   pad=('clamp(32px,4vw,48px)', 32),
                   edges=(edge(CREAM, 'pv-edge-navy-m6', 30), edge(NAVY, 'pv-edge-cream-6', 26, top=False)))

    agr = [('Liittymissopimus', '2022/09/Liittymissopimus.doc', MIST, BLUE, False),
           ('Johtoalueen käyttöoikeussopimus – 110914', '2014/08/Johtoalueen-k%C3%A4ytt%C3%B6oikessopimus-1109141.pdf',
            SUN, NAVY, True),
           ('Vesisopimus vuokralaiselle', '2023/03/Vesisopimus-vuokralainen.doc', MIST, BLUE, False)]
    agr_rows = [con(drop_icon('pv-icon-doc', db, dc, 44, 20),
                    con(heading(t, 17, 600, 1.3, col='#FFFFFF' if hl else NAVY, tag='span'),
                        heading('Sopimuspohja ↗', 12, 600, 1.4, col='#D6E8F4' if hl else BLUE, tag='span'),
                        gap_=4, grow=1, width=0),
                    d='row', gap_=16, align='center', link=UP + f, bg=BLUE if hl else '#FFFFFF', radius=18,
                    pad=(16, 18), cls='pv-link-card', extra=CARD_SHADOW)
                for t, f, db, dc, hl in agr]
    agreements = section(con(heading('Sopimuspohjat', 'clamp(32px,4vw,56px)', 600, 1.1, -0.02, NAVY),
                             lines('sky', 6, 160, 30, 'md'), d='row', wrap=True, justify='space-between',
                             align='center', gap_=16),
                         con(photo_area('sh-agreements', 'clamp(260px,24vw,320px)', SUN,
                                        {'pos': {'left': '30%', 'top': '-8%'}, 'w': '60%', 'h': '60%'}),
                             COL2(380, *agr_rows, gap_=10, cls='pv-stagger'),
                             d='row', wrap=True, gap_='clamp(24px,3vw,32px)', align='center'),
                         sid='sopimuspohjat')

    reports = [('2023', [('Toimintakertomus', '2024/11/PVOK-Toimintakertomus-2023.pdf'),
                         ('Tuloslaskelma ja tase', '2024/11/tasejatulos2023.pdf')]),
               ('2022', [('Toimintakertomus', '2023/05/PVOK-Toimintakertomus-2022.pdf'),
                         ('Tuloslaskelma ja tase', '2023/05/tilinp%C3%A4%C3%A4t%C3%B6s-yhteenveto.pdf')]),
               ('2021', [('Toimintakertomus', '2023/05/Toimintakertomusnettisivuille.pdf'),
                         ('Tuloslaskelma ja tase', '2023/05/tilinp%C3%A4%C3%A4t%C3%B6syhteenveto2021.pdf')]),
               ('2020', [('Toimintakertomus, tuloslaskelma ja tase', '2023/05/tilinp%C3%A4%C3%A4t%C3%B6s-2020.pdf')])]
    year_cards = [white_card(heading(y, 'clamp(32px,3.4vw,44px)', 600, 1, -0.02, BLUE, tag='span'),
                             *[button(f'{t} ↗', UP + f, size=13, ls=0, transform='none', fg=NAVY, bg=MIST, hfg=NAVY,
                                      hbg='#D6E8F4', pad=(10, 12), radius=10, cls='pv-doc-btn') for t, f in docs],
                             width=200, grow=1, gap_=10, pad=(20, 16))
                  for y, docs in reports]
    rep_photo = con(photo('sh-reports', 28, {'pos': {'left': 0, 'top': 0}, 'w': '100%', 'h': '100%'}),
                    minh='clamp(200px,24vw,340px)', extra={'min_height_mobile': unit(200)})
    reps = section(*sun_title('Toimintakertomukset, tuloslaskelmat ja taseet'), rep_photo,
                   con(*year_cards, d='row', wrap=True, gap_=14, align='stretch', cls='pv-stagger'),
                   sid='toimintakertomukset', gap_=28)
    return [hero, meet, ann, band, agreements, reps]


# ================================================================== VEDENLAATUTULOKSET
WQ_TEXT = {
    'Follow-up sample on 2 October': 'Uusintanäyte 2.10.',
    'Water quality test following pipe damage, 31 August 2020': 'Vedenlaatutesti putkivaurion jälkeen 31.8.2020',
    'Follow-up sample: Vastilantie': 'Uusintanäyte: Vastilantie',
    "Health Inspector's Statement Regarding a Water Pipe Break": 'Terveystarkastajan lausunto putkirikosta',
    'water is clean.': 'vesi on puhdasta', 'a new sample will be taken.': 'uusi näyte otetaan',
    'latest sample; water is clean.': 'uusin näyte, vesi on puhdasta', 'latest sample.': 'uusin näyte',
    'interim update.': 'välitiedote', 'under monitoring.': 'seurannassa', 'new sample': 'uusi näyte',
    'new sample collected': 'uusi näyte otettu',
}
WQ_SUMMARY_2023 = ['Vesijohtoverkoston veden laatu täytti kaikilta osin talousvedelle asetetut mikrobiologiset '
                   'laatuvaatimukset.',
                   'Myös Vastilantien veden laatu täytti vaatimukset, vaikka bakteeripesäkkeiden määrä oli koholla.']


def water_quality(data):
    el.set_seed('page-vedenlaatu')
    years = [y['year'] for y in data]
    chips = con(*[chip(y, f'#vuosi-{y}') for y in years[:4]], d='row', wrap=True, gap_=8)
    hero = page_hero('Vedenlaatutulokset', 'Vedenlaatutulokset', [chips], 'wq-hero')

    filt = button('Kaikki', '#tulokset', size=14, ls=0, transform='none', fg='#FFFFFF', bg=NAVY, hfg='#FFFFFF',
                  hbg=BLUE, pad=(8, 14), radius=999, cls='pv-wq-filter is-active')
    filters = [filt] + [button(y, f'#vuosi-{y}', size=14, ls=0, transform='none', fg=NAVY, bg='rgba(0,0,0,0)',
                               hfg=NAVY, hbg=MIST, pad=(8, 12), radius=999, cls='pv-wq-filter') for y in years]
    bar = con(con(*filters, d='row', wrap=True, gap_=4, align='center', grow=1, width=0),
              con(cls='pv-wq-search', width=240, minh=38, extra={'_flex_size': 'none'}),
              d='row', wrap=True, justify='space-between', align='center', gap_=12, bg='#FFFFFF', radius=999,
              pad=(8, 8, 8, 10), cls='pv-wq-bar', extra=CARD_SHADOW)
    bar['settings']['border_radius_mobile'] = dims(22)

    def item(it):
        place = WQ_TEXT.get(it['place'], it['place'])
        date = WQ_TEXT.get(it['date'], finnish_date(it['date']))
        note = WQ_TEXT.get(it['note'], it['note'])
        meta = []
        if date:
            meta.append(heading(date, 13, 400, 1.4, col=GREY, tag='span'))
        if note:
            ok = 'puhdasta' in note
            meta.append(heading(note, 11, 600, 1.4, col='#1E6B45' if ok else '#7A5300', tag='span',
                                bg='#DDF3E6' if ok else '#FCE6B8', radius=999, pad=(3, 9), width='auto'))
        kids = [heading(place, 16, 600, 1.35, col=NAVY, tag='span')]
        if meta:
            kids.append(con(*meta, d='row', wrap=True, gap_=8, align='center'))
        return con(*kids, link=it['href'], bg='#FFFFFF', radius=14, pad=(12, 16), gap_=4, cls='pv-wq-item pv-link-card',
                   extra=shadow(0, 10, 24, -18, 'rgba(11,46,79,.35)'))

    rows = []
    for y in data:
        right = []
        if y['year'] == '2023':
            right.append(con(*[text(f'<p>{p}</p>', 14, 1.6, '#FFFFFF') for p in WQ_SUMMARY_2023], bg=NAVY, radius=16,
                             pad=(16, 18), gap_=6, cls='pv-wq-summary'))
        right += [item(it) for it in y['items']]
        rows.append(con(COL2(180, heading(y['year'], 'clamp(44px,5vw,72px)', 600, 1, -0.03, BLUE, tag='h2'),
                             lines('sky', 6, 60, 18, 'quick'), gap_=8, cls='pv-wq-yearhead'),
                        COL2(520, *right, gap_=8),
                        d='row', wrap=True, gap_='clamp(20px,4vw,48px)', align='flex-start', cls='pv-wq-year',
                        extra={'_element_id': f'vuosi-{y["year"]}'}))
    results = section(bar, *rows, sid='tulokset', pad=(8, 32, 'clamp(56px,7vw,96px)', 32), gap_=44, cls='')
    return [hero, results]


PAGES_OUT = {
    'hinnasto': ('Price list', price_list),
    'yhteystiedot': ('Contact', contact_page),
    'hallitus': ('Board pages', board_page),
    'pumppaamon-huolto': ('Pumping station maintenance', pump_page),
    'yleista-tietoa-vedesta': ('General water information', water_info),
    'osakkaat': ('Members', shareholders),
    'vedenlaatutulokset': ('Water quality results', None),
}


def main():
    data = json.load(open(sys.argv[1]))
    el.MEDIA.update({k: tuple(v) for k, v in data['media'].items() if isinstance(v, list)})
    build.PAGES.update({k: v[1] for k, v in data['pages'].items()})
    wq = json.load(open(os.path.join(OUT, 'water-quality-en.json')))
    for slug, (_, fn) in PAGES_OUT.items():
        els = water_quality(wq) if slug == 'vedenlaatutulokset' else fn()
        els = auto_widths(els)
        path = os.path.join(OUT, f'page-{slug}.json')
        json.dump(els, open(path, 'w'), ensure_ascii=False, separators=(',', ':'))
        print(slug, os.path.getsize(path))


if __name__ == '__main__':
    main()
