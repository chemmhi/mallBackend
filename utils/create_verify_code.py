# author=chenchen
from PIL import Image,ImageDraw,ImageFilter,ImageFont
import random

class CreateVerifyCode():
    def __init__(self,  code_length = 4,
                        size=(120, 30),
                        mode="RGB",
                        font_type="Monaco.ttf",
                        font_size=18,
                        fg_color=(0,0,255),
                        bg_color=(255,255,255),
                        n_line=(1,2),
                        draw_dot=False,
                 ):
        self.size = size,
        self.font_type = font_type
        self.font_size = font_size
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.n_line = n_line
        self.draw_dot = draw_dot
        self.width = size[0]
        self.height = size[1]
        self.code_length = code_length
        #生成白板图片
        self.img = Image.new(mode, size, color=bg_color)
        #生成画笔
        self.draw = ImageDraw.Draw(self.img)

    def generateCode(self, length):
        """
        创建一个指定长度的随机字符串
        :param length: 需要创建随机字符串的长度
        :return: 返回创建的随机字符串
        """
        lowcases = "abcdefghjkmnpqrstuvwxy"  # 去掉容易产生干扰的i,l,o,z
        uppercases = lowcases.upper()
        digital = "".join(map(str, (range(3, 10))))
        population="".join((lowcases,uppercases,digital))
        return "".join(random.sample(population,length))

    def drawCheckCode(self, checkcode):
        """
        将checkcode按指定的格式绘制在图片上
        :param checkcode: 需要绘制的文本，或者验证码
        :return: 
        """
        checkcode=" ".join(checkcode)
        font=ImageFont.truetype(self.font_type,self.font_size)
        font_width,font_height=font.getsize(checkcode)    #验证码字体的长度和宽度

        self.draw.text(
                ((self.width-font_width)/2,(self.height-font_height)/2),   #位置
                checkcode,  #文本内容
                self.fg_color,    #颜色
                font)     #使用的字体

    def drawDot(self):
        for w in range(self.width):
            for h in range(self.height):
                tem=random.randint(0,20)
                tem1=random.randint(0,20)
                if tem==tem1:
                    self.draw.point((w,h),(0,0,0))

    def drawLine(self):
        for i in self.n_line:
            begin=(random.randint(0, self.width), random.randint(0, self.height))
            end=(random.randint(0, self.width), random.randint(0, self.height))
            self.draw.line((begin,end),fill=(0,0,0))


    def start(self):
        checkcode=self.generateCode(self.code_length)   #生成验证码
        if self.draw_dot:
            self.drawDot()
        self.drawLine()
        self.drawCheckCode(checkcode)   #将验证码写入图片中

        params = [1 - float(random.randint(1, 2)) / 100,
                  0,
                  0,
                  0,
                  1 - float(random.randint(1, 10)) / 100,
                  float(random.randint(1, 2)) / 500,
                  0.001,
                  float(random.randint(1, 2)) / 500
                  ]
        size = (self.size[0][0],self.size[0][1])
        img=self.img.transform(size,Image.PERSPECTIVE,params)

        return img, checkcode

