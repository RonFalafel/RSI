from Windows.MainWindow import MainWindow
from yeelight import discover_bulbs
import time

# import Windows.SettingsWindow as SettingsWindow, Utils.ConfigurationManager as ConfigurationManager, Utils.HALightChanger as HALightChanger

from Utils.ConfigurationManager import ConfigurationManager
from Utils.ILightChanger import ILightChanger
from Utils.HALightChanger import HALightChanger
from Utils.YeeLightChanger import YeeLightChanger
from Utils.LightChangerResolver import LightChangerResolver
from Utils.ScreenReader import ScreenReader
from Windows.SettingsWindow import SettingsWindow
from Windows.MainWindow import MainWindow

# Utils Initialization
configurationManager = ConfigurationManager()
screenReader = ScreenReader()
lightChangerResolver = LightChangerResolver(configurationManager)

# Windows Initialization
settingsWindow = SettingsWindow(configurationManager, lightChangerResolver)
mainWindow = MainWindow(screenReader, lightChangerResolver, settingsWindow)

# YLC = YeeLightChanger("192.168.1.164")
# YLC.changeColor(0, 255, 0, 100)
# time.sleep(1)
# YLC.changeColor(0, 100, 0, 100)
# time.sleep(1)
# YLC.changeColor(0, 1, 0, 100)

# print(discover_bulbs())

mainWindow.showMainWindow()
