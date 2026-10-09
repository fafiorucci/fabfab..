import sys, os, re, subprocess, json
from PIL import Image
deck, ids, outpng = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
B='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
faces=json.load(open(f'{deck}/project/deck.json'))['faces']
links=''.join(f'<link rel="stylesheet" href="{v["href"]}">' for v in faces.values() if 'href' in v)
tiles=[]
for i in ids:
    h=open(f'{deck}/project/slides/{i}.html').read()
    h=re.sub(r'<aside>.*?</aside>','',h,flags=re.S)
    h=h.replace('<section ','<section data-x ',1).replace('style="','style="position:relative; width:1920px; height:1080px; box-sizing:border-box; overflow:hidden; ',1)
    tiles.append(h)
html=f'<html><head>{links}<style>*{{margin:0;box-sizing:border-box}} section[data-x] > *:not(svg):not([style*="position:absolute"]){{position:relative}} ul,ol{{padding-left:40px}}</style></head><body style="margin:0">'+''.join(tiles)+'</body></html>'
open('pv.html','w').write(html)
subprocess.run([B,'--headless','--no-sandbox','--disable-gpu','--hide-scrollbars','--virtual-time-budget=6000',f'--window-size=1920,{1080*len(ids)+200}',f'--screenshot={os.path.abspath("pv_full.png")}','file://'+os.path.abspath('pv.html')],capture_output=True)
im=Image.open('pv_full.png'); n=len(ids)
cols=2 if n>1 else 1; rows=(n+cols-1)//cols
sheet=Image.new('RGB',(960*cols,540*rows),'white')
for k in range(n):
    t=im.crop((0,1080*k,1920,1080*(k+1))).resize((960,540))
    sheet.paste(t,((k%cols)*960,(k//cols)*540))
sheet.save(outpng)
