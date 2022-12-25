import PySimpleGUI as sg
import time

import Utils.ConfigurationManager as ConfigurationManager, Utils.ILightChanger as ILightChanger, Utils.Mode as Mode
from Utils.LightChangerResolver import LightChangerResolver
from Utils.HALightChanger import HALightChanger
from Utils.YeeLightChanger import YeeLightChanger

class SettingsWindow:
    def __init__(self, configManager : ConfigurationManager, lightChangerResolver: LightChangerResolver):
        self.configManager = configManager
        self.lightChangerResolver = lightChangerResolver
        self.lightChanger = self.lightChangerResolver.getLightChanger()

    def renderLayout(self):
        config = self.configManager.read()
        mode = config['MODE']['mode']
        home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
        home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
        yeelight_ip = config['YEELIGHT']['yeelight_ip']
        
        modeConfigLayout = []

        if str(mode) == str(Mode.Mode.HomeAssistant.name):
            modeConfigLayout = [
                [
                    sg.Text('Home Assistant IP', tooltip = 'The local address of your Home Assistant.'), 
                    sg.InputText(default_text = home_assistant_ip, key = 'HOME-ASSISTANT-IP')
                ],
                [
                    sg.Text('Home Assistant Port:', tooltip = 'The port of your Home Assistant (8123 by default).'), 
                    sg.InputText(default_text = home_assistant_port, key = 'HOME-ASSISTANT-PORT')
                ]
            ]
        elif str(mode) == str(Mode.Mode.Yeelight.name):
            modeConfigLayout = [
                [
                    sg.Text('Yeelight bulb IP', tooltip = 'The local address of your Yeelight lightbulb.'), 
                    sg.InputText(default_text = yeelight_ip, key = 'YEELIGHT-IP')
                ]
            ]

        modes = [e.name for e in Mode.Mode]

        defaultButtons = [
                [
                    sg.Button('Default', tooltip = 'Returns all default values.'), 
                    sg.Combo(values = modes, default_value = [mode], auto_size_text = True, key = 'MODE', enable_events = True, tooltip = 'Switches between yeelight mode to homme assistant mode.'),
                    sg.Button('Save', tooltip = 'Validates and saves the new configuration.'), 
                    sg.Button('Cancel', tooltip = 'Closes the settings window.'), 
                ]
            ]

        modeConfigLayout.append(defaultButtons)

        window = sg.Window('Settings', modeConfigLayout)
        return window
    
    def showSettingsWindow(self):
        window = self.renderLayout()        

        while True:
            event, values = window.read()
            if event == 'Default':
                self.configManager.default()
                window.close()
                window = self.renderLayout()        
            if event == 'MODE':
                mode = values['MODE']
                self.configManager.writeMode(mode)
                window.close()
                window = self.renderLayout()   
            if event in ('Cancel', sg.WIN_CLOSED):
                break
            if event == 'Save':
                mode = values['MODE']
                if str(mode) == str(Mode.Mode.HomeAssistant.name):
                    home_assistant_ip = values['HOME-ASSISTANT-IP']
                    home_assistant_port = values['HOME-ASSISTANT-PORT']
                    self.configManager.writeHAConfig(home_assistant_ip, home_assistant_port)
                elif str(mode) == str(Mode.Mode.Yeelight.name):
                    yeelight_ip = values['YEELIGHT-IP']
                    self.configManager.writeYeelightConfig(yeelight_ip)
                
                self.lightChanger = self.lightChangerResolver.getLightChanger()

                try:
                    print('Testing Configuration')
                    self.lightChanger.changeColor(0, 255, 0, 100)
                    time.sleep(1)
                    self.lightChanger.defaultColor()
                    break
                except:
                    sg.popup('Reaching Home Assistant failed!', 'Validate your IP and Port and make sure your webhooks are configured correctly!')

        window.close()