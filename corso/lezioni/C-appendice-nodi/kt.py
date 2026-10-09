"""Anteprima rapida dei pannelli dei nodi: python3 kt.py nome -> kt_nome.png"""
import sys, os, subprocess, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nodi
from PIL import Image
name=sys.argv[1]
K=nodi.KNOTS[name](); panels=K['panels']
CH='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
W,H=(nodi.PW,nodi.PH) if K['layout']=='land' else (nodi.QW,nodi.QH)
NC=2 if K['layout']=='land' else 4
cells=''.join(f'<div style="position:relative;width:{W}px;height:{H+74}px;background:#E4F3F1;border-radius:24px;overflow:hidden"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{b}</svg><p style="position:absolute;left:14px;bottom:6px;margin:0;font:600 20px Arial;color:#16324F">{i+1}. {cap}</p></div>' for i,(b,cap) in enumerate(panels))
html=f'<html><body style="margin:0;background:#FFF8EE"><div style="display:grid;grid-template-columns:repeat({NC},{W}px);gap:16px;padding:16px">{cells}</div></body></html>'
open('kt.html','w').write(html)
rows=(len(panels)+NC-1)//NC; h=rows*(H+74+16)+16; w=NC*W+16*(NC+1)
subprocess.run([CH,'--headless','--no-sandbox','--disable-gpu','--hide-scrollbars',f'--window-size={w},{h+200}','--force-device-scale-factor=1.5',f'--screenshot={os.path.abspath("kt.png")}','file://'+os.path.abspath('kt.html')],capture_output=True)
im=Image.open('kt.png'); im.crop((0,0,int(w*1.5),int(h*1.5))).save(f'kt_{name}.png')
print('ok', sum(len(b) for b,_ in panels))
