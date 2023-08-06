from pycloak.adb_util import AdbCommand
from pycloak.picture_tool import PicHandler
from . import __connect

def 获取设备列表():
    return __connect.get_devices_list()

def 设备连接初始化(设备号, 截图保存路径, 截图质量=100)->AdbCommand:
    return __connect.init_device(设备号, 截图保存路径, 截图质量)

def wifi连接设备(设备号):
    return __connect.wifi_adb_connect(设备号)


def 图片工具初始化(设备号, 对比图片文件夹路径, 截图文件夹路径)->PicHandler:
    return __connect.init_pic_handler(设备号, 对比图片文件夹路径, 截图文件夹路径)




if __name__ == '__main__':
    设备 = 获取设备列表()[0]
    设备连接初始化(设备,r'D:\desktop\cap_pic')
