from test_cases import *
# mapping from action to primitive function
from primitive_test import *

act_func = {
    "action_Change_address_of_local_device" : None,
    "action_Connect_to_serial_port" : connect_to_serial_port,
    "action_Determine_baudrate" : None, #determine_baudrate,
    "action_Determine_CAN_status" : determine_CAN_status,
    "action_Determine_current_protocol" : determine_current_protocol,
    "action_Determine_pairing_status" : determine_pairing_status,
    "action_Display_keywords" : determine_keywords,
    "action_Display_program_parameters_summary" : determine_program_parameters_summary,
    "action_Find_the_link_key_from_local_or_remote_device" : None,
    "action_Flood_with_set_UDS_messages" : udsflood,
    "action_Read_IgnMon_input_level" : determine_IgnMon_input_level,
    "action_Read_label" : None,
    "action_Read_manual" : None,
    "action_Read_stored_data" : determine_stored_data,
    "action_Read_Voltage" : determine_voltage,
    "action_Run_through_00_00_to_0A_FF__standard_" : standardobd,
    "action_Run_through_0B_00_to_FF_FF__non_standard_" : nonstandardobd,
    "action_Scan_for_devices_using_hcitool" : determine_devices_using_hcitool,
    "action_Send__flood_with__CAN_messages" : canmsg,
    "action_Trial_and_error_connections_to_open_ports" : None,
    "action_Use_AT_commands__ATI_" : determine_ELM327_use_AT_commands,
    "action_Use_bluetoothctl" : None,
    "action_Use_Service_Discovery_Protocol" : detemrine_services,
    "action_Using_OEM_CAN_database" : None,
    "action_Using_passive_monitoring" : monitoring,
    "action_Using_reverse_engineering" : None,
    "action_View_device_information__hcitool_info" : None, #dev_information,
    "action_VIN_number" : determine_vin
    }


def exec_all_test_cases():
    n = 0
    test_results = ""
    for tc in Test_Cases:
        n += 1
        try:
            for a in tc:
                if act_func[a] is None:
                    raise ValueError(a)
        except ValueError as e:
            print("Test case " + str(n) + ": unexecutable " + e.message + "")
            test_results += "Test case " + str(n) + ": unexecutable action " + e.message + "\n"
            continue

        print('Test case ' + str(n)  + ' : ' + '->'.join(tc) )
        raw_input('Enter to try this test case')

        try:
            for a in tc:
                fc = act_func[a]
                fc()
            print("Test case " + str(n) + ": Passed")
            test_results += "Test case " + str(n) + ": Passed\n"
        except:
            print("Test case " + str(n) + ": Failed")
            test_results += "Test case " + str(n) + ": Failed\n"
    rs_file = open("test_report.txt","w")
    rs_file.write(test_results)
    rs_file.close()

    release_serial_port()