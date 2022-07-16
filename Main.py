from Windows.MainWindow import MainWindow
import Windows.SettingsWindow as SettingsWindow, Utils.ConfigurationManager as ConfigurationManager, Utils.LightChanger as LightChanger

from Utils.ConfigurationManager import ConfigurationManager
from Utils.LightChanger import LightChanger
from Utils.ScreenReader import ScreenReader
from Windows.SettingsWindow import SettingsWindow
from Windows.MainWindow import MainWindow

# Utils Initialization
configurationManager = ConfigurationManager()
screenReader = ScreenReader()
lightChanger = LightChanger(configurationManager)

# Windows Initialization
settingsWindow = SettingsWindow(configurationManager, lightChanger)
mainWindow = MainWindow(screenReader, lightChanger, settingsWindow)

mainWindow.showMainWindow()
