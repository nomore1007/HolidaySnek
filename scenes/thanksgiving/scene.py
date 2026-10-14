import math
from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.sky(c,w,h,"HARVEST TIME","Golden leaves, warm lights, grateful hearts","yellow")
        leaves=["*","v","~",",","+"]
        for i in range(int(w*intensity/2)):
            x=int((i*23+math.sin(self.t+i)*4+self.t*(1+i%2))%max(1,w))
            y=int((i*13+self.t*(1+i%3))%max(1,h-4))
            c.text(x,y,leaves[i%len(leaves)],["yellow","red","green"][i%3],True)
        x=max(0,w//2-12); y=max(2,h*2//3)
        c.text(x,y,"+--------------------+","yellow",True)
        c.text(x,y+1,"|   HARVEST FEAST    |","red",True)
        c.text(x,y+2,"+--------------------+","yellow",True)
