from yeelight import *
import time

import Utils.ILightChanger as ILightChanger

class YeeLightChanger(ILightChanger.ILightChanger):
    def __init__(self, yeelightIP):
        
        # Connection taken from https://hyperion-project.org/forum/index.php?thread/529-xiaomi-rgb-bulb-simple-udp-server-solution/
        self.yeelightIP = yeelightIP
        self.bulb = Bulb(self.yeelightIP)
        self.bulb.turn_on()
        self.bulb.effect = "smooth" # can be "sudden"
        
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
    
    def changeColor(self, h, s, v):
        try:
            self.bulb.set_hsv(h, s, v) #, LightType.Main) # Don't know what this does... maybe look into it later lol
        except Exception as e:
            print(e)
            
    def defaultColor(self):
        try:
            self.bulb.set_color_temp(4700)
        except Exception as e:
            print(e)
