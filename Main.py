from Windows.MainWindow import MainWindow

from Utils.ConfigurationManager import ConfigurationManager
from Utils.LightChangerResolver import LightChangerResolver
from Utils.ScreenReader import ScreenReader
from Utils.RGBToHSVConverter import RGBToHSVConverter
from Utils.YeeLightBulbFinder import YeeLightBulbFinder
from Windows.SettingsWindow import SettingsWindow
from Windows.MainWindow import MainWindow

# Utils Initialization
configurationManager = ConfigurationManager()
screenReader = ScreenReader()
rgbToHSVConverter = RGBToHSVConverter()
lightChangerResolver = LightChangerResolver(configurationManager)
yeeLightBulbFinder = YeeLightBulbFinder()

# Windows Initialization
settingsWindow = SettingsWindow(configurationManager, lightChangerResolver, yeeLightBulbFinder)
mainWindow = MainWindow(screenReader, rgbToHSVConverter, lightChangerResolver, settingsWindow)

mainWindow.showMainWindow()
