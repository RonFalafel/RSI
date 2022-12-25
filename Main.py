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
from Utils.RGBToHSVConverter import RGBToHSVConverter
from Windows.SettingsWindow import SettingsWindow
from Windows.MainWindow import MainWindow

# Utils Initialization
configurationManager = ConfigurationManager()
screenReader = ScreenReader()
rgbToHSVConverter = RGBToHSVConverter()
lightChangerResolver = LightChangerResolver(configurationManager)

# Windows Initialization
settingsWindow = SettingsWindow(configurationManager, lightChangerResolver)
mainWindow = MainWindow(screenReader, rgbToHSVConverter, lightChangerResolver, settingsWindow)

# print(discover_bulbs()) # Fututre feature - auto-discover yealink bulbs using this

mainWindow.showMainWindow()
