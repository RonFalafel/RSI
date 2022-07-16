import configparser

class ConfigurationManager:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def write(self, home_assistant_ip, home_assistant_port):
        self.config['HOME ASSISTANT'] = {'home_assistant_ip': home_assistant_ip, 'home_assistant_port': home_assistant_port}
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def read(self):
        try:
            self.config.read('config.ini')
            return self.config
        except:
            print('Reading config failed, writing new config instead.')
            self.write('192.168.1.123', '8123') # Default home assistant values