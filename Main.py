from Windows.MainWindow import MainWindow
from yeelight import discover_bulbs # Fututre feature - auto-discover yealink bulbs using this
print(discover_bulbs()) # Fututre feature - auto-discover yealink bulbs using this

from Utils.ConfigurationManager import ConfigurationManager
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

mainWindow.showMainWindow()
