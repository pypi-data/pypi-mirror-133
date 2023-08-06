from pycloak.adb_util import AdbCommand
from pycloak.picture_tool import PicHandler
from . import __connect

def get_devices_list():
    return __connect.get_devices_list()

def init_device(serialno, pic_save_path,picture_nature=100)->AdbCommand:
    return __connect.init_device(serialno, pic_save_path,picture_nature)

def wifi_adb_connect(serialno):
    return __connect.wifi_adb_connect(serialno)


def init_pic_handler(serialno, contr_path, cap_path)->PicHandler:
    return __connect.init_pic_handler(serialno, contr_path, cap_path)

