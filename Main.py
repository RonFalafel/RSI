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
mainWindow = MainWindow(configurationManager, screenReader, rgbToHSVConverter, lightChangerResolver, settingsWindow)

mainWindow.showMainWindow()

# IN ORDER TO BUILD EXECUTABLE:
# 1. RUN: pip install pyinstaller
# 2: RUN: python3 -m PyInstaller --noconsole --onefile Main.py
