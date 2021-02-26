#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

DIR_LIB = os.path.join(DIRECTORY, 'lib')
DIR_MEDIA = os.path.join(DIRECTORY, 'media')

FONT = 'UbuntuBoldItalic-Rg86.ttf'

if os.path.exists(DIR_LIB):
    sys.path.append(DIR_LIB)

from lib import epd2in13_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("e-Paper")

    logging.info("init & clear")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    WIDTH = epd.height # 250 pixels
    HEIGHT = epd.width # 122 pixels
    logging.info("init complete")

    image_name = 'bitcoin122x122_b.bmp'
    image = Image.open(os.path.join(DIR_MEDIA, image_name))
    image_width, image_height = image.size
    padding_left = int((WIDTH - image_width) / 2)

    frame = Image.new('1', (WIDTH, HEIGHT), 0) # 255: clear the frame
    frame.paste(image, (padding_left,0))    
    epd.display(epd.getbuffer(frame))
    time.sleep(5)

    epd.Clear(0xFF)

    FONT_SIZE = 64
    font = ImageFont.truetype(os.path.join(DIR_MEDIA, FONT), FONT_SIZE)
    
    #frame = Image.new('1', (WIDTH, HEIGHT), 0)  # 255: clear the frame    
    price = ImageDraw.Draw(frame)
    padding_top = int((HEIGHT - FONT_SIZE) / 2)
    logging.info(padding_top)
    price.text((32, padding_top), u'$48''231', font = font, fill = 1)
    epd.display(epd.getbuffer(frame))
    time.sleep(5)
    
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        time_draw.rectangle((32, 32, 220, 105), fill = 255)
        time_draw.text((32, 32), time.strftime('%H:%M:%S'), font = font, fill = 0)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        if(num == 10):
            break
    # epd.Clear(0xFF)
    logging.info("Clear...")
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
