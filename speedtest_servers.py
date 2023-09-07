from sqlite_server import Speedtest
ObjSpeedtest = Speedtest()

objData = ObjSpeedtest.get_servers()
ServerList = [i for i in objData]



if __name__ == '__main__':
    ObjSpeedtest.add_speedtest_log()