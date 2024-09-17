import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

toy = scanner.find_toy() ##Change this to the name of my robot for use in class
with SpheroEduAPI(toy) as droid:
    # droid.set_back_led(255)

    ###Code for Hello in Morse Code

    ###Brief explanation of my Morse Code
    ##Dots - quickly blink once
    ##Dashes - blink 3 times longer than a dot
    ##Letters made up of multiple dots and dashes
    ##Sleep for 1 second between every letter and 2 seconds between every word


    ##H -- 4 dots (blinks) in a row
    droid.strobe(Color(255, 57, 66), (1 / 9), 4)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##E - A single blink
    droid.strobe(Color(0, 57, 66), (1 / 9), 1)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ###L - 1 dot, followed by 1 dash(stays 3 times longer than a dot), followed by 2 dots
    droid.strobe(Color(255, 57, 66), (1 / 9), 1) # First dot in L
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # First dash in L
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 9), 2) # Last 2 dots in L
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##Second L  same as the first L
    ##Note, the time is longer than 3 times to be able to show the difference between a dash and dot
    droid.strobe(Color(0, 57, 66), (1 / 9), 1) # First dot in L
    droid.strobe(Color(0, 57, 66), (1 / 3), 1) # First dash in L
    time.sleep(.5)
    droid.strobe(Color(0, 57, 66), (1 / 9), 2) # Last 2 dots in L
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##O - 3 dashes
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # First dash in O
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Second dash in O
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Third dash in O
    time.sleep(.5)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(2)

    droid.spin(360, 5)


    ##Morse code for Saying "I am Sphero"
    ##I apologize for whoever is grading this.

    ##I - 2 dots
    droid.strobe(Color(255, 57, 66), (1 / 9), 2) # 2 dots for I
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(2)

    ##A - 1 dot, followed by 1 dash
    droid.strobe(Color(0, 57, 66), (1 / 9), 1) # First dot in A
    time.sleep(.5)
    droid.strobe(Color(0, 57, 66), (1 / 3), 1) # First dash in A
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##M - 2 dashes
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # First dash in M
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Second dash in M
    droid.set_main_led(Color(0, 0, 0))

    ##Update: I am ___

    time.sleep(2)

    ##S - 3 dots
    droid.strobe(Color(0, 57, 66), (1 / 9), 3) # 3 dots in S
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##P - 1 dot, followed by 2 dashes and then 1 dot
    droid.strobe(Color(255, 57, 66), (1 / 9), 1) # First dot in P
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # First dash in P
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Second dash in P
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 9), 1) # Last dot in P
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##H - 4 dots (blinks) in a row
    droid.strobe(Color(0, 57, 66), (1 / 9), 4)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##E - A single blink
    droid.strobe(Color(255, 57, 66), (1 / 9), 1)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##R - 1 dot, followed by 1 dash and then 1 dot
    droid.strobe(Color(0, 57, 66), (1 / 9), 1) # First dot in R
    droid.strobe(Color(0, 57, 66), (1 / 3), 1) # First dash in R
    time.sleep(.5)
    droid.strobe(Color(0, 57, 66), (1 / 9), 1) # Last dot in R
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(1)

    ##O - 3 dashes
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # First dash in O
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Second dash in O
    time.sleep(.5)
    droid.strobe(Color(255, 57, 66), (1 / 3), 1) # Third dash in O
    time.sleep(.5)
    droid.set_main_led(Color(0, 0, 0))
    time.sleep(2)

    ###Moving forwards and backwards at the end    
    droid.set_speed(40)
    time.sleep(1)
    droid.set_speed(-40)
    time.sleep(1)
    droid.set_speed(0)
