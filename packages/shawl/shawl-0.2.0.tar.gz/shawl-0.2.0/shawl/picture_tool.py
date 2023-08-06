from pycloak.__picture_tool import PicHandler


class 图片工具初始化(PicHandler):
    def 计算相似度(self, 图片1, 图片2):
        return PicHandler.calc_similar(self, 图片1, 图片2)

    def 寻找图片(self, 目标图片路径, 背景图片路径):
        return PicHandler.find_pic(self, 目标图片路径, 背景图片路径)

    def 寻找坐标(self, 图片名字, 左上X=0, 左上Y=0, 右下X=0, 右下Y=0):
        return PicHandler.find_loc(self, 图片名字, 左上X, 左上Y, 右下X, 右下Y)

class PicHandler(图片工具初始化):

    def calc_similar(self, 图片1, 图片2):
        return PicHandler.calc_similar(self, 图片1, 图片2)

    def find_pic(self, 目标图片路径, 背景图片路径):
        return PicHandler.find_pic(self, 目标图片路径, 背景图片路径)

    def find_loc(self, 图片名字, 左上X=0, 左上Y=0, 右下X=0, 右下Y=0):
        return PicHandler.find_loc(self, 图片名字, 左上X, 左上Y, 右下X, 右下Y)



