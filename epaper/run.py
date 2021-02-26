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
    logging.info("init complete")

    frame = Image.new('1', (epd.height, epd.width), 0)  # 255: clear the frame
    bitcoin = Image.open(os.path.join(DIR_MEDIA, 'bitcoin122x122_b.bmp'))
    frame.paste(bitcoin, (64,0))    
    epd.display(epd.getbuffer(frame))
    time.sleep(5)

    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(DIR_MEDIA, FONT), 15)
    font36 = ImageFont.truetype(os.path.join(DIR_MEDIA, FONT), 36)
    
    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
    draw = ImageDraw.Draw(image)
    
    draw.rectangle([(0,0),(50,50)],outline = 0)
    draw.rectangle([(55,0),(100,50)],fill = 0)
    draw.line([(0,0),(50,50)], fill = 0,width = 1)
    draw.line([(0,50),(50,0)], fill = 0,width = 1)
    draw.chord((10, 60, 50, 100), 0, 360, fill = 0)
    draw.ellipse((55, 60, 95, 100), outline = 0)
    draw.pieslice((55, 60, 95, 100), 90, 180, outline = 0)
    draw.pieslice((55, 60, 95, 100), 270, 360, fill = 0)
    draw.polygon([(110,0),(110,50),(150,25)],outline = 0)
    draw.polygon([(190,0),(190,50),(150,25)],fill = 0)
    draw.text((120, 60), 'e-Paper demo', font = font15, fill = 0)
    draw.text((110, 90), u'$48''231', font = font36, fill = 0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    
    # read bmp file 
    logging.info("2.read bmp file...")
    image = Image.open(os.path.join(DIR_MEDIA, '2in13.bmp'))
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    

    
    # # partial update
    logging.info("4.show time...")
    time_image = Image.new('1', (epd.height, epd.width), 255)
    time_draw = ImageDraw.Draw(time_image)
    
    epd.init(epd.FULL_UPDATE)
    epd.displayPartBaseImage(epd.getbuffer(time_image))
    
    epd.init(epd.PART_UPDATE)
    num = 0
    while (True):
        time_draw.rectangle((120, 80, 220, 105), fill = 255)
        time_draw.text((120, 80), time.strftime('%H:%M:%S'), font = font36, fill = 0)
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
