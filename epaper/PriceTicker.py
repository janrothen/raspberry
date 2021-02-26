    
#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import math

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

DIR_LIB = os.path.join(DIRECTORY, 'lib')
DIR_MEDIA = os.path.join(DIRECTORY, 'media')

if os.path.exists(DIR_LIB):
    sys.path.append(DIR_LIB)

from lib import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

class PriceTicker(object):
    def __init__(self, price_client):
        self.price_client = price_client

        self.WIDTH = 0
        self.HEIGHT = 0
        self.IMAGE_MODE = '1' # 1 (1-bit pixels, black and white, stored with one pixel per byte)

        self.init_epd()

    def init_epd(self):
        self.epd = epd2in13_V2.EPD()
        self.epd.init(self.epd.FULL_UPDATE)

        self.WIDTH = self.epd.height # 250 pixels
        self.HEIGHT = self.epd.width # 122 pixels

    def wait(self):
        time.sleep(5)

    def clear_display(self):
        self.epd.Clear(0xFF)

    def run(self):
        #self.display_image()
        #self.wait()
        #self.clear_display()
        self.display_price()

    def display_image(self):
        image = self.load_image()
        image_width, image_height = image.size
        padding_left = int((self.WIDTH - image_width) / 2)

        frame = self.create_frame()
        frame.paste(image, (padding_left,0))    
        
        self.epd.display(self.epd.getbuffer(frame))

    def load_image(self):
        try:
            image_file_name = 'bitcoin122x122_b.bmp'
            return Image.open(os.path.join(DIR_MEDIA, image_file_name))
        except IOError as e:
            logging.error(e)    

    def load_font(self):
        try:
            font_file_name = 'UbuntuBoldItalic-Rg86.ttf'
            font_file = os.path.join(DIR_MEDIA, font_file_name)
            FONT_SIZE_IN_POINTS = 48 # 48 points = 64 pixels
            return ImageFont.truetype(font_file, FONT_SIZE_IN_POINTS)
        except IOError as e:
            logging.error(e)    


    def create_frame(self):
        return Image.new(self.IMAGE_MODE, (self.WIDTH, self.HEIGHT))

    def display_price(self):
        try:
            font = self.load_font()
            font_size = int(math.ceil(font.size * 1.333)) # points * 1+1/3 = pixels

            image = Image.new(self.IMAGE_MODE, (self.epd.height, self.epd.width), 255)
            time_draw = ImageDraw.Draw(image)
            
            #self.epd.init(self.epd.FULL_UPDATE)
            #self.epd.displayPartBaseImage(self.epd.getbuffer(image))
            
            self.epd.init(self.epd.PART_UPDATE)
            num = 0
            while (True):
                time_draw.rectangle((0, 0, self.WIDTH, self.HEIGHT), fill = 0)
                price_s = self.price_client.retrieve_price()
                time_draw.text((8, 32), price_s, font = font, fill = 255)
                
                #time_draw.text((0, 32), time.strftime('%H:%M:%S'), font = font, fill = 255)
                self.epd.displayPartial(self.epd.getbuffer(image))
                num = num + 1
                time.sleep(15)
                if(num == 100):
                    break
            # epd.Clear(0xFF)
            logging.info("Clear...")
            #epd.init(epd.FULL_UPDATE)
            #epd.Clear(0xFF)
            
            logging.info("Goto Sleep...")
            self.epd.sleep()
        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd2in13_V2.epdconfig.module_exit()
            exit()
