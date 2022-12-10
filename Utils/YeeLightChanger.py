from ctypes.wintypes import RGB
from yeelight import Bulb

import Utils.ILightChanger as ILightChanger

class YeeLightChanger(ILightChanger.ILightChanger):
    def __init__(self, yeelightIP):
        self.yeelightIP = yeelightIP
        self.bulb = Bulb(self.yeelightIP)
    
    def changeColor(self, r, g, b, br):
        print(f"R: {r}, G: {g}, b: {r}, ")
        self.bulb.set_rgb(r, g, b)
        self.bulb.set_brightness(br)

    def defaultColor(self):
        self.bulb.set_default