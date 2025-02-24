import PySimpleGUI as sg

import Utils.ConfigurationManager as ConfigurationManager
from Utils.LightChangerResolver import LightChangerResolver
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

    def renderLayout(self, theme, refreshRate, colorPrecision):
        sg.theme(theme)

        layout = [  
            [
                sg.Text('Max Brightness:', tooltip = 'The max brightness of the screen. When \"Vary Brightess\" is off, this change be the lamp brightness.'), 
                sg.Slider(range = (1, 100), default_value = 100, orientation = 'horizontal', key = "MAX-BRIGHTNESS", tooltip = 'The max brightness of the screen. When \"Vary Brightess\" is off, this change be the lamp brightness.'),
                sg.Checkbox('Vary Brightess', default = True, key = "VARY-BRIGHTNESS", tooltip = 'Toggles whether the brightness will vary depending on screen brightness.')
            ],
            [
                sg.Text('Refresh Rate:', tooltip = 'Milliseconds between each screen capture'), 
                sg.Slider(range = (0, 150), default_value = refreshRate, orientation = 'horizontal', enable_events=True, key = "REFRESH-RATE", tooltip = 'Milliseconds between each screen capture'),
                sg.Text('Color Precision:', tooltip = 'The precision of the color capture. Lower values are faster (less CPU) but less accurate.'), 
                sg.Slider(range = (0, 100), default_value = colorPrecision, orientation = 'horizontal', enable_events=True, key = "COLOR-PRECISION", tooltip = 'The precision of the color capture. Lower values are faster (less CPU) but less accurate.'),
            ],
            [
                sg.Text('Screen:', tooltip = 'The screen to be synced to the light.'), 
                sg.Combo(values = self.screens_list, default_value = [self.screens_list[0]], disabled = len(self.screens_list) == 2, auto_size_text = True, key = 'SCREENS-LIST'), 
                sg.Button('Refresh Screens', tooltip = 'Use this to refresh the screen list when connecting / disconnecting screens.'),
                sg.Text('UI Theme:', tooltip = 'The theme for the UI (I personally reccommend HotDogStand).'), 
                sg.Combo(values = sg.theme_list(), default_value = theme, auto_size_text = True, enable_events=True, key = 'THEME', tooltip = 'The theme for the UI (I personally reccommend HotDogStand).')
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
        config = self.configManager.read()

        try:
            refreshRate = int(config['ADVANCED']['refresh_rate'])
            colorPrecision = int(config['ADVANCED']['color_precision'])
        except:
            refreshRate = 0
            colorPrecision = 20
            self.configManager.writeAdvancedConfig(int(refreshRate), int(colorPrecision))

        try:
            theme = config['UI']['theme']
        except:
            theme = 'reddit'
            self.configManager.writeUIConfig(theme)


        window = self.renderLayout(theme, refreshRate, colorPrecision)
        running = False # Whether the light sync is running or not

        while True:
            event, values = window.read(refreshRate) # I reccomend using 150ms for YeeLight Mode and 1000ms on HA mode (higher latency)
            # print(event, values) # Shows GUI state (for debugging)
            
            if event == sg.WIN_CLOSED or values is None: # if user closes window
                self.lightChanger.defaultColor()
                break

            max_br = values["MAX-BRIGHTNESS"]
            vary_br = values["VARY-BRIGHTNESS"]
            sc = self.screens_list.index(values['SCREENS-LIST'])

            if event == 'Start': # if user clicks start
                running = True

            if event == 'Stop': # if user clicks stop
                self.lightChanger.defaultColor()
                running = False

            if event == 'Refresh Screens': # if user clicks Refresh Screens
                self.screens_list = self.screenReader.getScreensList()
                window.Element('SCREENS-LIST').update(values = self.screens_list, set_to_index = [0])
                window.Element('SCREENS-LIST').update(disabled = len(self.screens_list) == 2)

            if event == 'Settings': # if user clicks Settings
                self.settingsWindow.showSettingsWindow()
                self.lightChanger = self.lightChangerResolver.getLightChanger()

            if event == 'REFRESH-RATE': # if user changes refresh rate
                refreshRate = int(values['REFRESH-RATE'])
                self.configManager.writeAdvancedConfig(refreshRate, colorPrecision)

            if event == 'COLOR-PRECISION': # if user changes color precision
                colorPrecision = int(values['COLOR-PRECISION'])
                self.configManager.writeAdvancedConfig(refreshRate, colorPrecision)

            if event == 'THEME': # if user changes theme
                theme = values['THEME']
                self.configManager.writeUIConfig(theme)
                window.close()
                window = self.renderLayout(theme, refreshRate, colorPrecision)

            if running:
                avg = self.screenReader.getAvgScreenColor(sc, colorPrecision)
                rgb = avg[0],avg[1],avg[2]
                if vary_br:
                    self.lightChanger.changeColor(*rgb)
                else:
                    self.lightChanger.changeColor(rgb[0], rgb[1], rgb[2], max_br)

        window.close()