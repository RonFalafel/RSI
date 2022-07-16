import PySimpleGUI as sg
import time

import Utils.ConfigurationManager as ConfigurationManager, Utils.LightChanger as LightChanger

class SettingsWindow:
    def __init__(self, configManager : ConfigurationManager, lightChanger: LightChanger):
        self.configManager = configManager
        self.lightChanger = lightChanger

    def showSettingsWindow(self):
        config = self.configManager.read()
        home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
        home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
        
        layout = [
                    [
                        sg.Text('Home Assistant IP', tooltip = 'The local address of your Home Assistant.'), 
                        sg.InputText(default_text = home_assistant_ip, key = 'HOME-ASSISTANT-IP')
                    ],
                    [
                        sg.Text('Home Assistant Port:', tooltip = 'The port of your Home Assistant (8123 by default).'), 
                        sg.InputText(default_text = home_assistant_port, key = 'HOME-ASSISTANT-PORT')
                    ],
                    [
                        sg.Button('Save', tooltip = 'Validates and saves the new configuration.'), 
                        sg.Button('Cancel', tooltip = 'Closes the settings window.'), 
                    ]
                ]

        window = sg.Window('Settings', layout)

        while True:
            event, values = window.read()
            if event in ('Cancel', sg.WIN_CLOSED):
                break
            if event == 'Save':
                home_assistant_ip = values['HOME-ASSISTANT-IP']
                home_assistant_port = values['HOME-ASSISTANT-PORT']
                self.configManager.write(home_assistant_ip, home_assistant_port)
                try:
                    print('Testing Configuration')
                    self.lightChanger.changeColor(0, 255, 0, 100)
                    time.sleep(1)
                    self.lightChanger.defaultColor()
                    break
                except:
                    sg.popup('Reaching Home Assistant failed!', 'Validate your IP and Port and make sure your webhooks are configured correctly!')

        window.close()