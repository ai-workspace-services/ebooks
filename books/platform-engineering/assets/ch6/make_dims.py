from PIL import Image, ImageDraw, ImageFont
FB="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc";FR="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
f=lambda p,s:ImageFont.truetype(p,s,index=2)
W,H=1080,760;im=Image.new("RGB",(W,H),"white");d=ImageDraw.Draw(im)
t="四个维度交叉组合，各取所需";d.text(((W-d.textlength(t,font=f(FB,32)))/2,30),t,font=f(FB,32),fill=(15,23,42))
cx,cy=540,420
B=[("多环境","SIT / UAT / PROD",(37,99,235),(240,246,255),(cx,150)),
   ("多分支","feature / main / release tag",(22,163,74),(240,253,244),(cx+330,cy)),
   ("滚动发布","按 digest 分批 + 探针放行",(217,119,6),(255,251,235),(cx,690)),
   ("特性泳道","feature-<id>-sit 隔离命名空间",(147,51,234),(250,245,255),(cx-330,cy))]
for _,_,c,_,(x,y) in B: d.line((cx,cy,x,y),fill=c,width=5)
for a,b,c,bg,(x,y) in B:
    w=300;h=96;d.rounded_rectangle((x-w/2,y-h/2,x+w/2,y+h/2),16,fill=bg,outline=c,width=4)
    d.text((x-d.textlength(a,font=f(FB,28))/2,y-40),a,font=f(FB,28),fill=c)
    d.text((x-d.textlength(b,font=f(FR,20))/2,y+4),b,font=f(FR,20),fill=(30,41,59))
d.ellipse((cx-110,cy-62,cx+110,cy+62),fill=(15,23,42))
for i,s in enumerate(["一次变更","按需选组合"]):
    d.text((cx-d.textlength(s,font=f(FB,24))/2,cy-36+i*36),s,font=f(FB,24),fill="white")
im.save("assets/ch6/dims.png")
