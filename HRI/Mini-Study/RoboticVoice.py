import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color
from playsound import playsound

toy = scanner.find_toy() ##Change this to the name of my robot for use in class
with SpheroEduAPI(toy) as droid:
    droid.set_main_led(Color(255, 57, 66))
    droid.spin(360, 2)
    playsound('RobotVoice.m4a')

