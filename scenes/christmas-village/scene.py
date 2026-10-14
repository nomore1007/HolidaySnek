from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.sky(c,w,h,"CHRISTMAS VILLAGE","Snowfall and starlight on a winter night","cyan")
        self.snow(c,w,h-2,intensity)
        ground=max(2,h*2//3)
        c.text(0,ground,"_"*w,"white")
        count=max(1,w//10)
        for i in range(count):
            x=i*max(1,w//count); hh=3+i%3
            for j in range(hh): c.text(x,ground-j-1,"/\\ " if j==hh-1 else "|_|","yellow" if i%2 else "cyan")
            c.text(x,ground-hh-1,"*","yellow",True)
