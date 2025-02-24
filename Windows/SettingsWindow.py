import PySimpleGUI as sg
import time

import Utils.ConfigurationManager as ConfigurationManager, Utils.ILightChanger as ILightChanger, Utils.Mode as Mode
from Utils.YeeLightBulbFinder import YeeLightBulbFinder
from Utils.LightChangerResolver import LightChangerResolver

class SettingsWindow:
    def __init__(self, configManager : ConfigurationManager, lightChangerResolver: LightChangerResolver, yeeLightBulbFinder: YeeLightBulbFinder):
        self.configManager = configManager
        self.lightChangerResolver = lightChangerResolver
        self.lightChanger = self.lightChangerResolver.getLightChanger()
        self.yeeLightBulbFinder = yeeLightBulbFinder
        self.defaultYeelightIPs = ['Press Discover to find bulbs!']

    def renderLayout(self):
        config = self.configManager.read()

        mode = config['MODE']['mode']
        home_assistant_ip = config['HOME ASSISTANT']['home_assistant_ip']
        home_assistant_port = config['HOME ASSISTANT']['home_assistant_port']
        yeelight_ip = config['YEELIGHT']['yeelight_ip']
        wled_ip = config['WLED']['wled_ip']
        
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
                ],
                [
                    sg.Text('Bulbs in your LAN', tooltip = 'Automatically discovered yeelight bulbs in your LAN.'), 
                    sg.Button('Discover', tooltip = 'Automatically discovers yeelight bulbs in your LAN.'),
                    sg.Combo(values = self.defaultYeelightIPs, disabled = self.defaultYeelightIPs[0] == 'Press Discover to find bulbs!', default_value = self.defaultYeelightIPs[0], expand_x = True, auto_size_text = True, enable_events = True, key = 'DISCOVERED-BULBS-LIST')
                ]
            ]
        elif str(mode) == str(Mode.Mode.WLED.name):
            modeConfigLayout = [
                [
                    sg.Text('WLED IP', tooltip = 'The local address of your WLED instance.'), 
                    sg.InputText(default_text = wled_ip, key = 'WLED-IP')
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
            if event == 'DISCOVERED-BULBS-LIST':
                ip = values['DISCOVERED-BULBS-LIST']
                window.Element('YEELIGHT-IP').update(value = ip)
            if event == 'Discover':
                bulbs = self.yeeLightBulbFinder.findBulbs()
                self.defaultYeelightIPs = bulbs
                if len(bulbs) == 0:
                    sg.popup('No bulbs found!', 'Make sure your bulbs are on and connected to the same network.')
                else:
                    window.Element('DISCOVERED-BULBS-LIST').update(values = bulbs, value = bulbs[0], disabled = False)
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
                elif str(mode) == str(Mode.Mode.WLED.name):
                    wled_ip = values['WLED-IP']
                    self.configManager.writeWLEDConfig(wled_ip)
                
                self.lightChanger = self.lightChangerResolver.getLightChanger()

                try:
                    print('Testing Configuration')
                    self.lightChanger.changeColor(0, 255, 0)
                    time.sleep(1)
                    self.lightChanger.defaultColor()
                    break
                except:
                    if str(mode) == str(Mode.Mode.HomeAssistant.name):
                        sg.popup('Reaching Home Assistant failed!', 'Validate your IP and Port and make sure your webhooks are configured correctly!')
                    elif str(mode) == str(Mode.Mode.Yeelight.name):
                        sg.popup('Reaching Yeelight Bulb failed!', 'Validate your IP and make sure your bulb is on & connected!')
                    elif str(mode) == str(Mode.Mode.WLED.name):
                        sg.popup('Reaching WLED failed!', 'Validate your IP and make sure your WLED instance is on!')

        window.close()