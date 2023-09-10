import configparser

file_path = "../config.ini" if __name__ == "__main__" else "config.ini"

config = configparser.ConfigParser()
config.read(file_path)

APP_HOST = config.get('app','host')
APP_PORT = config.get('app','port')
APP_DEBUG = config.get('app','debug')

STYLE_TITLE = config.get('style','title')
STYLE_SUBDOMAIN = config.get('style','subdomain')
STYLE_ROOTDOMAIN = config.get('style','rootDomain')
STYLE_BACKGROUNGCOLOR = config.get('style','backgroundColor')
STYLE_PRIMARYCOLOR = config.get('style','primaryColor')