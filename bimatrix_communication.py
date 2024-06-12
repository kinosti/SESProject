import controller
#import logging
import time

from helpers import *
from settings import *

from time import sleep

""" 
bimatrix_communication.py (ex. testing5.py)

Handles all communication with the BiMatrix device.
"""


class user:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.minCharge = None
        self.maxCharge = None
        self.minCurrent = None
        self.maxCurrent = None

    def __str__(self):
        return f"{self.name}({self.id}): threshold current [mA]: {self.minCurrent}, max current [mA]: {self.maxCurrent}" 


class deviceSettings:
    def __init__(self):        
        self.current_range = None  # high or low
        self.voltage = None  # range 70V - 150V
        self.num_nplets = None  # 0 (infinity) - 16777215
        self.time_between = None  # 1ms - 255ms
        self.delay = None  # 0ms - 16777215ms
        self.repetition_rate = None  # 1 - 400pps (pulses per second)
        self.pulse_widths = None  # 50 - 1000 microseconds
        self.pulse_amplitudes = None  # w = 100 - 1000, unit w/10 mA (High), w/100 mA (Low)
        self.mode = None  # unipolar or bipolar
        self.common_electrode = None  # cathode or anode
        self.output_channels = None
        self.channel_pairs = None #[([3],[10])]
        self.is_short_protocol = None
        self.common_electrode_short = None # cathode or anode
        self.output_channel_activity = None # ([1,3,5], 50)

def setPulseGenerator(state):
    #

    return device.set_pulse_generator(state)


def initControllerValues():
    # Initializes BiMatrix with proper base values

    # Setting 'device' as global var to not have to pass it as arg each time
    global device

    # only send the n-plet once upon trigger
    res = device.set_num_nplets(BM_NPLETAMOUNT)
    if not res: raise Exception("set_num_nplets error")
    
    #res = device.set_num_nplets(1)
    #if not res: raise Exception("set_num_nplets error")

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # -----------------------------------
    # mode = "bipolar"
    # voltage = 100
    # currentRange = "high"

    # nPletRate = 1
    # timeBetweenPulses = 1

    # commonPulseWidth = 500 # set to None if using unique pulse widths
    # pulseWidths = [] # keep empty if using commonPulseWidth, otherwise fill each pulse (24) width separated by commas
    
    # commonPulseAmplitude = 200  # set to None if using pulseWidths
    # pulseAmplitudes = [] # keep empty if using commonPulseAmplitude, otherwise fill each pulse (24) amplitude separated by commas

    # anodesCathodes = [([3], [10])]
    
    mode = BM_MODE
    voltage = BM_VOLTAGE
    currentRange = BM_CURRENTRANGE
    nPletRate = BM_NPLETRATE
    timeBetweenPulses = BM_TIMEBETWEENPULSES
    commonPulseWidth = BM_COMMONPULSEWIDTH 
    commonPulseAmplitude = BM_COMMONPULSEAMPLITUDE  
    anodesCathodes = BM_ANODESCATHODES

    pulseWidths = [] 
    pulseAmplitudes = [] 
    
    # - - - - - - - - - - - - - - - - - -

    amplitudeScaler=10 if currentRange == "high" else 100
    pulseAmplitudesScaled = [x/amplitudeScaler for x in pulseAmplitudes]

    print("Mode: ", mode)
    print("Voltage: ", voltage, "V")
    print("Current range: ", currentRange)
    print("N-plet repetition rate: ", nPletRate, "Hz")
    print("Time between pulses: ", timeBetweenPulses, "ms")

    if commonPulseWidth:
        print("Common pulse width: ", commonPulseWidth, "μs")
        for i in range(24):
            pulseWidths.append(commonPulseWidth)
    else:
        print("Pulse widths [μs]: ", pulseWidths)
    
    if commonPulseAmplitude:
        print("Common pulse amplitude: ", commonPulseAmplitude/amplitudeScaler, "mA")
        if commonPulseAmplitude == 0:
            pulseAmplitudes = [0]*24
        else:
            for i in range(24):
                pulseAmplitudes.append(commonPulseAmplitude)

    else:
        print("Pulse amplitudes [mA]: ", pulseAmplitudesScaled)

    print("Anode-cathode pairs each pulse: " , anodesCathodes)

    # -----------------------------------
    
    #print("Set voltage")
    if device.set_voltage(voltage) is False: return False

    #print("Set mode")
    if device.set_mode(mode) is False: return False
    
    #print("Toggle pulse generation")
    device.set_pulse_generator(False)
    if device.set_pulse_generator(True) is False: return False

    #print("Set current range")
    if device.set_current_range(currentRange) is False: return False
    
    #print("Set n-plet repetition rate")
    if device.set_repetition_rate(nPletRate) is False: return False
    
    #print("Set time between pulses")
    if device.set_time_between(timeBetweenPulses) is False: return False

    #print("Set pulse widths")
    if device.set_pulse_width(pulseWidths) is False: return False
    
    #print("Set pulse charges / amplitudes")
    if device.set_amplitude(pulseAmplitudes) is False: return False

    #print("Set bipolar pulse anodes & cathodes")
    if device.set_pulses_bipolar(anodesCathodes) is False: return False

    print()

    if commonPulseAmplitude and commonPulseWidth:
        print(mode, ",", voltage, "V,", commonPulseAmplitude/amplitudeScaler, "mA,", len(anodesCathodes), "pulse(s) with each a duration of", commonPulseWidth, "μs and", timeBetweenPulses, "ms between pulses, repeating at", nPletRate, "Hz.")
    elif commonPulseWidth and not commonPulseAmplitude:
        print(mode, ", ", voltage, "V, from ", min(pulseAmplitudes,default=0)/amplitudeScaler, "mA to ", max(pulseAmplitudes,default=0)/amplitudeScaler, "mA. ", len(anodesCathodes), " pulse(s) with each a duration of ", commonPulseWidth, "μs and ", timeBetweenPulses, "ms between pulses, repeating at ", nPletRate, "Hz.")  
    elif commonPulseAmplitude and not commonPulseWidth:
        print(mode, ", ", voltage, "V, ", commonPulseAmplitude/amplitudeScaler, "mA, ", len(anodesCathodes), " pulse(s) durations from ", min(pulseWidths), "μs to ", max(pulseWidths), "μs and ", timeBetweenPulses, "ms between pulses, repeating at ", nPletRate, "Hz.")
    else:
        print(mode, ", ", voltage, "V, from ", min(pulseAmplitudes,default=0)/amplitudeScaler, "mA to ", max(pulseAmplitudes,default=0)/amplitudeScaler, "mA. ", len(anodesCathodes), " pulse(s) durations from ", min(pulseWidths), "μs to ", max(pulseWidths), "μs and ", timeBetweenPulses, "ms between pulses, repeating at ", nPletRate, "Hz.")  
    
    print(len(anodesCathodes), " pulses [a-->c]:")
    for anode, cathode in anodesCathodes:
        print(anode, "-->", cathode)


def changeSettings(settings, debugging=False):

    if settings.num_nplets:
        if debugging: print("Set number of n-plets")
        if device.set_num_nplets(settings.num_nplets) is False: return False

    if settings.voltage:
        if debugging: print("Set voltage")
        if device.set_voltage(settings.voltage) is False: return False

    if settings.mode:
        if debugging: print("Set mode")
        if device.set_mode(settings.mode) is False: return False

    if settings.current_range:
        if debugging: print("Set current range")
        if device.set_current_range(settings.current_range) is False: return False
    
    if settings.repetition_rate:
        if debugging: print("Set n-plet repetition rate")
        if device.set_repetition_rate(settings.repetition_rate) is False: return False
    
    if settings.time_between:
        if debugging: print("Set time between pulses")
        if device.set_time_between(settings.time_between) is False: return False

    if settings.pulse_widths:
        if debugging: print("Set pulse widths")
        if device.set_pulse_width(settings.pulse_widths) is False: return False
    
    if settings.pulse_amplitudes:
        if debugging: print("Set pulse charges / amplitudes")
        print(settings.pulse_amplitudes)
        print(type(settings.pulse_amplitudes))
        #if device.set_amplitude(settings.pulse_amplitudes) is False: return False
        res = device.set_amplitude(settings.pulse_amplitudes)
        if not res: return False
    if settings.delay:
        if debugging: print("Set delay")
        if device.set_delay(settings.delay) is False: return False

    #if settings.mode:
        #if settings.mode == 'bipolar':
    if settings.channel_pairs:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(settings.channel_pairs)
        print(device.channel_pairs)
        if debugging: print("Set bipolar pulse anodes & cathodes")
        if device.set_pulses_bipolar(settings.channel_pairs) is False: return False
        print(device.channel_pairs)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            #res = device.set_pulses_bipolar(settings.channel_pairs)
            #if not res: 
                #print(res)
                #return False
        #else: # mode == unipolar
        #if settings.short_protocol:
    #if settings.common_electrode_short:
        #if debugging: print("SHORT: Set common anode/cathode (unipolar)")
        #if device.set_common_electrode_short(settings.common_electrode_short) is False: return False
    
    #if settings.output_channel_activity:
        #if debugging: print("SHORT: Set output channel activity  (unipolar)")
        #if device.set_output_channel_activity(settings.output_channel_activity) is False: return False
            #pass
        #else:
    if settings.common_electrode:
        if debugging: print("Set common anode/cathode (unipolar)")
        if device.set_common_electrode(settings.common_electrode) is False: return False
    
    if settings.output_channels:
        if debugging: print("Set unipolar pulse outputs")
        if device.set_pulses_unipolar(settings.output_channels) is False: return False

    return True


def executePulseSequence(data, prevTriggerTime):
    # TODO selkeyden kannalta olisi parempi jos "changeSettings" funccia asetusten muutosteen, (toista funkkia käyttää triggaamiseen), 
    # ja tätä vain data-dictin unpackaukseen ja delay odotus looppaukseen ym. Mutta tuoko lisää paljon delayta?


    # NOTE: When triggering an nplet, BiMatrix has takes settings from two places: "prebuffer" and "buffer". Upon triggering an nplet, the 
        # settings move from prebuffer to buffer, if any new settings were previously written to prebuffer. All settings for each individual pulse
        # (electrodes, pulse widths, .. ) are taken from buffer, but some (all?) values associated to the nplet in general are taken directly from buffer
        # (number of pulses in the nplet, time between pulses, ..). This means that the settings for each pulse must be written not for the set of pulses intended to 
        # be triggered next, but the one(s) after. However, the amount of pulses in the nplet and the time between pulses is taken from the settings written right before 
        # triggering, which means that those must be saved from previous loop and written using as those "previous cycle values". The biggest issue comes when the
        # amount of pulses change. If the number of pulses increase, then all the values for all of the pulses are written to BiMatrix as normal, but immediately afterwards
        # (before triggering), the settings must be written to BiMatrix again but without all the values for the "excess" pulses. 

        # EXAMPLE: Nplet A has only one pulse A1, nplet B has three pulses B1,B2,B3. We have written the values of nplet A to the BiMatrix before previous trigger,
        # meaning that all values for nplet A have already moved from prebuffer to buffer. Now before triggering the nplet A, we need to write the values of the next
        # nplet (nplet B) to the BiMatrix so that those values similarly move from prebuffer to buffer upon triggering nplet A. We first write all settings of the 
        # three pulses of nplet B to BiMatrix as normal (B1,B2,B3), but then we need to immediately write the settings of nplet B again to the BiMatrix BUT ONLY WITH
        # THE DATA OF THE FIRST PULSE (B1), so that the number of pulses in settings in prebuffer right before triggering the pulse is equal to the number of pulses in
        # the buffer (nplet A). Now we can trigger the pulse A, and we are ready for the next cycle as well because the first value writing of B1,B2,B3 wrote all the settings to 
        # prebuffer, but then the second writing of only B1 writes the value for B1 again (but does not overwrite settings for B2 and B3, and as such they still remain
        # in the prebuffer). As the last values written to BiMatrix only contained 1 pulse, the triggered nplet only has 1 pulse,and its values are fetched from buffer, 
        # and therefore the triggered nplet now only triggers one pulse with the settings from buffer, which contains the values for the nplet A (pulse A1) as inteded.

        # In similar case but where the number of pulses decrease (so nplet A has three pulses and nplet B only one), we can do otherwise the same process, but instead of 
        # writing the values a second time with less pulses, we actually just write more pulses. The values of these pulses will never be used, so as long as the number of 
        # pulses match, it doesn't matter what values are written (as long as they are possible and do not cause an error in BiMatrix). This method doesn't actually require
        # a second writing of the settings, as the same effect would be achieved with just writing the extra pulse settings in the initial writing of the settings, but for
        # coherence of the code this is still done with the second settings-writing as then always the first settings are correct for the next round's nplet, and the second 
        # writing of settings is only used to correct the bugs of BiMatrix.

    # Setting 'device' as global var to not have to pass it as arg each time
    global device

    print()
    print("------ executePulseSequence ------")

    # ------------

    order = data["order"]
    print(order)

    minTimeBetweenSequences = data['minTimeBetweenSequences']

    pulseReady=False
    prev = prevTriggerTime  # Time ref point

    currPulseDelay = 0
    nextPulseDelay = 0

    pulseIndex = 0

    timeBetweenPulses = 1
    prevTimeBetweenPulses = 1
    
    anodesCathodes = []
    pulseWidths = []
    prevAnodesCathodes = []
    prevPulseWidths = []

    # ------------
    prevPulsesInNplet = 1
    pulsesInNplet = 1
    #fullDelay = 0


    delayAfterTrigger = 0.1 # 0.05
    now = 0


    nPulses = P_SIZE+1 if P_USELOCPULSE else P_SIZE

    pulseSequenceStartTime = time.perf_counter()
    while pulseIndex <= nPulses:
        if pulseReady == False and time.perf_counter()-now > delayAfterTrigger:
            #printf(pulseReady=pulseReady)
            prevPulsesInNplet = pulsesInNplet
            prevAnodesCathodes = anodesCathodes
            prevPulseWidths = pulseWidths

            anodesCathodes = []
            pulseWidths = []

            if pulseIndex == nPulses:
                # Writing dummy pulse values, but the triggered pulse is the last of the sequence
                currPulseDelay = nextPulseDelay 

                anodesCathodes = [([1], [2])]

                pulseWidths = [400]
            else:
                pulseLocation = order[pulseIndex]

                currPulseDelay = nextPulseDelay # first round == 0
                if pulseIndex == 0:
                    nextPulseDelay = minTimeBetweenSequences
                else:
                    nextPulseDelay = minTimeBetweenSequences+data[pulseLocation]["absTiming"]

                #printf(nextPulseDelay=nextPulseDelay, minTimeBetweenSequences=minTimeBetweenSequences,abstiming=data[pulseLocation]["absTiming"])

                pulsesInNplet = 1
                prevTimeBetweenPulses = timeBetweenPulses
                combinedTimeBetweenPulses = 0
                for i in range(pulseIndex+1,nPulses):
                    """
                    if data[order[i]]["relTiming"] <= 17:
                        # All pulses with delay <= 15ms are set as a single nplet with minimum delay in betwen pulses (1ms)
                        # TODO aseta joku flagi että löytyi jo tälläinen rykelmä ja breakkaa jos löytyy muita <= 50ms pulsesja jotka ei sovi tähän JA BREAK JOS FLÄGI JO ASETETTU
                        pulsesInNplet+=1
                        timeBetweenPulses = 1
                    elif data[order[i]]["relTiming"] <= 34:
                        # TODO aseta joku flagi että löytyi jo tälläinen rykelmä ja breakkaa jos löytyy muita <= 50ms pulsesja jotka ei oo tähän JA BREAK JOS FLÄGI JO ASETETTU
                        pulsesInNplet+=1
                        timeBetweenPulses = 25
                    elif data[order[i]]["relTiming"] <= 51:
                        # TODO aseta joku flagi että löytyi jo tälläinen rykelmä ja breakkaa jos löytyy muita <= 50ms pulsesja jotka ei oo tähän JA BREAK JOS FLÄGI JO ASETETTU
                        pulsesInNplet+=1
                        timeBetweenPulses = 42
                    else:
                        timeBetweenPulses = 1
                        break
                    """

                    """
                    # Group similar low-delay pulses to same nplet with delay handled within BiMatrix 
                    if data[order[i]]["relTiming"] <= 20:
                        groupTimeBetweenPulses = 1

                        # break if 
                        if pulsesInNplet > 1 and timeBetweenPulses != groupTimeBetweenPulses: break

                        pulsesInNplet+=1
                        timeBetweenPulses = groupTimeBetweenPulses
                    elif data[order[i]]["relTiming"] <= 50:
                        groupTimeBetweenPulses = 35
                        if pulsesInNplet > 1 and timeBetweenPulses != groupTimeBetweenPulses: break

                        pulsesInNplet+=1
                        timeBetweenPulses = groupTimeBetweenPulses
                    else:
                        break
                    """
                    
                    # All following pulses with delay less than 40 (min. delay that BiMatrix is capable of is 47 in current system) are grouped to single nplet where all pulses are without delays
                    loopDelay = data[order[i]]["relTiming"]
                    printf(loopDelay=loopDelay)
                    if loopDelay <= 60: #60
                        print("pulsesInNplet+=1")
                        pulsesInNplet+=1
                        combinedTimeBetweenPulses += loopDelay
                    else:
                        break

                if pulsesInNplet > 1:
                    # Use the mean delay within the pulse delays in the nplet. If pulsesInNplet==2, result is the second pulse delay directly
                    timeBetweenPulses = int(combinedTimeBetweenPulses/(pulsesInNplet-1))
                    if timeBetweenPulses < 1: timeBetweenPulses=1

                for i in range(pulsesInNplet):
                    anodesCathodes.append(data[order[pulseIndex+i]]["electrodes"])
                    pulseWidths.append(data[order[pulseIndex+i]]["pulseWidth"])


            #printf("setting values initially")
            #time.sleep(0.0075)
            orgTime = time.perf_counter()
            while time.perf_counter()-orgTime<0.015:                
                time.sleep(0.0001)

            res = device.set_pulses_bipolar(anodesCathodes)
            if not res:
                printf("FAILED: ANODESCATHODES 1")
                res = device.set_pulses_bipolar(anodesCathodes)
                if not res: raise Exception("Error setting anodesCathodes")

            #time.sleep(0.0075)
            #time.sleep(0.01)
            orgTime = time.perf_counter()
            while time.perf_counter()-orgTime<0.01:                
                time.sleep(0.0001)


            res = device.set_pulse_width(pulseWidths)
            if not res: 
                printf("FAILED: PULSE WIDTHS 1")
                res = device.set_pulse_width(pulseWidths)
                if not res: raise Exception("Error setting pulseWidths")

            #print("ORIGINAL WRITTEN SETTINGS: ")
            #printf(anodesCathodes=anodesCathodes, pulseWidths=pulseWidths)

            if pulsesInNplet != prevPulsesInNplet:
                # The number of pulses and timebetweenpulses are taken from prebuffer (settings given above), but as other values are taken from buffer
                # (values written before previous trigger), we need to rewrite settings with correct number of pulses in the nplet if the numbers differ
                
                printf(pulsesInNplet=pulsesInNplet, prevPulsesInNplet=prevPulsesInNplet)

                if pulsesInNplet > prevPulsesInNplet:
                    # In the current settings there are more pulses in the nplet than in the one we are about to trigger - remove excess pulses from the end to match pulse amount
                    while len(anodesCathodes) > prevPulsesInNplet:
                        anodesCathodes.pop()
                        pulseWidths.pop()
                else:
                    # In the current settings there are fewer pulses in the nplet than in the one we are about to trigger - add dummy pulses to match pulse amount
                    while len(anodesCathodes) < prevPulsesInNplet:
                        anodesCathodes.append(([1], [2]))
                        pulseWidths.append(400)

                res = device.set_pulses_bipolar(anodesCathodes)
                if not res:
                    printf("FAILED: ANODESCATHODES 2")
                    res = device.set_pulses_bipolar(anodesCathodes)
                    if not res: raise Exception("Error setting anodesCathodes")

                res = device.set_pulse_width(pulseWidths)
                if not res: 
                    printf("FAILED: PULSE WIDTHS 2")
                    res = device.set_pulse_width(pulseWidths)
                    if not res: raise Exception("Error setting pulseWidths")
            

            if prevPulsesInNplet > 1:
                res = device.set_time_between(prevTimeBetweenPulses)
                if not res:
                    printf("FAILED: TIME BETWEEN PULSES")
                    res = device.set_time_between(prevTimeBetweenPulses)
                    if not res: raise Exception("Error setting time between pulses")
            
            
            #print("FINAL WRITTEN SETTINGS: ")
            #printf(anodesCathodes=anodesCathodes, pulseWidths=pulseWidths, timeBetweenPulses=prevTimeBetweenPulses)

            pulseReady = True

        while pulseReady:
            now = time.perf_counter()
            #elapsed_time = now - prev
            elapsed_time = now - pulseSequenceStartTime
            elapsed_time_ms = elapsed_time*1000
            
            if elapsed_time_ms >= currPulseDelay:
                #timeExceeded = round(elapsed_time_ms-currPulseDelay,0)
                #print("Target delay was " + str(currPulseDelay) + "ms, waited " + str(round(elapsed_time_ms,0)) + "ms (" + str(timeExceeded) + "ms too long)")
                
                # if timeExceeded >= 5:
                #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                #     timeExceededCounter+=1
                #     if timeExceededCounter >= 3:
                #         raise Exception(fullPulseSequencesDone)

                pulseIndex += pulsesInNplet

                prev = now

                res = device.trigger_pulse_generator()
                if not res: raise Exception("Trigger error")
                print("ACTUAL triggered pulse anodes-cathodes:")
                printf(anodesCathodes=prevAnodesCathodes, pulseWidths=prevPulseWidths, timeBetweenPulses=prevTimeBetweenPulses)

                #print(str(pulsesInNplet) + "pulses in triggered nplet, took "+ str(round((time.perf_counter()-now)*1000,0)) + "ms")

                if pulseIndex >= nPulses: 
                    #print("Pulse sequence completed, took " + str(round((time.perf_counter()-pulseSequenceStartTime)*1000,0)) + "ms (for ref: " + str(fullDelay) + "ms of delay set, does not include pulse widths)") 
                    #pulseSequenceStartTime = time.perf_counter()
                    prevTriggerTime = prev

                pulseReady = False
                #time.sleep(0.0001) # required for bimatrix to not lag out occasionally
                time.sleep(0.00001) # required for bimatrix to not lag out occasionally

    return prevTriggerTime

def close():
    # closes connection

    device.close_serial()


def connectToBiMatrix():
    # Connects to BiMatrix
    
    # Setting 'device' as global var to not have to pass it as arg each time
    global device

    print("Starting...")
    device = controller.Controller(BM_PORT, logging_level=BM_LOGGING)
    print("Started")

    device.set_pulse_generator(True)  
    battery_level = device.read_battery()
    print("Battery level is: {}%".format(battery_level)) 
    device.set_pulse_generator(False)


def initializeController():
    # Handles full initialization of the controller (creates connection + sets initial parameters)

    connectToBiMatrix()
    initControllerValues()