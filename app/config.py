import os
import configparser

# 构建配置文件路径
file_path = os.path.join("..", "config.ini") if __name__ == "__main__" else "config.ini"

# 创建ConfigParser对象并读取配置
config = configparser.ConfigParser()
config.read(file_path)

RESERVED_IPV4 = [
    '0.0.0.0/8',
    '10.0.0.0/8',
    '100.64.0.0/10',
    '127.0.0.0/8',
    '169.254.0.0/16',
    '172.16.0.0/12',
    '192.0.0.0/24',
    '192.0.2.0/24',
    '192.88.99.0/24',
    '192.168.0.0/16',
    '198.18.0.0/15',
    '198.51.100.0/24',
    '203.0.113.0/24',
    '224.0.0.0/4',
    '233.252.0.0/24',
    '240.0.0.0/4',
    '255.255.255.255/32'
]

IPINFO_API = "http://ip-api.com/json/"

TEMPLATE_NAME = 'index.html'

# 设置默认值
default_values = {
    'app': {
        'host': 'localhost',
        'port': '8080',
        'debug': 'False',
    },
    'style': {
        'title': 'Speedtest',
        'subdomain': 'speedtest',
        'rootDomain': 'localhost.com',
        'backgroundColor': '#ffffff',
        'primaryColor': '#120d14',
    }
}

# 获取配置值，如果不存在则使用默认值
APP_HOST = config.get('app', 'host', fallback=default_values['app']['host'])
APP_PORT = config.get('app', 'port', fallback=default_values['app']['port'])
APP_DEBUG = config.getboolean('app', 'debug', fallback=default_values['app']['debug'])

STYLE_TITLE = config.get('style', 'title', fallback=default_values['style']['title'])
STYLE_SUBDOMAIN = config.get('style', 'subdomain', fallback=default_values['style']['subdomain'])
STYLE_ROOTDOMAIN = config.get('style', 'rootDomain', fallback=default_values['style']['rootDomain'])
STYLE_BACKGROUNGCOLOR = config.get('style', 'backgroundColor', fallback=default_values['style']['backgroundColor'])
STYLE_PRIMARYCOLOR = config.get('style', 'primaryColor', fallback=default_values['style']['primaryColor'])