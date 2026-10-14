"""Reusable animation primitives for built-in scene plugins."""
import math, random

class BaseScene:
    def __init__(self):
        self.t=0.0
        self.rng=random.Random()
    def update(self,dt,width,height,intensity):
        self.t += dt
    def sky(self,c,w,h,title,subtitle,color="cyan"):
        for y in range(1,max(1,h-1),2):
            for x in range(int(self.t*2)%7,w,7):
                c.text(x,y,".", "blue", dim=True)
        c.text(max(0,(w-len(title))//2),max(0,h//4),title,color,True)
        c.text(max(0,(w-len(subtitle))//2),max(0,h//4+2),subtitle,"white")
    def snow(self,c,w,h,intensity):
        for i in range(int(w*h*.018*intensity)):
            x=int((i*37+math.sin(self.t*.8+i)*4+self.t*(1+i%3)*1.4)%max(1,w))
            y=int((i*19+self.t*(2+i%4))%max(1,h-1))
            c.text(x,y,"." if i%3 else "*","white",dim=i%3!=0)
    def fireplace(self,c,w,h,intensity,festive=False):
        if w<12 or h<6:
            c.text(0,0,"Resize terminal for the full hearth","yellow"); return
        top=max(1,int(h*.06)); floor=max(top+2,int(h*.82))
        palette=["red","red","yellow","yellow","white"]
        for y in range(top,floor):
            for x in range(w):
                ny=(floor-y)/max(1,floor-top)
                wave=math.sin(x*.31+self.t*3)+math.sin(x*.11-self.t*1.8)*.7+math.sin(x*.67+self.t*2.3)*.35
                edge=.12+.75*ny+wave*.10
                if ny>edge and self.rng.random()<min(.98,.30+intensity*.68):
                    ch=self.rng.choice([" "," ",".","░","▒","▓","^","/","|"])
                    color=palette[min(4,max(0,int(ny*5+self.rng.random()*1.6-.5)))]
                    if ch.strip(): c.text(x,y,ch,color,color=="white")
        c.text(0,floor,"="*w,"yellow",True)
        log_y=min(h-2,floor+1)
        c.text(0,log_y,"#"*w,"red",True)
        for x in range(w):
            if self.rng.random()<.12*intensity: c.text(x,log_y,"*","yellow",True)
        for i in range(int(w*intensity*.20)):
            x=int((i*29+math.sin(self.t*1.5+i)*5)%w)
            y=int(floor-(self.t*(2+i%4)+i*7)%max(1,floor-top))
            c.text(x,y,"." if i%2 else "*","yellow" if i%3 else "red",i%3==0)
        if festive:
            c.text(0,0,"~"*w,"green",True)
            bulbs=["red","yellow","cyan","magenta","green"]
            for x in range(2,w,5): c.text(x,1,"o",bulbs[int(x/5+self.t*2)%len(bulbs)],True)
            for x in range(3,w-3,max(8,w//5)):
                c.text(x,3,"|","red"); c.text(x-1,4,"[___]","red",True)
            c.text(max(0,w//2-8),max(2,floor-2),"MERRY CHRISTMAS","green",True)
        else:
            for y in range(2,max(2,floor-2),3):
                c.text(0,y,"*","cyan"); c.text(w-2,y,"*","cyan")
            self.snow(c,w,max(1,floor),intensity*.35)
    def room(self,c,w,h,title,festive=False):
        c.fill(0,0,w,h," ","blue")
        for y in range(1,max(1,h-2)):
            c.text(0,y,"|","yellow"); c.text(w-1,y,"|","yellow")
        c.text(2,1,"+"+"-"*max(0,w-6)+"+","yellow")
        c.text(max(1,(w-len(title))//2),2,title,"white",True)
        ww=min(18,max(8,w//4)); wx=max(2,w//6); wy=max(4,h//5); wh=max(3,h//3)
        for y in range(wy,min(h-3,wy+wh)):
            c.text(wx,y,"|"+ "."*max(0,ww-2)+"|","cyan")
        c.text(wx+ww//2,wy,"+","cyan")
        c.text(wx+ww//2,min(h-3,wy+wh//2),"+","cyan")
        for i in range(max(2,w//10)):
            x=(i*13+int(self.t*2))%max(1,w); y=(i*7+int(self.t*(1+i%2)))%max(1,h//2)
            c.text(x,y,"*","white",dim=True)
        fx=max(2,w*2//3); fy=max(5,h//2)
        for y in range(fy,min(h-3,fy+max(2,h//4))):
            c.text(fx,y,"|"+"#"*max(2,w//7)+"|","red",True)
        c.text(fx,fy-1,"/"+"^"*max(2,w//7)+"/","yellow",True)
        for i in range(max(2,h//5)):
            x=min(w-3,max(1,w//4+(i%2)*2)); y=min(h-4,h//2+i)
            c.text(x,y,"A","green",True)
            c.text(x,y+1,"*","yellow" if int(self.t*3+i)%2 else "red",True)
        if festive:
            for x in range(3,w-3,4): c.text(x,3,"o",["red","yellow","cyan","magenta"][int(x/4+self.t*2)%4],True)
            c.text(max(1,w//3),max(1,h-4),"Merry Christmas!","yellow",True)
        else: c.text(max(1,w//3),max(1,h-4),"Stay warm and cozy","yellow")
