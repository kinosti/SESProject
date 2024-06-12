import math
import numpy as np
import scipy as sp
from helpers import printf
#import time

from settings import *

""" 
ping_to_data.py (ex. Gaussian3x3.py)

Handles the creation of the pulse sequence data from the given ping location. "getPulseSequenceData"-func handles the full process and returns the data-dict.
"""


def EuclideanDistance(p1,p2):
    # returns Euclidean distance between points. Includes Z if given

    x1, y1, *z1 = p1
    x2, y2, *z2 = p2

    if len(z1)!=len(z2) or len(z1)>1:
        raise Exception("Incorrect argument sizes")

    if len(z1)==0:
        z1=z2=0

    return math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


def locationToElectrodes(location):
    # from sensed stimulation locations to associated anodes/cathodes

    if P_SIZE == 8: 
        # New array of 16 electrodes arranged in pairs of 2 (as 2 rows of 8 electrodes). 
        # Pin 4 is the first pin in use as first 3 are not connected to used electrodes.
        # The electrodes are mapped in order always from left to right but for the first half the electode pairs are ordered bottom-top but then order changes to top-bottom

        anodesCathodes = {
        0: ([10],[12]), # ([13],[11]), neither one is "proper" as the electrodes here are aligned diagonally # NOTE: is the localization pulse
        1: ([18],[19]), # top-bottom (the right-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        2: ([16],[17]), # top-bottom
        3: ([14],[15]), # bottom-top
        4: ([12],[13]), # bottom-top
        5: ([10],[11]), # top-bottom (order swith at the midpoint of the array)
        6: ([8],[9]), # top-bottom
        7: ([6],[7]), # bottom-top
        8: ([4],[5]) # bottom-top (the left-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        }
   
    elif P_SIZE == 7: 
        anodesCathodes = {
        0: ([10],[12]), # ([13],[11]), neither one is "proper" as the electrodes here are aligned diagonally # NOTE: is the localization pulse
        1: ([18],[19]), # top-bottom (the right-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        2: ([16],[17]), # top-bottom
        3: ([14],[15]), # bottom-top
        4: ([8],[9]), # top-bottom
        5: ([6],[7]), # bottom-top
        6: ([4],[5]), # bottom-top (the left-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        7: ([10],[12]) # bottom-top (the left-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        }
        
    elif P_SIZE == 6: 
        anodesCathodes = {
        0: ([10],[12]), # ([13],[11]), neither one is "proper" as the electrodes here are aligned diagonally # NOTE: is the localization pulse
        1: ([18],[19]), # top-bottom (the right-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        2: ([16],[17]), # top-bottom
        3: ([14],[15]), # bottom-top
        4: ([8],[9]), # top-bottom
        5: ([6],[7]), # bottom-top
        6: ([4],[5]) # bottom-top (the left-most electrode pair if device is correct-face-up and port&electrode pad is facing away)
        }
    elif P_SIZE == 9:
        anodesCathodes = {
        0: ([7],[8]), # NOTE: is the localization pulse
        1: ([3],[4]), # ~=(1,2), mutta +2
        2: ([10],[7]),
        3: ([11],[14]),
        4: ([4],[5]),
        5: ([7],[8]),
        6: ([14],[13]),
        7: ([6],[5]),
        8: ([9],[8]),
        9: ([12],[13])
    }
    elif P_SIZE == 5:
        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([3],[4]),
            2: ([6],[5]),
            3: ([18],[17]),
            4: ([15],[16]),
            5: ([8],[14])
        }
    elif P_SIZE == 4:
        """
        anodesCathodes = {
            0: ([8],[10]), # NOTE: is the localization pulse
            1: ([11],[3]),
            2: ([3],[5]),
            3: ([5],[13]),
            4: ([11],[13])
        }
        """

        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([3],[4]),
            2: ([6],[5]),
            3: ([18],[17]),
            4: ([15],[16])
        }
    elif P_SIZE == 3:
        """
        anodesCathodes = {
            0: ([8],[10]), # NOTE: is the localization pulse
            1: ([10],[11]),
            2: ([5],[6]),
            3: ([16],[15])
        }
        anodesCathodes = {
            0: ([8],[10]), # NOTE: is the localization pulse
            1: ([3],[18]),
            2: ([3],[6]),
            3: ([18],[15])
        }
        anodesCathodes = {
            0: ([7],[8]), # NOTE: is the localization pulse
            1: ([10],[9]),
            2: ([3],[6]),
            3: ([11],[12])
        }
        anodesCathodes = {
            0: ([8],[14]), # NOTE: is the localization pulse
            1: ([10],[11]),
            2: ([6],[5]),
            3: ([15],[16])
        }
        """
        # OG:
        anodesCathodes = {
            0: ([8],[14]), # NOTE: is the localization pulse
            1: ([4],[10]),
            2: ([8],[14]),
            3: ([12],[16])
        }
        """
        # TESTI:
        anodesCathodes = {
            0: ([4],[5]), # NOTE: is the localization pulse
            1: ([3],[4]),
            2: ([10],[7]),
            3: ([11],[14])
        }
        """
    elif P_SIZE == 2:
        """
        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([3],[6]),
            2: ([18],[15])
        }
        # OG:
        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([18],[15]),
            2: ([3],[6])
        }

        # TESTI:
        anodesCathodes = {
            0: ([4],[5]), # NOTE: is the localization pulse
            1: ([3],[4]),
            2: ([6],[5])
        }
        """
        # TESTI:
        anodesCathodes = {
            0: ([4],[5]), # NOTE: is the localization pulse
            #1: ([10],[7]),
            #2: ([11],[14])
            1: ([3],[10]),
            #2: ([3],[4])
            2: ([4],[7])
        }


        """
        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([4],[6]),
            2: ([17],[15])
        }
        anodesCathodes = {
            0: ([8],[13]), # NOTE: is the localization pulse
            1: ([5],[6]),
            2: ([16],[15])
        }
        """
    elif P_SIZE == 1:
        anodesCathodes = {
            1: ([3],[4])
        }
    else:
        raise Exception("Not implemented yet / wrong P_SIZE")

    return anodesCathodes[location]


def calcGaussianCoeffLookupTable():
    # Calculates a gaussian-distribution lookup table (as sp.stats.norm.sf is too slow to do it "online")

    coeffLookupTable = {}
    
    for zScore in np.arange(0.00,3.01,0.01):
        percentageBetween = 1-2*sp.stats.norm.sf(zScore) # [%/100] percentage between -x...x
        reductionCoeff = 1-percentageBetween # coeff (0...1) to multiply the amplitude
        coeffLookupTable[zScore] = round(reductionCoeff,3)

    return coeffLookupTable


def lookupGaussianCoeff(lookupTable, sigma, x):
    # Returns the corresponding intensity coefficient to given value 'x'
    # sigma = stddev, x = value
    
    # mu = mean, zero-mean used here always
    mu = 0 
    zScore = round((x-mu)/sigma,2)

    if zScore in lookupTable:
        coeff = lookupTable[zScore]
    else:
        coeff = GAUSS_COEFF_MIN

    return coeff


def calcDistances(coordinates):
    # Calculate distances from the ping to each of the coordinates. 
    # In addition to abs.dist, also returns the relative distances, where the shortest distance d0 has been subtracted from all values (to have the first pulse triggering at t0=0).
    # Also returns the pulse order in which they are to be triggered

    elecDist = 100 # --> 100 so can be used as percetages of timeMultiplier 

    # ---------------------- New array of 16 electrodes arranged in pairs of 2 (as 2 rows of 8 electrodes). The orders below do not follow the physical format of the electrode pad
    if P_SIZE == 8: 
        # All in line like electrodes really are
        electrodeCoords = {
            1: (-4*elecDist,0),
            2: (-3*elecDist,0),
            3: (-2*elecDist,0),
            4: (-1*elecDist,0),
            5: (1*elecDist,0),
            6: (2*elecDist,0),
            7: (3*elecDist,0),
            8: (4*elecDist,0)
        }
    elif P_SIZE == 7:
        electrodeCoords = {
            1: (-3*elecDist,0),
            2: (-2*elecDist,0),
            3: (-1*elecDist,0),
            4: (1*elecDist,0),
            5: (2*elecDist,0),
            6: (3*elecDist,0),
            7: (0,5*elecDist)
        }
    elif P_SIZE == 6:
        # Triangle where
        electrodeCoords = {
            1: (-3*elecDist,0),
            2: (-2*elecDist,0),
            3: (-1*elecDist,0),
            4: (1*elecDist,0),
            5: (2*elecDist,0),
            6: (3*elecDist,0)
        }
    # -----------------------------

    elif P_SIZE == 9:
        electrodeCoords = {
            1: (-elecDist,elecDist),
            2: (0,elecDist),
            3: (elecDist,elecDist),
            4: (-elecDist,0),
            5: (0,0),
            6: (elecDist,0),
            7: (-elecDist,-elecDist),
            8: (0,-elecDist),
            9: (elecDist,-elecDist)
        }
    if P_SIZE == 5:
        electrodeCoords = {
            1: (-elecDist,elecDist),
            2: (-elecDist,-elecDist),
            3: (elecDist,elecDist),
            4: (elecDist,-elecDist),
            5: (0,0)
        }
    elif P_SIZE == 4:
        """
        electrodeCoords = {
            1: (0,elecDist),
            2: (-elecDist,0),
            3: (elecDist,0),
            4: (0,-elecDist)
        }
        """
        """
        electrodeCoords = {
            1: (-1.5*elecDist,1.5*elecDist),
            2: (-1.5*elecDist,-1.5*elecDist),
            3: (1.5*elecDist,1.5*elecDist),
            4: (1.5*elecDist,-1.5*elecDist)
        }
        """
        electrodeCoords = {
            1: (-elecDist,elecDist),
            2: (-elecDist,-elecDist),
            3: (elecDist,elecDist),
            4: (elecDist,-elecDist)
        }
    elif P_SIZE == 3:
        """
        electrodeCoords = {
            1: (0,1.5*elecDist),
            2: (-1.5*elecDist,-elecDist),
            3: (1.5*elecDist,-elecDist)
        }
        electrodeCoords = {
            1: (0,1.5*elecDist),
            2: (-1.5*elecDist,-elecDist),
            3: (1.5*elecDist,-elecDist)
        }
        electrodeCoords = {
            1: (0,2*elecDist),
            2: (-elecDist,0),
            3: (elecDist,0)
        }
        electrodeCoords = {
            1: (0,1.5*elecDist),
            2: (-1.5*elecDist,-elecDist),
            3: (1.5*elecDist,-elecDist)
        }

        """
        # OG:
        electrodeCoords = {
            1: (-elecDist,elecDist),
            2: (0,0),
            3: (elecDist,-elecDist)
        }
        """
        # TESTI:
        electrodeCoords = {
            1: (-elecDist,0),
            2: (0,0),
            3: (elecDist,0)
        }
        """
    elif P_SIZE == 2:
        electrodeCoords = {
            1: (-elecDist,0),
            2: (elecDist,0)
        }
    elif P_SIZE == 1:
        electrodeCoords = {
            1: (0,0)
        }

    # distance from the ping to each of the electrodes, which determines their trigger timing and intensity drop-off
    absDistancesToElectrodes = {}
    for i in range(1,P_SIZE+1):
        absDistancesToElectrodes[i] = EuclideanDistance(electrodeCoords[i], coordinates)

    d0 = min(absDistancesToElectrodes.values()) # distance from the ping to the nearest electrode (shortest distance to any electrode)
    
    # Subtract shortest distance from all to set the distance to the nearest electrode to 0
    relDistancesToElectrodes = {k:v-d0 for (k,v) in absDistancesToElectrodes.items()}

    return absDistancesToElectrodes, relDistancesToElectrodes


def calcPulseTimings(relDistances):
    # Calculate the order and timing of each of the pulses. 
    # Returns absolute (delays are w.r.t. the pulse sequence abs. start time t0) and relative (delays are w.r.t. the previous pulse trigger time) timings / delays of pulses
 
    if P_FREQUENCYLOCKED:
        frequency = P_FREQUENCY # [Hz]   
        delayBeforeSequenceStart = P_DELAYBEFORESEQSTART # [ms] minimum time between the end of the previous nplet pulse sequence and the localization pulse of the next nplet pulse sequence
        if P_USELOCPULSE: 
            delayAfterLocalizationPulse = P_DELAYAFTERLOCPULSE # [ms] time between the localization pulse and starting of the actual information nplet pulse sequence
            maxElectrodeTimeDiag = ((1000/frequency)-(delayBeforeSequenceStart+delayAfterLocalizationPulse))/2
        else:
            maxElectrodeTimeDiag = ((1000/frequency)-(delayBeforeSequenceStart))/2

        timeBetweenDiagElecs = maxElectrodeTimeDiag # [ms] max time between two electrodes - e.g. if ping is in top right corner, the time between first (L3) and last (L7) electrode pulses is 2 times this value
        timeBetweenTwoElecs = timeBetweenDiagElecs*np.sin(np.pi/4) # [ms] time between two electrodes on the same row / column
    else:
        timeBetweenTwoElecs = P_TIMEBETWEENTWOELECS

    timeMultiplier = timeBetweenTwoElecs/100 # timeBetweenTwoElecs/100 to be used with elecDist == 100 as ~percentages

    # Calculate each pulse absolute delay (delay from t0)
    pulseDelayAbsolute = {}
    for i in range(1,P_SIZE+1):
        pulseDelayAbsolute[i] = relDistances[i]*timeMultiplier

    # list pulse locations (keys) in the order of the pulses, as indicated by order of growing distance (values)
    pulseOrder = sorted(relDistances.keys(), key=lambda x:relDistances[x])

    # Calculate each pulse relative delay (delay from previous pulse)
    pulseDelayRelative = {k:v for (k,v) in pulseDelayAbsolute.items()}
    i_prev = None
    for i in pulseOrder[::-1]:
        if i_prev is not None:
            pulseDelayRelative[i_prev] = pulseDelayRelative[i_prev]-pulseDelayRelative[i]
        i_prev = i

    #tempDelayInOrder = {elec:pulseDelayRelative[elec] for elec in pulseOrder}
    #printf(absDelay=pulseDelayAbsolute, relDelay=pulseDelayRelative, orderedDelay=tempDelayInOrder)
    #exit(1)

    return pulseDelayAbsolute, pulseDelayRelative, pulseOrder


def calcPulseIntensityCoeffs(absoluteDistances, GaussianLookupTable):
    # Calculates each pulse intensity coefficient based on Gaussian distribution 

    intensityCoeffs = {}
    for i in range(1,P_SIZE+1):
        coeff = lookupGaussianCoeff(GaussianLookupTable, GAUSS_STDDEV, absoluteDistances[i])
        coeff = coeff if coeff > GAUSS_COEFF_MIN else GAUSS_COEFF_MIN
        intensityCoeffs[i] = coeff

    return intensityCoeffs


def calcPulseIntensity(intensityCoefficients, method="pulseWidth"):
    # Calculates each pulse intensity with the selected method

    if method == "pulseWidth":
        pulseWidthMax = BM_COMMONPULSEWIDTH

        pulseWidths = {}
        for i in range(1,P_SIZE+1):
            pulseWidths[i] = math.floor(pulseWidthMax*intensityCoefficients[i])

        return pulseWidths


def addLocalizationPulse(data, reverse=False):
    # adds data concerning the initial localization pulse to the timing and intensity of the pulse sequence data
    # NOTE: localization pulse location is already used in a pulse, so the localization pulse is marked as 0
    # if reverse==True, sets the localization pulse as last and not as first
    
    localizationPulseWidth_us = P_LOCPULSEWIDTH
    delayAfterLocalizationPulse = P_DELAYAFTERLOCPULSE

    localizationPulseWidth_ms = localizationPulseWidth_us/1000

    # Add localization pulse
    data[0] = {}
    data[0]["electrodes"] = locationToElectrodes(0)
    data[0]["intensityCoeff"] = -1
    data[0]["pulseWidth"] = localizationPulseWidth_us
    if not reverse:
        data[0]["relTiming"] = 0
        data[0]["absTiming"] = 0
        data["order"].insert(0,0)

        # Add localization pulse related delays to pulses
        #for i in range(1,P_SIZE+1):
            #for timing in ['relTiming', 'absTiming']:
                #data[i][timing] += localizationPulseWidth_ms+delayAfterLocalizationPulse
        for i in range(1,P_SIZE+1):
            data[data["order"][1]]["relTiming"] = localizationPulseWidth_ms+delayAfterLocalizationPulse
            data[i]["absTiming"] += localizationPulseWidth_ms+delayAfterLocalizationPulse
    else:
        data[0]["relTiming"] = delayAfterLocalizationPulse
        data[0]["absTiming"] = data[data["order"][-1]]["absTiming"]+delayAfterLocalizationPulse
        data["order"].append(0)

    return data


def getPulseSequenceData(pingCoordinates, GaussianLookupTable, goalBehind):
    # Given ping coordinates (and gaussian lookup table), returns the full pulse sequence settings for the BiMatrix to use

    # Calculate distances from ping to each of the electrodes. RelDistance has smallest dist d0 subtracted from all distances
    absDistances, relDistances = calcDistances(pingCoordinates)

    # Calculate pulse intensity coefficients based on the dropoff curve of a gaussian normal distribution
    intensityCoeffs = calcPulseIntensityCoeffs(absDistances, GaussianLookupTable)
    #printf(intensityCoeffs=intensityCoeffs)

    # Calculate the intensity of the pulse with the defined method
    pulseWidths = calcPulseIntensity(intensityCoeffs, method="pulseWidth")

    # Calculate the order and timing of each of the pulses. AbsTimings has each pulse delay refer to pulse sequence abs. start time t0, whereas relTimings are relative to the previous pulse
    absTimings, relTimings, pulseOrder = calcPulseTimings(relDistances)

    data = {}
    data["order"] = pulseOrder
    data["minTimeBetweenSequences"] = P_DELAYBEFORESEQSTART
    for i in range(1,P_SIZE+1):
        data[i]= {}
        data[i]["absTiming"] = absTimings[i] # Can be used to trigger each pulse w.r.t. absolute time (when the pulse should be triggered based on the start time of sequence)
        data[i]["relTiming"] = relTimings[i] # Can be used to trigger each pulse w.r.t. relative time (when the pulse should be triggered based on the previous pulse trigger time)
        data[i]["pulseWidth"] = pulseWidths[i] # Intensity is mapped directly to the given pulse width
        data[i]["intensityCoeff"] = intensityCoeffs[i] # Currently not used, as the more-refined value "pulseWidths" is used
        data[i]["electrodes"] = locationToElectrodes(i)

    if P_USELOCPULSE:
            # Add the localization pulse as the first pulse in the sequence and modify sequence values (mainly delays) to account for it
            data = addLocalizationPulse(data, reverse=goalBehind)
    
    for i in range(1,P_SIZE+1):
        for timing in ['relTiming', 'absTiming']:
            data[i][timing] = math.floor(data[i][timing])

    return data
