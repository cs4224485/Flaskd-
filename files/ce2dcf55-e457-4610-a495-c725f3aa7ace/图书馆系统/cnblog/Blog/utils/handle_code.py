# Author: harry.cai
# DATE: 2018/6/21
import random
from PIL import Image, ImageDraw, ImageFont


class CheckCode:
    '''
    生成图片验证码
    '''
    def generation_code(self):
        valid_code = ''
        for i in range(4):
            string_low = chr(random.randint(97, 122))
            string_upper = chr(random.randint(65, 90))
            num = str(random.randint(0,9))
            code = random.choice([string_low, string_upper, num])
            valid_code += code
        return valid_code

    def get_random_color(self):

        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    def generation_img(self):

        img = Image.new("RGB", (200, 40), color=self.get_random_color())
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('static/font/waterlily.ttf', size=30)
        check_code = self.generation_code()
        i = 1
        for c in check_code:
            draw.text((i*40, 4), c, self.get_random_color(), font=font )
            i = i+1

        width = 200
        height = 40
        for i in range(5):
            x1 = random.randint(0, width)
            x2 = random.randint(0, width)
            y1 = random.randint(0, height)
            y2 = random.randint(0, height)
            draw.line((x1, y1, x2, y2), fill=self.get_random_color())
        for i in range(5):
            draw.point([random.randint(0, width), random.randint(0, height)], fill=self.get_random_color())
            x = random.randint(0, width)
            y = random.randint(0, height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.get_random_color())

        return img, check_code



