#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import csv
import random
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
quotesdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'quotes')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in83_V2
import time
from PIL import Image,ImageDraw,ImageFont

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd5in83_V2 quotes")
    
    epd = epd5in83_V2.EPD()
    logging.info("init and Clear")
    epd.init()
    
    font48 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    quote_csv_file = open(os.path.join(quotesdir, 'quotes.csv'))
    quote_csv_reader = csv.reader(quote_csv_file)
    random_row = random.choice(list(quote_csv_reader))
    
    logging.info("Writing quote...")
    Qimage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Qimage)

    vertical = 10
    num_rows = 0
    while (len(random_row[-1])/((num_rows+1)*28)) > 1:
        start = num_rows * 28
        end = start + 27
        current_line = random_row[-1][start:end]
        draw.text((0, vertical), current_line, font = font48, fill = 0)
        num_rows += 1
        vertical += 100

    if len(random_row) == 2:
        author = random_row[0]
    else:
        author = "Unknown"
    draw.text((0, 400), author, font = font48, fill = 0)
    
    epd.display(epd.getbuffer(Qimage))
    time.sleep(10)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    draw.text((10, 20), '5.83inch e-Paper', font = font24, fill = 0)
    draw.text((150, 0), u'微雪电子', font = font24, fill = 0)    
    draw.line((20, 50, 70, 100), fill = 0)
    draw.line((70, 50, 20, 100), fill = 0)
    draw.rectangle((20, 50, 70, 100), outline = 0)
    draw.line((165, 50, 165, 100), fill = 0)
    draw.line((140, 75, 190, 75), fill = 0)
    draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    draw.rectangle((80, 50, 130, 100), fill = 0)
    draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    epd.display(epd.getbuffer(Himage))
    time.sleep(2)
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83_V2.epdconfig.module_exit()
    exit()
