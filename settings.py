import logging

""" 
settings.py

Contains general settings for all files.
"""

# BiMatrix base settings
BM_PORT = 'COM3'
BM_LOGGING = logging.WARNING
BM_MODE = "bipolar"
BM_VOLTAGE = 100
BM_CURRENTRANGE = "low"
BM_NPLETRATE = 1
BM_TIMEBETWEENPULSES = 1
BM_COMMONPULSEWIDTH = 500
BM_COMMONPULSEAMPLITUDE = 150 # 650  # 150
BM_ANODESCATHODES = [([3], [4])]
BM_NPLETAMOUNT = 1


# General pulse sequence settings
P_SIZE = 8 # Number of pulse locations available (8 for new 2x8 matrix pad) ------ (9 for 3x3, 3 for triangle, 4 for cross, 2 for "ears")
   
P_FREQUENCYLOCKED = False 
P_FREQUENCY = 1 # [Hz] Only used if P_FREQUENCYLOCKED == True 

P_TIMEBETWEENTWOELECS = 100 #100 # [ms] Only used if P_FREQUENCYLOCKED ==  False, otherwise is calculated based on P_FREQUENCY

P_DELAYBEFORESEQSTART = 500 # [ms] 

P_USELOCPULSE = False #False
#P_LOCPULSEREVERSE = True # if True, the location pulse is done after sequence. If false, the loc pulse is before sequence.
P_LOCPULSEWIDTH = 800 # [µs] Location pulse width. Used only if P_USELOCPULSE == True
P_DELAYAFTERLOCPULSE = 300 # [ms] Delay between localization pulse and first "proper" pulse. Used only if P_USELOCPULSE == True


# Gaussian settings
GAUSS_STDDEV = 3500 #350 # Gaussian standard deviation (used to calculate intensity dropoff)
GAUSS_COEFF_MIN = 0.4 #0.3 # Gaussian minimum coefficient (min. coefficient for intensity, as calculated from Gaussian)