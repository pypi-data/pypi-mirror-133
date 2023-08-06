from pycloak.__adb_util import AdbCommand


class 手机操作(AdbCommand):
    @staticmethod
    def 获取设备列表():
        return AdbCommand.get_devices_list()

    def 设备是否连接(self):
        return AdbCommand.is_device_connected(self)

    def 执行adb命令(self, 内容):
        return AdbCommand.execute(self, 内容)

    def 截图(self):
        return AdbCommand.capture(self)

    def 启动app(self, 包名):
        return AdbCommand.runapp(self,包名)

    def 获取前台包名(self):
        return AdbCommand.get_front_app(self)

    def 判断APP是否安装(self, 包名):
        return AdbCommand.app_in(self, 包名)

    def 输入文字(self, 输入内容):
        return AdbCommand.input_text(self, 输入内容)

    def 按键输入(self, 输入键码):
        return AdbCommand.input_keyevent(self, 输入键码)

    def 设置屏幕常亮(self):
        return AdbCommand.screen_off_timeout(self)

    def 获取app安装版本(self, 包名):
        return AdbCommand.get_app_verison(self, 包名)

    def 检查互联网连接(self,重试次数 = 1, 国家 = 'cn'):
        return AdbCommand.check_internet(self, retry= 重试次数, country= 国家)

    def 检查VPN连接(self):
        return AdbCommand.check_vpn_connect(self)

    def 检查系统是否启动完成(self):
        return AdbCommand.check_boot_completed(self)

    def 点亮屏幕(self):
        return AdbCommand.up_screen(self)

    def 获取进程列表(self):
        return AdbCommand.psef(self)

    def 查找进程pid(self, 进程名):
        return AdbCommand.find_pid(self, 进程名)

    def 结束进程(self, pid):
        return AdbCommand.kill_pid(self, pid)

    def 获取wifiIP(self):
        return AdbCommand.get_wifi_ip(self)

    def 通过wifi连接电脑(self, 连接端口):
        return AdbCommand.wifi_adb_connect(self, 连接端口)

    def 发送文件(self, 电脑路径, 手机保存路径):
        return AdbCommand.push_file(self, 电脑路径, 手机保存路径)

    def 拉取手机文件(self, 手机文件路径, 电脑保存路径):
        return AdbCommand.pull_file(self,手机文件路径, 电脑保存路径)

    def 判断文件是否存在(self, 手机文件路径):
        return AdbCommand.file_exist(self, 手机文件路径)

    def 读取手机文件(self, 手机文件路径):
        return AdbCommand.read_file(self, 手机文件路径)

    def 写入手机文件(self, 手机文件路径, 写入内容):
        return AdbCommand.write_file(self, 手机文件路径, 写入内容)

    def 追加写入手机文件(self, 手机文件路径, 追加内容):
        return AdbCommand.append_file(self, 手机文件路径, 追加内容)

    def 删除手机文件(self, 手机文件路径):
        return AdbCommand.del_file(self, 手机文件路径)

    def 获取目录下文件名(self, 手机文件目录):
        return AdbCommand.get_listdir(self, 手机文件目录)

    def 重启手机(self):
        return AdbCommand.reboot(self)

    def 关机(self):
        return AdbCommand.shutdown(self)

    def 安装app(self, app路径):
        return AdbCommand.install(self, app路径)

    def 读取剪切板(self):
        return AdbCommand.get_clipper(self)

    def 设置剪切板内容(self,内容):
        return AdbCommand.set_clipper(self, 内容)

    def 点击(self,坐标点, 压力=100, 持续时间=None, 不弹起=None):
        AdbCommand.tap(self, 坐标点, pressure=压力, duration=持续时间, no_up=不弹起)

    def 滑动(self, 坐标点, 压力=100, 持续时间=None, 不下按 = None, 不弹起=None):
        AdbCommand.swipe(self, 坐标点, pressure=压力, no_down = 不下按, duration=持续时间, no_up=不弹起)

    def 精确滑动(self, 坐标点, 压力=100, 持续时间=None, 滑动区间 = None, 不下按 = None, 不弹起=None):
        AdbCommand.ext_smooth_swipe(self, 坐标点, pressure=压力, duration=持续时间, part=滑动区间, no_down=不下按, no_up=不弹起)


class AdbCommand(手机操作):
    @staticmethod
    def get_devices_list():
        return AdbCommand.get_devices_list()

    def is_device_connected(self):
        return AdbCommand.is_device_connected(self)

    def execute(self, 内容):
        return AdbCommand.execute(self, 内容)

    def capture(self):
        return AdbCommand.capture(self)

    def runapp(self,包名):
        return AdbCommand.runapp(self,包名)

    def get_front_app(self):
        return AdbCommand.get_front_app(self)

    def app_in(self, 包名):
        return AdbCommand.app_in(self, 包名)

    def input_text(self, 输入内容):
        return AdbCommand.input_text(self, 输入内容)

    def input_keyevent(self, 输入键码):
        return AdbCommand.input_keyevent(self, 输入键码)

    def screen_off_timeout(self):
        return AdbCommand.screen_off_timeout(self)

    def get_app_verison(self, 包名):
        return AdbCommand.get_app_verison(self, 包名)

    def check_internet(self,重试次数 = 1, 国家 = 'cn'):
        return AdbCommand.check_internet(self, retry= 重试次数, country= 国家)

    def check_vpn_connect(self):
        return AdbCommand.check_vpn_connect(self)

    def check_boot_completed(self):
        return AdbCommand.check_boot_completed(self)

    def up_screen(self):
        return AdbCommand.up_screen(self)

    def psef(self):
        return AdbCommand.psef(self)

    def find_pid(self, 进程名):
        return AdbCommand.find_pid(self, 进程名)

    def kill_pid(self, pid):
        return AdbCommand.kill_pid(self, pid)

    def get_wifi_ip(self):
        return AdbCommand.get_wifi_ip(self)

    def wifi_adb_connect(self, 连接端口):
        return AdbCommand.wifi_adb_connect(self, 连接端口)

    def push_file(self, 电脑路径, 手机保存路径):
        return AdbCommand.push_file(self, 电脑路径, 手机保存路径)

    def pull_file(self, 手机文件路径, 电脑保存路径):
        return AdbCommand.pull_file(self,手机文件路径, 电脑保存路径)

    def file_exist(self, 手机文件路径):
        return AdbCommand.file_exist(self, 手机文件路径)

    def read_file(self, 手机文件路径):
        return AdbCommand.read_file(self, 手机文件路径)

    def write_file(self, 手机文件路径, 写入内容):
        return AdbCommand.write_file(self, 手机文件路径, 写入内容)

    def append_file(self, 手机文件路径, 追加内容):
        return AdbCommand.append_file(self, 手机文件路径, 追加内容)

    def del_file(self, 手机文件路径):
        return AdbCommand.del_file(self, 手机文件路径)

    def get_listdir(self, 手机文件目录):
        return AdbCommand.get_listdir(self, 手机文件目录)

    def reboot(self):
        return AdbCommand.reboot(self)

    def shutdown(self):
        return AdbCommand.shutdown(self)

    def install(self, app路径):
        return AdbCommand.install(self, app路径)

    def get_clipper(self):
        return AdbCommand.get_clipper(self)

    def set_clipper(self,内容):
        return AdbCommand.set_clipper(self, 内容)

    def tap(self,坐标点, 压力=100, 持续时间=None, 不弹起=None):
        AdbCommand.tap(self, 坐标点, pressure=压力, duration=持续时间, no_up=不弹起)

    def swipe(self, 坐标点, 压力=100, 持续时间=None, 不下按 = None, 不弹起=None):
        AdbCommand.swipe(self, 坐标点, pressure=压力, no_down = 不下按, duration=持续时间, no_up=不弹起)

    def ext_smooth_swipe(self, 坐标点, 压力=100, 持续时间=None, 滑动区间 = None, 不下按 = None, 不弹起=None):
        AdbCommand.ext_smooth_swipe(self, 坐标点, pressure=压力, duration=持续时间, part=滑动区间, no_down=不下按, no_up=不弹起)



