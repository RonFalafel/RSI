from yeelight import Bulb

import Utils.ILightChanger as ILightChanger

class YeeLightChanger(ILightChanger.ILightChanger):
    def __init__(self, yeelightIP):
        self.yeelightIP = yeelightIP
        self.bulb = Bulb(self.yeelightIP)
    
    def changeColor(self, r, g, b, br):
        try:
            print(f"R: {r}, G: {g}, b: {r}, ")
            self.bulb.set_rgb(r, g, b)
            self.bulb.set_brightness(br)
        except Exception as e:
            print(e)
            
    def defaultColor(self):
        try:
            self.bulb.set_default
        except Exception as e:
            print(e)
