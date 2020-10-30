
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

# https://circuitdigest.com/microcontroller-projects/voice-to-text-typing-using-raspberry-pi for how to split text

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep
import Adafruit_CharLCD as LCD
import textwrap
import feedparser
import re

# Raspberry Pi GPIO pin setup for communication with lcd
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 4 # Not controlled in this project.

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


# Create object bbc to store the bbc's rss feed data
bbc = feedparser.parse("http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml")

# Define and activate lcd and which pins on lcd to use
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
sleep(1)


# Get x number of headlines from feed data and print to monitor.
for i in range(2):
    s = (bbc['entries'][i]['title']) # Define string as 's'
    print(s)

# Print “BBC News" to the first line of the LCD.
lcd.message('BBC News')
sleep(3)
lcd.clear()

# Create a loop to print the contents of the split object to the LCD screen.

try: 
    while True:

        for i in range(1): # Works best if you scroll only the first headline.
            w = 72 # Create an object called 'w' and use that to save character chunks of the RSS feed. Best with number of characters in headline. 
            s = (bbc['entries'][i]['title']) # Define string of incoming news.
            s = f'{s: <{w}}' # Format string, with left justification.
            s = ''.join(s[i:i+72] for i in range(0, len(s), 72)) # Ensure string chunks are 16 characters long, joined with a space.
            s = ((re.sub('([A-Z])', r' \1', s,))) # String 's', putting a space before every capital letter.
#
            lcd.move_left() # Direction of scroll, one character at a time.

            if (len(s)>16): # If the length of the string is greater than 16 characters ...
                a,b = s[:36],s[36:] # Divide it into 2 parts, a & b, each of half the width of the feed.
                lcd.message(a) #  Displays first half.
                lcd.message('\n') # Creates a line break.
                lcd.message(b) # Displays second half.
            else:
                lcd.message(s) # If headline has fewer than 16 characters, its string will not be split in half.

            sleep(0.3) # Controls speed of headline scroll. Increase sleep to slow it down.

except KeyboardInterrupt: # If there is a KeyboardInterrupt by pressing Ctrl+C, exit the program and cleanup.
    print("Cleaning up!")
    lcd.clear()
