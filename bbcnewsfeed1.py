#!/usr/bin/python3.7

# BBC News RSS Feed Scrolling Headline(s) on 16x2 LCD Display

# Use Python3 - clone and install all necessary modules using pip3
# Run program using command: python3 bbcnewsfeed1.py

# With thanks to the following for their contributions: 

# Adafruit
# remember to import custom Adafruit_CharLCD
# remember to define RPi GPIO pins correctly for your setup
# Original tutorial adafruit
# http://learn.adafruit.com/drive-a-16x2-lcd-directly-with-a-raspberry-pi

# Tom's Hardware
# https://www.tomshardware.com/uk/how-to/raspberry-pi-rss-news-ticker?region-switch=1603318021

# ElectronicsHobbyists for Scroll Function
# https://electronicshobbyists.com/raspberry-pi-lcd-display-interfacing/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep
import Adafruit_CharLCD as LCD
import feedparser 
#import textwrap
bbc = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml?edition=uk")

# Raspberry Pi GPIO pin setup for communication with lcd 
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4 ###Not controlled in this program###


# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2

# Define lcd and which pins on lcd to use
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
sleep(1)


# Get first main headline information from BBC and save it to an object named bbc.
# If you change it to (2) lcd will display only the second headline.
for i in range(1):
    print(bbc[('entries')][i][('title')]) ###Prints headline to computer screen.###
    message = (bbc['entries'][i]['title'], 2) ###Sends it to lcd###

# Scroll across lcd
try:

    while True:
            lcd.message(bbc[('entries')][i][('title')])
            sleep(1)

except KeyboardInterrupt: ### If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup###
        print("Cleaning up!")
        lcd.clear()
