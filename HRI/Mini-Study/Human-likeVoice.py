import time
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI
from spherov2.types import Color

toy = scanner.find_toy() ##Change this to the name of my robot for use in class
# with SpheroEduAPI(toy) as droid:
