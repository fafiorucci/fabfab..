/* Generato da prepara_pacchetto.py a partire da corso/app/index.html */
const HUES=['var(--coral)','var(--sea)','var(--purple)','var(--blue)','var(--green)'];
const TINTS=['var(--coral-t)','var(--sea-t)','var(--lilac-t)','var(--blue-t)','var(--green-t)'];

/* ---------- grafica delle slide: macchie, onde, linea ondulata, logo, icone ---------- */
function blob(cx,cy,r,seed=0,k=.18,n=7){const p=[];for(let i=0;i<n;i++){const a=2*Math.PI*i/n,rr=r*(1+k*Math.sin(3*a+seed)+.5*k*Math.cos(5*a+seed*1.7));p.push([cx+rr*Math.cos(a),cy+rr*Math.sin(a)]);}
  let d=`M${((p[0][0]+p[1][0])/2).toFixed(1)} ${((p[0][1]+p[1][1])/2).toFixed(1)} `;for(let i=0;i<n;i++){const a=p[(i+1)%n],b=p[(i+2)%n];d+=`Q${a[0].toFixed(1)} ${a[1].toFixed(1)} ${((a[0]+b[0])/2).toFixed(1)} ${((a[1]+b[1])/2).toFixed(1)} `;}return d+'Z';}
function wave(y,amp,per,x0,x1,h){let d=`M${x0} ${y} `;for(let x=x0;x<x1;x+=per)d+=`q${per/4} ${-amp} ${per/2} 0 t${per/2} 0 `;return d+`L${x1} ${h} L${x0} ${h} Z`;}
const W='#FFFFFF', SK=`stroke="${W}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"`;
const ICONS={
  lifebuoy:`<circle cx="50" cy="50" r="30" fill="none" stroke="${W}" stroke-opacity=".45" stroke-width="18"/><circle cx="50" cy="50" r="30" fill="none" stroke="${W}" stroke-width="18" stroke-dasharray="23.6 23.6" transform="rotate(-11 50 50)"/>`,
  hull:`<path d="M10 55 L90 55 L78 75 L22 75 Z" fill="${W}"/><path d="M34 55 L34 38 L64 38 L72 55" ${SK}/><path d="M8 90 q10.5 -7 21 0 t21 0 t21 0 t21 0" ${SK}/>`,
  propeller:`<circle cx="50" cy="50" r="9" fill="${W}"/>`+[0,120,240].map(a=>`<ellipse cx="50" cy="25" rx="11" ry="20" fill="${W}" transform="rotate(${a} 50 50)"/>`).join(''),
  quiz:`<rect x="16" y="12" width="68" height="80" rx="10" ${SK}/><path d="M30 34 L40 44 L56 26 M30 62 L70 62 M30 76 L60 76" ${SK}/>`,
  book:`<path d="M50 24 Q30 12 10 18 L10 82 Q30 76 50 88 Q70 76 90 82 L90 18 Q70 12 50 24 Z M50 24 L50 88" ${SK}/>`,
  chart:`<path d="M12 88 L90 88" ${SK}/><rect x="18" y="50" width="16" height="36" rx="3" fill="${W}"/><rect x="42" y="26" width="16" height="60" rx="3" fill="${W}"/><rect x="66" y="60" width="16" height="26" rx="3" fill="${W}"/>`,
  compass:`<circle cx="50" cy="50" r="38" ${SK}/><polygon points="50,14 58,50 50,86 42,50" fill="${W}"/><polygon points="14,50 50,42 86,50 50,58" fill="${W}" fill-opacity=".7"/>`,
  flag:`<path d="M24 10 L24 92" ${SK}/><path d="M28 14 L82 14 L70 32 L82 50 L28 50 Z" fill="${W}"/>`};
function svgEl(html,cls,vb){const s=document.createElementNS('http://www.w3.org/2000/svg','svg');s.setAttribute('viewBox',vb);if(cls)s.setAttribute('class',cls);s.setAttribute('aria-hidden','true');s.innerHTML=html;return s;}
const badge=(icon,hue)=>svgEl(`<path d="${blob(52,52,47,1,.07,8)}" fill="${hue}"/><g transform="translate(22 22) scale(.6)">${ICONS[icon]}</g>`,'badge','0 0 104 104');
const squiggle=(hue,w=150)=>{const s=svgEl(`<path d="M5 9 ${Array(Math.floor(w/44)).fill('q11 -10 22 0 t22 0').join(' ')}" fill="none" stroke="${hue}" stroke-width="7" stroke-linecap="round"/>`,'squig',`0 0 ${w} 18`);s.style.width=w*.8+'px';return s;};
function logo(dark){const ring=dark?'#FFF8EE':'var(--ink)',acc=dark?'#FFC145':'var(--coral)',wv=dark?'#7FD3DC':'var(--sea)';
  const ticks=[0,45,90,135,180,225,315].map(d=>{const a=d*Math.PI/180;return `<line x1="${100+78*Math.cos(a)}" y1="${100+78*Math.sin(a)}" x2="${100+86*Math.cos(a)}" y2="${100+86*Math.sin(a)}" stroke="${ring}" stroke-width="4" stroke-linecap="round"/>`}).join('');
  return svgEl(`<circle cx="100" cy="100" r="92" fill="none" stroke="${ring}" stroke-width="7"/>${ticks}<path d="M100 16 L109 34 L91 34 Z" fill="${acc}"/><path d="M97 42 L97 132 L46 132 Q66 92 97 42 Z" fill="${ring}"/><path d="M104 54 L104 132 L148 132 Q128 96 104 54 Z" fill="${acc}"/><path d="M44 140 L156 140 Q148 156 126 158 L74 158 Q52 156 44 140 Z" fill="${ring}"/><path d="M50 173 Q62.5 165 75 173 T100 173 T125 173 T150 173" fill="none" stroke="${wv}" stroke-width="6" stroke-linecap="round"/>`,'', '0 0 200 200');}
const el=(tag,attrs={},...kids)=>{const n=document.createElement(tag);for(const[k,v] of Object.entries(attrs)){if(k==='class')n.className=v;else if(k==='style')n.setAttribute('style',v);else if(k.startsWith('on'))n.addEventListener(k.slice(2),v);else if(v!==false&&v!=null)n.setAttribute(k,v===true?'':v);}for(const k of kids.flat()){if(k==null||k===false)continue;n.append(k.nodeType?k:document.createTextNode(String(k)));}return n;};
function head(pill,title,hue,icon,big){
  return el('div',{class:'head',style:'--hue:'+hue},badge(icon,hue),
    el('div',{class:'t'},el('span',{class:'pill'},pill),el(big?'h1':'h2',{},title),squiggle(hue)));
}
