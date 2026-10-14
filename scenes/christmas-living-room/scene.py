from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.room(c,w,h,"CHRISTMAS LIVING ROOM",True)
        self.snow(c,w,h//2,intensity*.45)
