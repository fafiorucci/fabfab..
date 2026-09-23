import math, glob, os
def backdrop(dark=False):
    ink,wave,rose = ('#F5F1E8','#7FB8BF','#F5F1E8') if dark else ('#10263A','#1F6F78','#10263A')
    k = 1.6 if dark else 1.0
    cx,cy,R = 1760,170,250
    ticks=''
    for i in range(72):
        a=math.radians(i*5); l = 18 if i%18==0 else (12 if i%2==0 else 6)
        ticks+=f'<line x1="{cx+R*math.cos(a):.1f}" y1="{cy+R*math.sin(a):.1f}" x2="{cx+(R-l)*math.cos(a):.1f}" y2="{cy+(R-l)*math.sin(a):.1f}"/>'
    def star(r1,r2,rot):
        pts=[]
        for i in range(8):
            a=math.radians(rot+i*45); r = r1 if i%2==0 else r2
            pts.append(f'{cx+r*math.sin(a):.1f},{cy-r*math.cos(a):.1f}')
        return ' '.join(pts)
    rosebody=(f'<g fill="none" stroke="{rose}" stroke-opacity="{0.07*k:.3f}" stroke-width="2"><circle cx="{cx}" cy="{cy}" r="{R}"/><circle cx="{cx}" cy="{cy}" r="{R-26}"/>{ticks}</g>'
      f'<polygon points="{star(200,40,0)}" fill="{rose}" fill-opacity="{0.05*k:.3f}"/>'
      f'<polygon points="{star(130,30,45)}" fill="{rose}" fill-opacity="{0.04*k:.3f}"/>')
    waves=''
    for i,(y,op) in enumerate([(944,0.035),(984,0.04),(1024,0.05)]):
        ph=i*160
        d=f'M0 {y} ' + ' '.join(f'Q{ph%320+x+80} {y-14} {ph%320+x+160} {y} T{ph%320+x+320} {y}' for x in range(-320,1920,320)) 
        waves+=f'<path d="M-320 {y} '+ ''.join(f'q80 -14 160 0 t160 0 ' for _ in range(15)) + f'L2080 1080 L-320 1080 Z" transform="translate({-ph%320} 0)" fill="{wave}" fill-opacity="{op*k:.3f}"/>'
    lines=''.join(f'<path d="M-320 {y} '+ ''.join('q80 -12 160 0 t160 0 ' for _ in range(15)) + f'" transform="translate({-(j*110)%320} 0)" fill="none" stroke="{wave}" stroke-opacity="{0.10*k:.3f}" stroke-width="2"/>' for j,y in enumerate([930,970]))
    return (f'<svg aria-label="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080" style="position:absolute; left:0px; top:0px; width:1920px; height:1080px">'
            f'{rosebody}{waves}{lines}</svg>')
if __name__=='__main__':
    open('bg_preview.html','w').write(f'<html><body style="margin:0"><div style="position:relative;width:1920px;height:1080px;background:#F5F1E8">{backdrop()}<h2 style="position:absolute;left:128px;top:128px;margin:0;font:700 64px Georgia;color:#14212E">Segnalamento, segnali sonori e sicurezza</h2><p style="position:absolute;left:192px;top:990px;margin:0;font:24px Arial;color:#5C6874">Fabrizio Fiorucci · Patente nautica Vela/Motore senza limiti dalla costa</p></div>'
      f'<div style="position:relative;width:1920px;height:1080px;background:#10263A">{backdrop(True)}<h1 style="position:absolute;left:128px;top:420px;margin:0;font:700 96px Georgia;color:#F5F1E8">Patente nautica Vela/Motore</h1></div></body></html>')
    print(len(backdrop()), len(backdrop(True)))
