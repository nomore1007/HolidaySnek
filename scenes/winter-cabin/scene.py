from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.room(c,w,h,"WINTER CABIN",False)
        self.snow(c,w,h//2,intensity*.6)
