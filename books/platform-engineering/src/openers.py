# 下篇章首插图（v0.9.2）：与上篇总图同风格——浅底、六边形面板、线性图标、橙色高亮焦点
import os, math, subprocess, tempfile
W,H=1201,848
NAVY='#1f2a44'; BLUE='#1e5bb8'; LINE='#c3cad8'; PANEL='#f4f6fa'; OR='#ff8a00'; SOFT='#e8f0fb'
def hexp(cx,cy,r):
    return ' '.join(f'{cx+r*math.cos(math.radians(a)):.1f},{cy+r*math.sin(math.radians(a)):.1f}' for a in range(0,360,60))
def HEX(cx,cy,r,hl=False,fill=PANEL):
    s=f'<polygon points="{hexp(cx,cy,r)}" fill="{fill}" stroke="{LINE}" stroke-width="3"/>'
    if hl: s=f'<polygon points="{hexp(cx,cy,r+6)}" fill="none" stroke="{OR}" stroke-width="16" opacity=".35" filter="url(#bl)"/>'+s.replace(LINE,OR).replace('stroke-width="3"','stroke-width="5"')
    return s
def BADGE(cx,cy,r,icon,hl=False):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{OR if hl else BLUE}" stroke-width="{5 if hl else 3}"/>'
    if hl: s=f'<circle cx="{cx}" cy="{cy}" r="{r+8}" fill="none" stroke="{OR}" stroke-width="14" opacity=".35" filter="url(#bl)"/>'+s
    return s+f'<g transform="translate({cx},{cy}) scale({r/40})" fill="none" stroke="{NAVY}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>'
def LBL(x,y,t,sz=20,c=NAVY,w=700): return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{sz}" font-weight="{w}" fill="{c}" letter-spacing="1" font-family="Noto Sans CJK SC,sans-serif">{t}</text>'
def DASH(pts,c=LINE,w=3): return f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="8 7"/>'
def ARR(x1,y1,x2,y2,c=NAVY,w=4): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" marker-end="url(#ar)"/>'
ICONS={
 'book':'<path d="M-20,-18 h16 a6,6 0 0 1 4,4 v32 a6,6 0 0 0 -4,-4 h-16z M20,-18 h-16 a6,6 0 0 0 -4,4 v32 a6,6 0 0 1 4,-4 h16z"/>',
 'git':'<circle cx="-10" cy="-16" r="5"/><circle cx="-10" cy="16" r="5"/><circle cx="12" cy="-4" r="5"/><path d="M-10,-11 v22 M12,1 c0,10 -22,6 -22,10"/>',
 'person':'<circle cx="0" cy="-10" r="9"/><path d="M-18,20 c0,-14 36,-14 36,0"/>',
 'robot':'<rect x="-17" y="-12" width="34" height="26" rx="6"/><circle cx="-7" cy="0" r="3"/><circle cx="7" cy="0" r="3"/><path d="M0,-12 v-8 M-6,8 h12 M-21,0 h-3 M21,0 h3"/>',
 'lock':'<rect x="-14" y="-4" width="28" height="22" rx="4"/><path d="M-8,-4 v-6 a8,8 0 0 1 16,0 v6"/>',
 'tag':'<path d="M-18,-18 h16 l20,20 -16,16 -20,-20z"/><circle cx="-9" cy="-9" r="3"/>',
 'gate':'<path d="M-20,20 v-26 a20,20 0 0 1 40,0 v26 M-10,20 v-20 a10,10 0 0 1 20,0 v20"/>',
 'road':'<path d="M-8,-20 L-20,20 M8,-20 L20,20 M0,-16 v6 M0,-2 v6 M0,12 v6"/>',
 'cloud':'<path d="M-16,12 a10,10 0 0 1 0,-20 a14,14 0 0 1 26,-4 a10,10 0 0 1 6,24z"/>',
 'globe':'<circle r="18"/><path d="M-18,0 h36 M0,-18 c-10,10 -10,26 0,36 M0,-18 c10,10 10,26 0,36"/>',
 'chart':'<path d="M-18,18 h36 M-12,14 v-10 M-2,14 v-20 M8,14 v-14 M-14,-6 l10,-10 8,6 12,-10"/>',
 'db':'<ellipse cx="0" cy="-12" rx="16" ry="6"/><path d="M-16,-12 v24 a16,6 0 0 0 32,0 v-24 M-16,0 a16,6 0 0 0 32,0"/>',
 'id':'<rect x="-20" y="-14" width="40" height="28" rx="4"/><circle cx="-8" cy="-2" r="5"/><path d="M-15,9 c2,-6 12,-6 14,0 M4,-4 h10 M4,4 h8"/>',
 'bell':'<path d="M-14,10 v-8 a14,14 0 0 1 28,0 v8 l4,4 h-36z M-4,18 a4,4 0 0 0 8,0"/>',
 'eye':'<path d="M-20,0 c10,-14 30,-14 40,0 c-10,14 -30,14 -40,0z"/><circle r="6"/>',
 'search':'<circle cx="-4" cy="-4" r="12"/><path d="M5,5 l12,12"/>',
 'gear':'<circle r="7"/><path d="M0,-18 v6 M0,12 v6 M-18,0 h6 M12,0 h6 M-13,-13 l4,4 M9,9 l4,4 M13,-13 l-4,4 M-9,9 l-4,4"/>',
 'check':'<circle r="18"/><path d="M-8,0 l6,6 10,-12"/>',
 'pen':'<path d="M-14,16 l4,-12 20,-20 8,8 -20,20z M-14,16 l12,-4"/>',
 'grid':'<rect x="-18" y="-18" width="16" height="16" rx="3"/><rect x="2" y="-18" width="16" height="16" rx="3"/><rect x="-18" y="2" width="16" height="16" rx="3"/><rect x="2" y="2" width="16" height="16" rx="3"/>',
 'loop':'<path d="M-14,-6 a16,16 0 0 1 28,-4 M14,6 a16,16 0 0 1 -28,4"/><path d="M14,-18 v8 h-8 M-14,18 v-8 h8"/>',
}
def frame(body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="bl"><feGaussianBlur stdDeviation="6"/></filter>
<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10z" fill="{NAVY}"/></marker>
<radialGradient id="bg" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9edf3"/></radialGradient>
<linearGradient id="road" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffcf73"/><stop offset="1" stop-color="#ff9d1f"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>{body}</svg>'''
def ch12():
    b=HEX(600,410,190,hl=True)+BADGE(600,360,78,'book',True)+LBL(600,490,'RULEBOOK · 13 + 8',24)+LBL(600,522,'pinned @ SHA',18,BLUE,500)
    b+=HEX(230,410,120)+BADGE(230,395,58,'person')+LBL(230,490,'HUMAN',20)
    b+=HEX(970,410,120)+BADGE(970,395,58,'robot')+LBL(970,490,'AGENT',20)
    b+=DASH([(350,410),(410,410)])+DASH([(790,410),(850,410)])
    xs=[330,470,600,730,870]
    b+=f'<line x1="300" y1="720" x2="900" y2="720" stroke="{LINE}" stroke-width="4"/>'
    for i,x in enumerate(xs):
        hl=i==2; b+=BADGE(x,720,34,'tag' if hl else 'git',hl)
    b+=DASH([(600,600),(600,684)],OR,4)+LBL(600,800,'GIT SNAPSHOT',20,NAVY)
    b+=BADGE(600,120,46,'lock')+DASH([(600,166),(600,220)])
    return b
def ch13():
    b=f'<path d="M520,840 L575,330 L625,330 L680,840 Z" fill="url(#road)" opacity=".95"/>'
    b+=''.join(f'<rect x="596" y="{y}" width="8" height="{h}" fill="#fff" opacity=".8"/>' for y,h in [(780,40),(690,34),(610,28),(540,22),(480,16),(430,12)])
    b+=f'<path d="M430,330 v-120 a170,170 0 0 1 340,0 v120" fill="{PANEL}" stroke="{OR}" stroke-width="6"/><path d="M430,330 v-120 a170,170 0 0 1 340,0 v120" fill="none" stroke="{OR}" stroke-width="18" opacity=".3" filter="url(#bl)"/>'
    b+=f'<path d="M500,330 v-110 a100,100 0 0 1 200,0 v110 z" fill="#fff" stroke="{LINE}" stroke-width="3"/>'+LBL(600,150,'PORTAL',22)
    for i,(ic,t) in enumerate([('grid','HUB'),('chart','OPS'),('tag','RELEASES')]):
        b+=BADGE(540+i*60,260,24,ic)
    for x,y,ic in [(200,480,'globe'),(330,640,'cloud'),(1000,480,'db'),(870,640,'robot')]:
        b+=HEX(x,y,82)+BADGE(x,y,42,ic)
        b+=DASH([(x+(70 if x<600 else -70),y),(560 if x<600 else 640,y)],OR,3)
    b+=LBL(200,590,'STATIC',18)+LBL(330,750,'WEB',18)+LBL(1000,590,'DATABASE',18)+LBL(870,750,'AI APP',18)
    return b
def ch14():
    b=HEX(600,420,170,hl=True)+BADGE(600,380,64,'person',True)+LBL(600,480,'SELF-SERVICE',22)+LBL(600,510,'request → policy → deliver',16,BLUE,500)
    pts=[(600,110,'globe','CDN / DNS'),(905,265,'chart','MONITORING'),(905,600,'db','STORAGE'),(600,760,'bell','NOTIFY'),(295,600,'id','IDENTITY'),(295,265,'lock','VAULT')]
    for x,y,ic,t in pts:
        b+=DASH([(600,420),(x,y)])
    b=b.replace('<polygon','<polygon',1)
    out=''
    for x,y,ic,t in pts: out+=HEX(x,y,88)+BADGE(x,y-12,40,ic)+LBL(x,y+52,t,16)
    return DASH([(600,420),(600,110)])+''.join(DASH([(600,420),(x,y)]) for x,y,_,_ in pts)+HEX(600,420,170,hl=True)+BADGE(600,380,64,'person',True)+LBL(600,480,'SELF-SERVICE',22)+LBL(600,510,'request → policy → deliver',16,BLUE,500)+out
def ch15():
    cx,cy,R=600,430,270; st=[('eye','OBSERVE'),('search','DIAGNOSE'),('gear','ACT'),('check','VERIFY'),('pen','WRITE-BACK')]
    b=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE}" stroke-width="5" stroke-dasharray="14 10"/>'
    for i in range(5):
        a=math.radians(-90+i*72+36); b+=f'<path d="M{cx+R*math.cos(a-0.12):.0f},{cy+R*math.sin(a-0.12):.0f} A{R},{R} 0 0 1 {cx+R*math.cos(a+0.02):.0f},{cy+R*math.sin(a+0.02):.0f}" stroke="{NAVY}" stroke-width="5" fill="none" marker-end="url(#ar)"/>'
    for i,(ic,t) in enumerate(st):
        a=math.radians(-90+i*72); x,y=cx+R*math.cos(a),cy+R*math.sin(a)
        b+=BADGE(x,y,52,ic,i==4)+LBL(x,y+(80 if y>cy-50 else -68),t,18)
    b+=HEX(cx,cy,130,hl=True)+BADGE(cx,cy-12,58,'robot',True)+LBL(cx,cy+80,'ON WATCH',20)
    b+=BADGE(1060,120,40,'person')+LBL(1060,190,'HUMAN DECIDES',15)+DASH([(1020,140),(cx+60,cy-100)],OR,3)
    return b
def ch16():
    b=''
    xs=[150,260,370]; 
    for i,x in enumerate([130,250,370]): b+=BADGE(x,300,44,['git','gear','cloud'][i])
    b+=ARR(176,300,204,300)+ARR(296,300,324,300)+f'<path d="M370,346 v70 h-240 v-66" fill="none" stroke="{BLUE}" stroke-width="4" stroke-dasharray="9 7" marker-end="url(#ar)"/>'
    b+=LBL(250,200,'CLASSIC LOOP',22)+f'<rect x="70" y="230" width="360" height="220" rx="24" fill="none" stroke="{LINE}" stroke-width="3"/>'
    cx,cy,R=860,340,150
    b+=f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE}" stroke-width="5" stroke-dasharray="14 10"/>'
    for i,ic in enumerate(['eye','search','gear','check','pen']):
        a=math.radians(-90+i*72); b+=BADGE(cx+R*math.cos(a),cy+R*math.sin(a),34,ic)
    b+=BADGE(cx,cy,56,'robot')+LBL(860,150,'MODERN LOOP',22)
    b+=f'<path d="M430,340 C540,340 600,340 700,340" stroke="{OR}" stroke-width="22" opacity=".3" filter="url(#bl)" fill="none"/><path d="M430,340 C540,340 600,340 700,340" stroke="{OR}" stroke-width="6" fill="none" marker-end="url(#ar)"/>'
    b+=HEX(565,620,110,hl=True)+BADGE(565,600,50,'db',True)+LBL(565,690,'PLATFORM STATE',18)
    b+=DASH([(250,450),(250,620),(455,620)])+DASH([(860,490),(860,620),(675,620)])
    return b
def ch11():
    b=HEX(600,400,170,hl=True)+BADGE(600,360,62,'grid',True)+LBL(600,460,'AI GATEWAY',22)+LBL(600,490,'models as infrastructure',16,BLUE,500)
    for i,y in enumerate([200,400,600]):
        b+=DASH([(250,y),(450,400)])+HEX(190,y,80)+BADGE(190,y-8,38,'cloud')+LBL(190,y+50,f'MODEL {"ABC"[i]}',15)
    for i,(y,ic,t) in enumerate([(200,'robot','AGENT'),(400,'gear','MCP TOOLS'),(600,'person','APPS')]):
        b+=DASH([(750,400),(950,y)])+HEX(1010,y,80)+BADGE(1010,y-8,38,ic)+LBL(1010,y+50,t,15)
    b+=DASH([(600,570),(600,660)],OR,4)+HEX(600,730,85)+BADGE(600,720,38,'search')+LBL(600,782,'STATE INDEX',15)
    b+=BADGE(600,120,40,'lock')+DASH([(600,160),(600,230)])
    return b
ART={'11':ch11,'12':ch12,'13':ch13,'14':ch14,'15':ch15,'16':ch16,'17':ch16,'18':ch16}
def render(n,path):
    with tempfile.NamedTemporaryFile('w',suffix='.html',delete=False) as f:
        f.write(f'<html><body style="margin:0">{frame(ART[n]())}</body></html>'); h=f.name
    subprocess.run(['google-chrome','--headless','--no-sandbox','--disable-gpu','--hide-scrollbars',f'--window-size={W},{H}',f'--screenshot={path}',f'file://{h}'],check=True,capture_output=True)
    return path
if __name__=='__main__':
    for n in ['12','13','14','15','16']: render(n,f'/tmp/op{n}.png')
