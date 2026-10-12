import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
INK="#1f2933"; LIGHT="#f0d9b5"; DARK="#b58863"; HL="#2563eb"; GREY="#8a949e"; EMPTY="#e9edf1"
plt.rcParams.update({"font.size":11,"text.color":INK,"figure.facecolor":"white","svg.fonttype":"path"})
import os; os.makedirs("assets",exist_ok=True)
G={"R":"♜","N":"♞","B":"♝","Q":"♛","K":"♚"}; CODE={"R":1,"N":2,"B":3,"Q":4,"K":5}
def save(fig,name):
    fig.savefig(f"assets/{name}.svg",bbox_inches="tight",facecolor="white")
    plt.close(fig)
def rank(ax,x0,y0,pieces,new=(),s=1.0,files=False,digits=False):
    for f in range(8):
        ax.add_patch(Rectangle((x0+f*s,y0),s,s,fc=DARK if f%2==0 else LIGHT,ec="none"))
        p=pieces[f]
        if p and p!="-":
            ax.text(x0+f*s+s/2,y0+s*0.47,G[p],ha="center",va="center",fontsize=26*s,color=HL if f in new else INK)
        if f in new: ax.add_patch(Rectangle((x0+f*s+.04,y0+.04),s-.08,s-.08,fc="none",ec=HL,lw=2.4))
        if files: ax.text(x0+f*s+s/2,y0+s+.18,"abcdefgh"[f],ha="center",va="bottom",fontsize=11,color=GREY)
        if digits: ax.text(x0+f*s+s/2,y0-.22,str(CODE[p]) if p and p!="-" else "0",ha="center",va="top",fontsize=17,fontweight="bold")
    ax.add_patch(Rectangle((x0,y0),8*s,s,fc="none",ec=INK,lw=1))

# 1. Decoding 518
steps=[("518 ÷ 4 = 129  r 2","Light-squared bishop\non 3rd light square: f","-----B--",[5]),
       ("129 ÷ 4 = 32  r 1","Dark-squared bishop\non 2nd dark square: c","--B--B--",[2]),
       ("32 ÷ 6 = 5  r 2","Queen on 3rd\nempty square: d","--BQ-B--",[3]),
       ("Knight code 5","Knights on 2nd and 4th\nempty squares: b, g","-NBQ-BN-",[1,6]),
       ("Remaining a, e, h","Rook, king, rook\nleft to right","RNBQKBNR",[0,4,7])]
fig,ax=plt.subplots(figsize=(10,7.6)); ax.set_xlim(-6.2,13.4); ax.set_ylim(-1.3,len(steps)*1.45+.9); ax.axis("off")
for i,(op,txt,b,new) in enumerate(steps):
    y=(len(steps)-1-i)*1.45
    ax.text(-6.1,y+.5,f"Step {i+1}",fontsize=10,color=GREY,va="center"); ax.text(-4.9,y+.5,op,fontsize=11,va="center",fontweight="bold")
    rank(ax,0.2,y,list(b),new,files=(i==0),digits=(i==len(steps)-1)); ax.text(8.6,y+.5,txt,fontsize=10,va="center")
ax.text(0.2+4,-1.05,"Layout code: 12,345,321",ha="center",fontsize=11.5,color=HL,fontweight="bold")
ax.set_title("Decoding Scharnagl Number 518",loc="left",fontweight="bold",fontsize=13); save(fig,"decode_518")

# 2. Reading the layout code
fig,ax=plt.subplots(figsize=(10,4.3)); ax.set_xlim(-2.6,13.6); ax.set_ylim(-3.6,1.5); ax.axis("off")
rank(ax,0,0,list("RNBQKBNR"),files=True,digits=True); ax.text(-.3,.5,"518",ha="right",va="center",fontsize=13,fontweight="bold")
rank(ax,0,-2.4,list("BBQNNRKR"),digits=True); ax.text(-.3,-1.9,"0",ha="right",va="center",fontsize=13,fontweight="bold")
ax.text(-.3,-3.05,"",fontsize=1)
for j,(p,c) in enumerate([("R",1),("N",2),("B",3),("Q",4),("K",5)]):
    y=.9-j*.85; ax.text(9.4,y,str(c),fontsize=15,fontweight="bold",va="center"); ax.text(10.0,y,G[p],fontsize=21,va="center")
    ax.text(10.75,y,{"R":"Rook","N":"Knight","B":"Bishop","Q":"Queen","K":"King"}[p],fontsize=11,va="center")
ax.set_title("Reading the Layout Code: one digit per file, a to h",loc="left",fontweight="bold",fontsize=13); save(fig,"layout_code")

# 3. Knight table
kn=[(0,1),(0,2),(0,3),(0,4),(1,2),(1,3),(1,4),(2,3),(2,4),(3,4)]
fig,ax=plt.subplots(figsize=(8.6,7.4)); ax.set_xlim(-2.4,10.6); ax.set_ylim(-.9,11.3); ax.axis("off")
ax.text(-1.2,10.55,"Code",ha="center",fontsize=10,color=GREY); ax.text(2.5,10.55,"Five empty squares, left to right",ha="center",fontsize=10,color=GREY)
ax.text(6.4,10.55,"First\n(0000111223)",ha="center",fontsize=9.5,color=GREY,va="bottom"); ax.text(8.6,10.55,"Second\n(1234234344)",ha="center",fontsize=9.5,color=GREY,va="bottom")
for c,(a,b) in enumerate(kn):
    y=9-c
    ax.text(-1.2,y+.45,str(c),ha="center",va="center",fontsize=13,fontweight="bold")
    for k in range(5):
        ax.add_patch(Rectangle((k+.05,y+.05),.9,.9,fc=EMPTY,ec="#c3cad1"))
        if k in (a,b): ax.text(k+.5,y+.45,G["N"],ha="center",va="center",fontsize=22,color=HL if k==b else INK)
        if c==9: ax.text(k+.5,y-.3,str(k),ha="center",va="center",fontsize=9,color=GREY)
    ax.text(6.4,y+.45,str(a),ha="center",va="center",fontsize=13); ax.text(8.6,y+.45,str(b),ha="center",va="center",fontsize=13,color=HL,fontweight="bold")
ax.text(2.5,-.75,"square number (from 0)",ha="center",fontsize=9,color=GREY)
ax.set_title("Knight Table: the second knight (blue) is placed first",loc="left",fontweight="bold",fontsize=13); save(fig,"knight_table")
