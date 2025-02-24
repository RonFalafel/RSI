from yeelight import *
import time

from Utils.ILightChanger import ILightChanger
from Utils.RGBToHSVConverter import RGBToHSVConverter

class YeeLightChanger(ILightChanger):
    def __init__(self, yeelightIP):
        self.rgbToHSVConverter = RGBToHSVConverter()
        
        # Connection taken from https://hyperion-project.org/forum/index.php?thread/529-xiaomi-rgb-bulb-simple-udp-server-solution/
        self.yeelightIP = yeelightIP
        self.bulb = Bulb(self.yeelightIP)
        try:
            self.bulb.turn_on()
        except Exception as e:
            print(e)
        self.bulb.effect = "smooth" # can be "sudden" or "smooth"
        self.bulb.duration = 150 # miliseconds of duration of effect, ignored in "sudden" effect. MINIMUM 30!
        
        # Stop/Start music mode, bypasses lamp rate limits, ensures that previous sockets close before starting
        while True:
            try:
                self.bulb.stop_music()
                break
            except BulbException:
                break
        time.sleep(1)
        while True:
            try:
                self.bulb.start_music()
                break
            except BulbException:
                break
        time.sleep(1)
    
    def changeColor(self, r, g, b, br = 100):
        hsv = self.rgbToHSVConverter.rgb2hsv(r, g, b)
        try:
            self.bulb.set_hsv(*hsv) #, LightType.Main) # Don't know what this does... maybe look into it later lol
        except Exception as e:
            print(e)
            
    def defaultColor(self):
        try:
            self.bulb.set_color_temp(4700)
        except Exception as e:
            print(e)
