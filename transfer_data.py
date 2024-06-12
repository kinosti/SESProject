import math

from settings import *

#from time import sleep


""" 
transfer_data.py 

Handles any and all data import/export of the process, e.g., saves and fetches the ping coordinate data.

"""


def poleCoordsToCartesian(polarCoordinates):
    # Returns Cartesian (x,y) coordinates from given polar coordinates (length, azimuth).
    # Azimuth (polar angle) should be in radians
    # NOTE: Azimuth 0 is forwards (up), not to right

    len, azimuth = polarCoordinates

    # NOTE: not tested
    x = len*math.cos(azimuth)
    y = len*math.sin(azimuth)

    return (x,y)

def fetchRelCoordinates(fromFile=False):
    # Fetches the ping location data (absolute position, no regards to user pos) and transforms them to x,y-format if needed
    # Note: does not flag if ping data has not been updated, i.e. is fetching the data as-is

    coordinates = (0,0)
    if fromFile:
        coordinates_str = ''
        while len(coordinates_str) < 3:
            with open('D:/OneDrive - Aalto University/Kurssimateriaalit/Kevät 2023/Individual Assignment - Surface Electrode Stimulation/SES project/Godot/relativeCoordinates.txt', 'r') as file:
                coordinates_str = file.read()
                if len(coordinates_str) < 3:
                    break
                coordinates_split = coordinates_str.split(",")
                coordinates = (int(coordinates_split[0]),int(coordinates_split[1]))
                #print(coordinates_str, coordinates_split, coordinates)
                #print(coordinates)

    else:
        # use this to test certain ping coordinates directly without having to write them to the coordinates file
        
        # coordinates = [
        #     (0,0),      # center
        #     (0,100),    # directly forward
        #     (100,0),    # directly to right
        #     (0,-100),   # directly behind
        #     (-100,0),   # directly to left
        #     (100,100),  # upper right corner
        #     (100,-100), # lower right corner
        #     (-100,-100),# lower left corner
        #     (-100,100), # upper left corner
        #     (200,200),  # upper right corner FAR
        #     (40,20)    # difficult timings (several low ms delays)
        #     ]

        coordinates = (40,20)
        #coordinates = (100,0)
        #coordinates = (100,100)
        #coordinates = (200,200)
        #coordinates = (200,0)
        #coordinates = (100,50)
        #coordinates = (200,100)
    
    return coordinates
