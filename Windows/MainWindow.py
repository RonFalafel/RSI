import PySimpleGUI as sg
import numpy as np

from Utils.LightChangerResolver import LightChangerResolver
from Utils.ILightChanger import ILightChanger
from Utils.ScreenReader import ScreenReader
from Windows.SettingsWindow import SettingsWindow

class MainWindow:
    def __init__(self, screenReader: ScreenReader, lightChangerResolver: LightChangerResolver, settingsWindow : SettingsWindow):
        self.settingsWindow = settingsWindow
        self.screenReader = screenReader
        self.lightChangerResolver = lightChangerResolver
        self.lightChanger = self.lightChangerResolver.getLightChanger()

    def showMainWindow(self):
        sg.theme('Reddit')
        screens_list = self.screenReader.getScreensList()

        layout = [  
            [
                sg.Text('Max Brightness:', tooltip = 'The max brightness of the screen. When \"Vary Brightess\" is off, this change be the lamp brightness.'), 
                sg.Slider(range = (1, 100), default_value = 100, orientation = 'horizontal', key = "MAX-BRIGHTNESS"),
                sg.Checkbox('Vary Brightess', default = True, key = "VARY-BRIGHTNESS", tooltip = 'Toggles whether the brightness will vary depending on screen brightness.')
            ],
            [
                sg.Text('Screen:', tooltip = 'The screen to be synced to the light.'), 
                sg.Combo(values = screens_list, default_value = [screens_list[0]], disabled = len(screens_list) == 2, auto_size_text = True, key = 'SCREENS-LIST'), 
                sg.Button('Refresh Screens', tooltip = 'Use this to refresh the screen list when connecting / disconnecting screens.')
            ],
            [
                sg.Button('Start', tooltip = 'Starts the light sync.'), 
                sg.Button('Stop', tooltip = 'Stops the light sync and goes back to default lighting.'),
                sg.Button('Settings', tooltip = 'Configure app settings.')
            ]
        ]

        # Create the Window
        window = sg.Window('Screen Light Thingy', layout)

        running = False

        while True:
            event, values = window.read(1000)      
            print(event, values) # Shows GUI state every 1 second
            max_br = values["MAX-BRIGHTNESS"]
            vary_br = values["VARY-BRIGHTNESS"]
            sc = screens_list.index(values['SCREENS-LIST'])

            if event == 'Start': # if user clicks start
                # if br == '': br = 100 # todo make sure this is redundant - supposed to be beacuse of default-value
                running = True

            if event == sg.WIN_CLOSED: # if user closes window
                self.lightChanger.defaultColor()
                break

            if event == 'Stop': # if user clicks stop
                self.lightChanger.defaultColor()
                running = False

            if event == 'Refresh Screens': # if user clicks stop
                screens_list = self.screenReader.getScreensList()
                print(screens_list)
                window.Element('SCREENS-LIST').update(values = screens_list, set_to_index = [0])
                window.Element('SCREENS-LIST').update(disabled = len(screens_list) == 2)

            if event == 'Settings': # if user clicks stop
                self.settingsWindow.showSettingsWindow()
                self.lightChanger = self.lightChangerResolver.getLightChanger()

            if running:
                avg = self.screenReader.getAvgScreenColor(sc)
                r,g,b = avg[0],avg[1],avg[2]
                if vary_br: # Calculating average screen brightness if varying brightness is enabled in the GUI
                    # Brightness is measured by average r, g, and b values
                    rgb_avg = np.average([r, g, b])
                    # Brightness is then re-calculated from a scale of 1 to max-brightness (taken from the GUI)
                    br = (rgb_avg / 255) * max_br
                else:
                    br = max_br
                self.lightChanger.changeColor(r, g, b, br)

        window.close()