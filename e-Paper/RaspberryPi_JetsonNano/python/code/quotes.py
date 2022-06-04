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

    # open quote csv and choose a random row
    quote_csv_file = open(os.path.join(quotesdir, 'quotes.csv'))
    quote_csv_reader = csv.reader(quote_csv_file)
    random_row = random.choice(list(quote_csv_reader))
    
    logging.info("Writing quote...")
    Qimage = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(Qimage)
    
    # print quote
    vertical = 10
    printed_character = 0
    while printed_character <= len(random_row[-1]):
        if len(random_row[-1]) - printed_character > 28:
            end = printed_character + 28
            while random_row[-1][end] != " ":
                end -= 1
            current_line = random_row[-1][printed_character:end]
        else:
            end = printed_character + 28
            current_line = random_row[-1][printed_character:]
        
        draw.text((0, vertical), current_line, font = font48, fill = 0)
        printed_character = end + 1
        vertical += 60

    # print author
    author = random_row[0]
    if author == "":
        author = "Unknown"
    draw.text((0, 400), author, font = font48, fill = 0)
    
    # display
    epd.display(epd.getbuffer(Qimage))
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in83_V2.epdconfig.module_exit()
    exit()
