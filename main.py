from pyacmi import *

if __name__ == '__main__':
    acmi = Acmi()
    acmi.load_acmi(filepath='test.acmi')
    print(acmi)
