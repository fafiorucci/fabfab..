"""Logo Fabrizio Fiorucci con la frase in inglese «Sailing with passion, teaching with heart».
Crea in questa cartella la versione orizzontale (chiara, trasparente, negativa) e quella quadrata per i social (chiara e negativa).
Uso: python3 genera_logo_frase.py ["frase inglese" ["frase sotto il nome"]]   (serve Chromium; i font Google vengono scaricati una volta in fonts/)"""
import os, sys, re, base64, subprocess, math
from PIL import Image
os.chdir(os.path.dirname(os.path.abspath(__file__)))
INK='#1B2A41'; NAVY='#16324F'; CORAL='#E4572E'; SEA='#0B8A99'; PAPER='#FFF8EE'; DACC='#FFC145'
TAG = sys.argv[1] if len(sys.argv) > 1 else 'Sailing with passion, teaching with heart'
ROLE = sys.argv[2] if len(sys.argv) > 2 else 'Il mare, a vele spiegate'
OUT = '.'
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
H = "'Fredoka', 'Trebuchet MS', sans-serif"; B = "'Nunito Sans', Arial, sans-serif"; HAND = "'Caveat', 'Brush Script MT', cursive"
def logo(dark=False, style='', label='Logo Fabrizio Fiorucci'):
    ring,acc,wv = ('#FFF8EE','#FFC145','#7FD3DC') if dark else (NAVY,CORAL,SEA)
    ticks=''.join(f'<line x1="{100+78*math.cos(a):.1f}" y1="{100+78*math.sin(a):.1f}" x2="{100+86*math.cos(a):.1f}" y2="{100+86*math.sin(a):.1f}" stroke="{ring}" stroke-width="4" stroke-linecap="round"/>'
                  for a in [math.radians(d) for d in range(0,360,45) if d!=270])
    return (f'<svg aria-label="{label}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200" style="{style}">'
      f'<circle cx="100" cy="100" r="92" fill="none" stroke="{ring}" stroke-width="7"/>{ticks}'
      f'<path d="M100 16 L109 34 L91 34 Z" fill="{acc}"/><path d="M97 42 L97 132 L46 132 Q66 92 97 42 Z" fill="{ring}"/>'
      f'<path d="M104 54 L104 132 L148 132 Q128 96 104 54 Z" fill="{acc}"/><path d="M44 140 L156 140 Q148 156 126 158 L74 158 Q52 156 44 140 Z" fill="{ring}"/>'
      f'<path d="M50 173 Q62.5 165 75 173 T100 173 T125 173 T150 173" fill="none" stroke="{wv}" stroke-width="6" stroke-linecap="round"/></svg>')
def squiggle(color=CORAL, w=180):
    return (f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 18" width="{w}" height="18" style="width:{w}px; height:18px">'
            f'<path d="M5 9 ' + ' '.join('q11 -10 22 0 t22 0' for _ in range(w//44)) + f'" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round"/></svg>')

def fonts_css():
    """scarica una volta i font (Fredoka 700, Caveat 700, Nunito Sans 800) e li incorpora: il PNG non dipende dalla rete"""
    os.makedirs('fonts', exist_ok=True)
    url = 'https://fonts.googleapis.com/css2?family=Fredoka:wght@700&family=Caveat:wght@700&family=Nunito+Sans:wght@800&display=block'
    css = subprocess.run(['curl', '-sS', '-m', '30', '-A', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36', url], capture_output=True, text=True).stdout
    out = ''
    blocks = re.findall(r'/\* ([\w-]+) \*/\s*(@font-face \{.*?\})', css, re.S) or [('latin', b) for b in re.findall(r'@font-face \{.*?\}', css, re.S)]
    if not blocks: sys.exit('font non scaricati: controlla la connessione')
    for sub, blk in blocks:
        if sub not in ('latin', 'latin-ext'): continue
        fam = re.search(r"font-family: '([^']+)'", blk).group(1); u = re.search(r'url\((https://[^)]+)\)', blk).group(1)
        fn = f"fonts/{fam.replace(' ','')}-{sub}.woff2"
        if not os.path.exists(fn): subprocess.run(['curl', '-sS', '-m', '30', '-o', fn, u], check=True)
        out += blk.replace(u, 'data:font/woff2;base64,' + base64.b64encode(open(fn, 'rb').read()).decode()) + '\n'
    return '<style>' + out + '</style>'
LINKS = fonts_css()

def horizontal(dark=False, bg=None):
    name = '#FFFFFF' if dark else INK; role = '#7FD3DC' if dark else SEA; tag = DACC if dark else CORAL
    back = bg or 'transparent'
    return (1600, 480, f'''<div style="width:1600px; height:480px; background:{back}; display:flex; align-items:center; justify-content:center; gap:56px; padding:0px 70px; box-sizing:border-box">
{logo(dark, 'width:340px; height:340px; flex:none')}
<div style="display:flex; flex-direction:column; gap:10px">
<p style="margin:0; font-family:{H}; font-size:108px; font-weight:700; line-height:1.05; color:{name}; white-space:nowrap">Fabrizio Fiorucci</p>
<p style="margin:0; font-family:{B}; font-size:40px; font-weight:800; letter-spacing:1px; color:{role}">{ROLE}</p>
<div style="margin-top:6px">{squiggle(tag, 440)}</div>
<p style="margin:0; font-family:{HAND}; font-size:66px; font-weight:700; line-height:1.15; color:{tag}; white-space:nowrap">{TAG}</p>
</div></div>''')

def square(dark=False):
    name = '#FFFFFF' if dark else INK; role = '#7FD3DC' if dark else SEA; tag = DACC if dark else CORAL
    back = NAVY if dark else PAPER
    return (1080, 1080, f'''<div style="width:1080px; height:1080px; background:{back}; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px; box-sizing:border-box">
{logo(dark, 'width:440px; height:440px')}
<p style="margin:26px 0 0 0; font-family:{H}; font-size:92px; font-weight:700; line-height:1.05; color:{name}">Fabrizio Fiorucci</p>
<p style="margin:0; font-family:{B}; font-size:38px; font-weight:800; letter-spacing:1px; color:{role}">{ROLE}</p>
<div style="margin-top:8px">{squiggle(tag, 352)}</div>
<p style="margin:0; font-family:{HAND}; font-size:64px; font-weight:700; line-height:1.15; color:{tag}; text-align:center; width:900px">{TAG.replace(', ', ',<br>')}</p>
</div>''')

def render(name, spec, transparent=False):
    w, h, body = spec
    html = f'<html><head>{LINKS}<style>html,body{{margin:0; background:transparent}}</style></head><body>{body}</body></html>'
    src = os.path.abspath(f'{OUT}/_{name}.html'); open(src, 'w').write(html)
    args = [CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--virtual-time-budget=8000',
            f'--window-size={w},{h+200}', '--force-device-scale-factor=2', f'--screenshot={os.path.abspath(f"{OUT}/{name}.png")}']
    if transparent: args.insert(1, '--default-background-color=00000000')
    subprocess.run(args + ['file://' + src], capture_output=True)
    os.remove(src)
    im = Image.open(f'{OUT}/{name}.png'); im.crop((0, 0, 2*w, 2*h)).save(f'{OUT}/{name}.png')

render('logo-fiorucci-sailing-with-passion', horizontal(False, PAPER))
render('logo-fiorucci-sailing-with-passion-trasparente', horizontal(False), transparent=True)
render('logo-fiorucci-sailing-with-passion-negativo', horizontal(True, NAVY))
render('logo-fiorucci-sailing-with-passion-quadrato', square(False))
render('logo-fiorucci-sailing-with-passion-quadrato-negativo', square(True))
print('ok')
