import configparser as cp

path = '/Users/seongjun/Desktop/PIM/Configuration_Files/Config1.cfg'
config = cp.ConfigParser()
config.read(path)
section = 'Save_Parameters'
a = config.get(section, 'PIM_Flag')
print(type(a))