import math
from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.sky(c,w,h,"HALLOWEEN NIGHT","The witching hour is near","magenta")
        for i in range(int(w*intensity/5)):
            x=int((i*17+self.t*(2+i%3))%max(1,w))
            y=int((i*11+math.sin(self.t+i)*3)%max(1,h-3))
            c.text(x,y,"v" if i%2 else "^","white",True)
        x=max(0,w//2-7); y=max(0,h*2//3)
        c.text(x,y," .------. ","yellow",True)
        c.text(x,y+1," | o  o | ","yellow",True)
        c.text(x,y+2," |  vv  | ","yellow",True)
        c.text(x,y+3," '------' ","yellow",True)
