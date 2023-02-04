from configparser import ConfigParser
file = 'config.ini'
config = ConfigParser()
config.read(file)
FORMAT = config['format']
DISPLAY_LINES = FORMAT['displayLines']
