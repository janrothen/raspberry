#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import os
import math

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

from BitcoinPriceClient import BitcoinPriceClient

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("₿ e-Paper")

    logging.info("init & clear")
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    #epd.Clear(0x00)
    WIDTH = epd.height # 250 pixels
    HEIGHT = epd.width # 122 pixels
    IMAGE_MODE = '1' # 1 (1-bit pixels, black and white, stored with one pixel per byte)
    logging.info("init complete")

    image_name = 'bitcoin122x122_b.bmp'
    image = Image.open(os.path.join(DIR_MEDIA, image_name))
    image_width, image_height = image.size
    padding_left = int((WIDTH - image_width) / 2)

    frame = Image.new(IMAGE_MODE, (WIDTH, HEIGHT))
    frame.paste(image, (padding_left,0))    
    epd.display(epd.getbuffer(frame))
    time.sleep(5)

    epd.Clear(0xFF)

    FONT_SIZE_IN_POINTS = 48 # 48 points = 64 pixels
    font_file = os.path.join(DIR_MEDIA, FONT)
    font = ImageFont.truetype(font_file, FONT_SIZE_IN_POINTS)
    FONT_SIZE = int(math.ceil(FONT_SIZE_IN_POINTS * 1.333)) # points * 1+1/3 = pixels
    logging.info(FONT_SIZE)

    frame = Image.new(IMAGE_MODE, (WIDTH, HEIGHT))
    price = ImageDraw.Draw(frame)
    padding_top = int((HEIGHT - FONT_SIZE) / 2)
    logging.info(padding_top)

    bitcoin_price_client = BitcoinPriceClient()
    logging.info(bitcoin_price_client)
    price_s = bitcoin_price_client.retrieve_price('USD')
    logging.info(price_s)

    price.text((8, 32), price_s, font = font, fill = 1)
    epd.display(epd.getbuffer(frame))
    time.sleep(5)
    
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new(IMAGE_MODE, (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        time_draw.rectangle((0, 0, WIDTH, HEIGHT), fill = 0)
        price_s = bitcoin_price_client.retrieve_price('USD')
        time_draw.text((0, 32), price_s, font = font, fill = 255)
        
        #time_draw.text((0, 32), time.strftime('%H:%M:%S'), font = font, fill = 255)
        epd.displayPartial(epd.getbuffer(time_image))
        num = num + 1
        time.sleep(5)
        if(num == 100):
            break
    # epd.Clear(0xFF)
    logging.info("Clear...")
    #epd.init(epd.FULL_UPDATE)
    #epd.Clear(0xFF)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
