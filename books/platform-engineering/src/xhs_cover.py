"""Highlighted Open Platform Toolkit overview per chapter (dim rest, glow on region). Boxes in 1024-wide display coords."""
import os,io,base64
from PIL import Image,ImageEnhance,ImageFilter,ImageDraw
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CROP=(82,85,942,692)
B=dict(title=(160,88,820,205),center=(420,330,605,460),git=(425,208,600,325),iac=(580,245,770,382),auto=(578,388,770,527),sec=(420,452,605,574),env=(255,388,445,527),cloud=(258,245,445,385),
 identity=(100,235,192,345),obs=(98,358,192,465),ops=(98,470,192,577),secure=(798,235,892,357),observable=(798,362,892,462),recov=(798,470,892,582),chain=(205,572,805,645))
MAP={'1':['title','center'],'2':['git','chain'],'3':['iac'],'4':['auto'],'5':['sec','identity','secure'],'6':['env'],'7':['cloud'],'8':['obs','observable'],'9':['recov'],'10':['ops','chain'],'11':list(B)}
def cover(n,path=None):
    src=Image.open(os.path.join(ROOT,'assets','overview-src.jpg')).convert('RGB'); k=src.width/1024
    sc=lambda b:tuple(int(v*k) for v in b)
    im=src.crop(sc(CROP)); ox,oy=sc(CROP)[:2]
    dim=ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(0.15)).enhance(0.55)
    mask=Image.new('L',im.size,0); d=ImageDraw.Draw(mask); boxes=[]
    for r in MAP[n]:
        x0,y0,x1,y1=sc(B[r]); b=(x0-ox,y0-oy,x1-ox,y1-oy); boxes.append(b); d.rounded_rectangle(b,24,fill=255)
    out=Image.composite(im,dim,mask)
    glow=Image.new('L',im.size,0); g=ImageDraw.Draw(glow)
    for b in boxes: g.rounded_rectangle(b,24,outline=255,width=14)
    glow=glow.filter(ImageFilter.GaussianBlur(10))
    out=Image.composite(Image.new('RGB',im.size,'#ffb020'),out,glow)
    dd=ImageDraw.Draw(out)
    for b in boxes: dd.rounded_rectangle(b,24,outline='#ff8a00',width=5)
    if path: out.save(path); return os.path.basename(path)
    buf=io.BytesIO(); out.save(buf,'PNG'); return 'data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
if __name__=='__main__':
    import sys; n=sys.argv[1]; open(f'/tmp/cov{n}.png','wb').write(base64.b64decode(cover(n).split(',')[1]))
