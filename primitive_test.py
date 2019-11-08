import AT_db

import serial
import time
import bluetooth
import bluetool

import subprocess

TIME_DELAY = 1
CONNECTION_READ_LEN = 64

connection = None
services = None
vehicle_info = dict()
target = "00:04:3E:9A:0D:96"
blue = bluetool.bluetool.Bluetooth()


def bind_serial_port():
    subprocess.check_output(['rfcomm', 'bind', 'rfcomm0', target])


def release_serial_port():
    subprocess.check_output(['rfcomm', 'release', 'rfcomm0'])


def connect_to_serial_port():
    global connection

    print('Connect to serial port')

    if connection is None:
        bind_serial_port()
        connection = serial.Serial(port='/dev/rfcomm0', bytesize=8, parity='N', stopbits=1, timeout=0, rtscts=False, dsrdtr=False)

    time.sleep(TIME_DELAY + 5)
    determine_vehicle_info("ATI")
    return connection


def determine_vehicle_info(cmd, delay = TIME_DELAY):
    global connection
    try:
        cmdr = cmd + "\r"
        connection.write(cmdr.encode())
        time.sleep(delay)
        inforesponse = connection.read(CONNECTION_READ_LEN)
        connection.flushInput()
        connection.flushOutput()
    except Exception as e:
        inforesponse = "NULL_" + cmd
    print(AT_db.AT_desc[cmd] + " (" + cmd + ") : " + inforesponse)
    vehicle_info[cmd] = inforesponse
    return inforesponse


def determine_CAN_status():
    return determine_vehicle_info("ATCS")


def determine_current_protocol():
    return determine_vehicle_info("ATDP")


def determine_keywords():
    return determine_vehicle_info("ATKW")


def determine_program_parameters_summary():
    return determine_vehicle_info("ATPPS")


def determine_IgnMon_input_level():
    return determine_vehicle_info("ATIGN")


def determine_stored_data():
    return determine_vehicle_info("ATRD")


def determine_voltage():
    return determine_vehicle_info("ATRV")


def determine_vin():
    return determine_vehicle_info("0902")


def determine_pairing_status():
    print('Pair with the target device')
    # get the list of paired devices
    paircheck = blue.get_paired_devices()
    status = any(search['mac_address'] == target for search in paircheck)
    # if the target is not paired then try to pair
    if not status:
        blue.scan() # lesson learnt: must do a scan before pairing
        status = blue.pair(target)
    return status


def determine_devices_using_hcitool():
    print("Performing inquiry for nearby devices...")
    nearby_devices = bluetooth.bluez.discover_devices(duration=8, lookup_names=True, flush_cache=True)
    print("  found %d devices" % len(nearby_devices))
    for addr, name in nearby_devices:
        print("    %s - %s" % (addr, name))
    return nearby_devices


def determine_ELM327_use_AT_commands():
    determine_vehicle_info("ATI")
    determine_vehicle_info("AT@1")
    determine_vehicle_info("AT@2")

def detemrine_services():
    global services
    services = bluetooth.find_service(address=target)
    return services

MS_INTERVAL = 0.5
def standardobd():
    print('-' * 45)
    print('+++++ Standard MODEs & PIDs')
    print('-' * 45)
    print(
    'The following tests for the standard 10 modes of operation as described in the latest OBD-II standard SAE J1979.  OEMs are not required to support all modes')
    print('')
    print('If you need to pause for whatever reason, use CTRL+C')
    st = int('00', 16)
    ed = int('0A', 16)
    ed2 = int('FF', 16)

    #smsginterval0 = raw_input("What message interval would you like to set (in seconds, floating point allowed)? ")
    print("Message interval: " + str(MS_INTERVAL))
    #smsginterval = float(smsginterval0)

    #sobdlogfile = "sobdlog_" + target + ".log"

    #sobdlog = open(sobdlogfile, 'wb')

    for x in xrange(st, ed + 1):
        smode = str(format(x, 'X')).zfill(2)

        for y in xrange(st, ed2 + 1):
            spid = str(format(y, 'X')).zfill(2)

            # print smode+" "+spid #FOR TESTING

            sentry = smode + spid + "\r"

            # sobdlog.write("-----------------------------------\n")
            # sobdlog.write("Mode & PID: " + smode + " " + spid + "\n")
            # sobdlog.write("-----------------------------------\n")

            try:
                # connection.flushInput() #discard input buffer contents
                # connection.flushOutput() #discard output buffer contents

                connection.write(sentry.encode())

                time.sleep(MS_INTERVAL)  # give the port time to respond

                response = connection.read(CONNECTION_READ_LEN)

                # sobdlog.write(str(response))

                print "Sent Mode & PID: " + str(sentry) + " || " + str(response) + "\n"

            except KeyboardInterrupt:
                print ""
                standardagain = raw_input(
                    "KeyboardInterrupt: hit 'x' to stop or press the ENTER key to continue the test: ")
                if standardagain == 'x':
                    return #sobdlogfile
                else:
                    None

            except Exception, e:
                print "Error: " + str(e)
                return

    #sobdlog.close()

    return #sobdlogfile


def nonstandardobd():
    print('-' * 45)
    print('+++++ Non-standard MODEs & PIDs')
    print('-' * 45)
    print(
    'The following tests for OEM specific modes and PIDs.  Some PIDs may have an additional sub-PID, but as these are manufacturer specific, it may not be obvious which ones do')
    print('')
    print('If you need to pause for whatever reason, use CTRL+C')
    print ''
    print('WARNING: May result in vehicle malfunction')
    print('')

    start = int('0B', 16)
    start2 = int('00', 16)
    end = int('FF', 16)

    # nmsginterval0 = raw_input("What message interval would you like to set (in seconds, floating point allowed)? ")
    # nmsginterval = float(nmsginterval0)

    # nobdlogfile = "nobdlog_" + target + ".log"
    #
    # nobdlog = open(nobdlogfile, 'wb')

    for i in xrange(start, end + 1):

        nmode = str(format(i, 'X')).zfill(2)

        for j in xrange(start2, end + 1):

            npid = str(format(j, 'X')).zfill(2)

            nentry = nmode + npid + "\r"

            # nobdlog.write("-----------------------------------\n")
            # nobdlog.write("Mode & PID: " + nmode + " " + npid + "\n")
            # nobdlog.write("-----------------------------------\n")

            try:
                #				connection.flushInput() #discard input buffer contents
                #				connection.flushOutput() #discard output buffer contents


                connection.write(nentry.encode())

                time.sleep(MS_INTERVAL)  # give the port time to respond

                response2 = connection.read(64)

                # nobdlog.write(str(response2))

                print "Sent Mode & PID: " + str(nentry) + " || " + str(response2) + "\n"

            except KeyboardInterrupt:
                print ""
                nonstandardagain = raw_input(
                    "KeyboardInterrupt: hit 'x' to stop or press the ENTER key to continue the test: ")
                if nonstandardagain == 'x':
                    return #nobdlogfile
                else:
                    None
            except Exception, e:
                print "Error: " + str(e)
                return

    return #nobdlogfile

def monitoring():
    try:
        print('-' * 45)
        print('+++++ Passive monitoring')
        print('-' * 45)
        print ""
        print('If you need to pause for whatever reason, use CTRL+C')
        print ''
        print ""
        print "CAN bus stream coming through..."
        print ""
        headson = "ATH1\r"
        connection.write(headson.encode())
        time.sleep(1)

        monitorcmd = "ATMA\r"

        # monlog = "monlog_" + target + ".log"
        #
        # monlogger = open(monlog, 'ab')

        while True:
            try:
                connection.write(monitorcmd.encode())
                time.sleep(0.1)
                monitor = connection.read(64)
                print monitor
                # monlogger.write(monitor)
            except KeyboardInterrupt:
                print ""
                monagain = raw_input(
                    "KeyboardInterrupt: hit 'x' to stop, or press the ENTER key to continue the test: ")
                if monagain == 'x':
                    return # monlog
    except:
        pass

FLOOD_MODE = int('11',16)
FLOOD_PID  = int('22',16)
FLOOD_NUMBER = 100
FLOOD_INTERVAL = 0.2

def udsflood():
    print('-' * 45)
    print('+++++ UDS messages')
    print('-' * 45)
    print(
    'The following tests for mainly physical responses to Unified Diagnostic Service (UDS) message floods.  It is recommended that you run through the whole suite of non-standard modes and PIDs first and note any responses.  However, this is here in case such messages have already been predetermined')
    print('')
    print('If you need to stop for whatever reason, use CTRL+C.  Example of input: 09 02 (for VIN number)')
    print ''
    print('WARNING: May result in vehicle malfunction')
    print('')

    # udsfloodmode0 = raw_input("Please enter mode (usually 2-digit hex): ")
    # udsfloodmode1 = int(udsfloodmode0, 16)
    udsfloodmode = str(format(FLOOD_MODE, 'X')).zfill(2)

    # udsfloodpid0 = raw_input("Please enter PID (usually 2-digit hex): ")
    # udsfloodpid1 = int(udsfloodpid0, 16)
    udsfloodpid = str(format(FLOOD_PID, 'X')).zfill(2)

    # floodnumber0 = raw_input("How many times would you like to send this message? ")
    floodnumber = str(FLOOD_NUMBER) # int(FLOOD_NUMBER)

    # floodinterval0 = raw_input("How long should the interval be (in seconds, floating point allowed)?: ")
    floodinterval = str(FLOOD_INTERVAL) #float(FLOOD_INTERVAL)

    print "Flooding with message MODE: " + udsfloodmode + " PID: " + udsfloodpid + " exactly " + floodnumber + " times, with an interval of " + floodinterval + " seconds"
    print ""

    udsentry = udsfloodmode + udsfloodpid + "\r"

    # udslogfile = "udslog_" + target + ".log"

    # udslog = open(udslogfile, 'wb')

    # udslog.write("-----------------------------------\n")
    # udslog.write("Mode & PID: " + udsfloodmode + " " + udsfloodpid + "\n")
    # udslog.write("Sent: " + floodnumber0 + " times\n")
    # udslog.write("Message interval: " + floodinterval0 + " seconds\n")
    # udslog.write("-----------------------------------\n")

    for i in range(FLOOD_NUMBER):
        try:
            connection.write(udsentry.encode())
            time.sleep(FLOOD_INTERVAL)
            udsresponse = connection.read(CONNECTION_READ_LEN)
            # udslog.write(udsresponse)
            print udsresponse
        except KeyboardInterrupt:
            print "Stop this test"
            return
            # udsagain = raw_input("You have stopped the test, would you like to try again (y/n)?: ")
            # if udsagain == 'y':
            #     udsflood()
            # elif udsagain == 'n':
            #     return #udslogfile
            # else:
            #     None

        # except Exception, e:
        #     print "Error: " + str(e)
        #     print "Please try again..."
        #     print ""
        #     udsflood()

    return #udslogfile

FLOOD_CANID = '777'
FLOOD_CANMSG = '1122334455667788'

def canmsg():
    print('-' * 45)
    print('+++++ CAN Message Injection')
    print('-' * 45)
    print(
    'The following tests for responses to CAN message injection.  The CAN ID should be set first (usually 3 hex digits) and then the rest of the message.  ')
    print('')
    print('If you need to stop for whatever reason, use CTRL+C')
    print ''
    print('WARNING: May result in vehicle malfunction')
    print('')
    # try:
    # canidquestion = raw_input('Please indicate the header (3 hex digits): ')
    canid = "ATSH " + FLOOD_CANID + "\r"
    connection.write(canid.encode())
    time.sleep(1)
    canidbytestoread = connection.inWaiting()
    canidresponse = connection.read(canidbytestoread)

    print canidresponse
    print ""

    # canflood0 = raw_input('Please indicate how many times you would like to send this message: ')
    canflood = int(FLOOD_NUMBER)

    # caninterval0 = raw_input(
    #     'How long should the interval between messages be (in seconds, floating point allowed)?: ')
    caninterval = str(FLOOD_INTERVAL) #float(caninterval0)
    print ""
    # print "Please type in the message you would like to send: "
    canmsgquestion = FLOOD_CANMSG # raw_input('8 bytes in hex format (e.g. AABBCCDD00112233): ')

    # canmsglog = "CANmessage_" + target + ".log"

    # canmsglogfile = open(canmsglog, 'wb')
    #
    # canmsglogfile.write("-----------------------------------\n")
    # canmsglogfile.write("CAN ID: " + canidquestion + "\n")
    # canmsglogfile.write("Data payload: " + canmsgquestion + "\n")
    # canmsglogfile.write("Sent: " + canflood0 + " times\n")
    # canmsglogfile.write("Message interval: " + caninterval0 + " seconds\n")
    # canmsglogfile.write("-----------------------------------\n")

    for i in range(FLOOD_NUMBER):#repeat(None, canflood):
        try:
            connection.write(canmsgquestion.encode())
            time.sleep(FLOOD_INTERVAL)
            canmsgresponse = connection.read(CONNECTION_READ_LEN)

            # canmsglogfile.write(canmsgresponse)
            print canmsgresponse
        except KeyboardInterrupt:
            print "Stop the test"
            return
            #canmsgagain = raw_input(
            #    "You have paused the test, would you like to enter different parameters (y), continue (n) or stop (CTRL+C)?: ")
            #if canmsgagain == 'y':
            #    canmsg()
            #elif canmsgagain == 'n':
            #    return #canmsglog
            #else:
            #    None

    # print ""

    # except KeyboardInterrupt:
    #     canmsgagain2 = raw_input("You have stopped the test, would you like to try again (y/n)?: ")
    #     if canmsgagain2 == 'y':
    #         canmsg()
    #     elif canmsgagain2 == 'n':
    #         return
    #     else:
    #         None
    # except Exception, e:
    #     print "Error: " + str(e)
    #
    return #canmsglog
