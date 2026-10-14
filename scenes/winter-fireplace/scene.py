from holidaysnek.effects import BaseScene
class Scene(BaseScene):
    def render(self,c,w,h,intensity):
        self.fireplace(c,w,h,intensity,False)
