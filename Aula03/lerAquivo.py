import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {
    'database': 'localhost',
    'dbuser': 'postgres',
    'dbpassword': '123'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)    

config.read('config.ini')
database = config['DEFAULT']['database']
print(database)