import PySimpleGUI as sg

import Utils.ConfigurationManager as ConfigurationManager
from Utils.LightChangerResolver import LightChangerResolver
from Utils.ILightChanger import ILightChanger
from Utils.ScreenReader import ScreenReader
from Utils.RGBToHSVConverter import RGBToHSVConverter
from Windows.SettingsWindow import SettingsWindow

class MainWindow:
    def __init__(self, configManager : ConfigurationManager, screenReader: ScreenReader, rgbToHSVConverter: RGBToHSVConverter, lightChangerResolver: LightChangerResolver, settingsWindow : SettingsWindow):
        self.configManager = configManager
        self.settingsWindow = settingsWindow
        self.screenReader = screenReader
        self.rgbToHSVConverter = rgbToHSVConverter
        self.lightChangerResolver = lightChangerResolver
        self.lightChanger = self.lightChangerResolver.getLightChanger()
        self.screens_list = self.screenReader.getScreensList()

    def renderLayout(self):
        sg.theme('Reddit')

        layout = [  
            [
                sg.Text('Max Brightness:', tooltip = 'The max brightness of the screen. When \"Vary Brightess\" is off, this change be the lamp brightness.'), 
                sg.Slider(range = (1, 100), default_value = 100, orientation = 'horizontal', key = "MAX-BRIGHTNESS"),
                sg.Checkbox('Vary Brightess', default = True, key = "VARY-BRIGHTNESS", tooltip = 'Toggles whether the brightness will vary depending on screen brightness.')
            ],
            [
                sg.Text('Screen:', tooltip = 'The screen to be synced to the light.'), 
                sg.Combo(values = self.screens_list, default_value = [self.screens_list[0]], disabled = len(self.screens_list) == 2, auto_size_text = True, key = 'SCREENS-LIST'), 
                sg.Button('Refresh Screens', tooltip = 'Use this to refresh the screen list when connecting / disconnecting screens.')
            ],
            [
                sg.Button('Start', tooltip = 'Starts the light sync.'), 
                sg.Button('Stop', tooltip = 'Stops the light sync and goes back to default lighting.'),
                sg.Button('Settings', tooltip = 'Configure app settings.')
            ]
        ]

        # Create the Window
        return sg.Window('Screen Light Thingy', layout)
    
    def showMainWindow(self):
        window = self.renderLayout()
        config = self.configManager.read()

        refreshRate = config['ADVANCED']['refresh_rate']
        
        running = False # Wether the light sync is running or not

        while True:
            event, values = window.read(refreshRate) # I reccomend using 150ms for YeeLight Mode and 1000ms on HA mode (higher latency)
            # print(event, values) # Shows GUI state (for debugging)
            max_br = values["MAX-BRIGHTNESS"]
            vary_br = values["VARY-BRIGHTNESS"]
            sc = self.screens_list.index(values['SCREENS-LIST'])

            if event == 'Start': # if user clicks start
                running = True

            if event == sg.WIN_CLOSED: # if user closes window
                self.lightChanger.defaultColor()
                break

            if event == 'Stop': # if user clicks stop
                self.lightChanger.defaultColor()
                running = False

            if event == 'Refresh Screens': # if user clicks stop
                self.screens_list = self.screenReader.getScreensList()
                window.Element('SCREENS-LIST').update(values = self.screens_list, set_to_index = [0])
                window.Element('SCREENS-LIST').update(disabled = len(self.screens_list) == 2)

            if event == 'Settings': # if user clicks stop
                self.settingsWindow.showSettingsWindow()
                self.lightChanger = self.lightChangerResolver.getLightChanger()

            if running:
                avg = self.screenReader.getAvgScreenColor(sc)
                rgb = avg[0],avg[1],avg[2]
                hsv = self.rgbToHSVConverter.rgb2hsv(*rgb)
                if vary_br:
                    self.lightChanger.changeColor(*hsv)
                else:
                    self.lightChanger.changeColor(hsv[0], hsv[1], max_br)

        window.close()