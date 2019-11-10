from treelib import Tree, Node

def create_attack_tree():
    tree_empty = Tree()

    tree_empty.create_node("GOAL: Vehicle Compromise", "vehiclecomp")

    # # RECONNAISSANCE
    # tree_empty.create_node("SAND:1 Reconnaissance", "recon", parent="vehiclecomp")
    # # OBD-II device information
    # tree_empty.create_node("AND: OBD-II Device Information", "obd2info", parent="recon")
    # tree_empty.create_node("AND: Determine Bluetooth address", "obd2info_btaddr", parent="obd2info")
    # tree_empty.create_node("OR: Scan for devices using hcitool", "obd2info_btaddr_scan", parent="obd2info_btaddr")
    # tree_empty.create_node("OR: Read label", "obd2info_btaddr_read", parent="obd2info_btaddr")
    # tree_empty.create_node("OR: Use bluetoothctl", "obd2info_btaddr_bctl", parent="obd2info_btaddr")
    #
    # tree_empty.create_node("AND: Determine ELM327 version", "obd2info_elm", parent="obd2info")
    # tree_empty.create_node("OR: Use AT commands (ATI)", "obd2info_elm_at", parent="obd2info_elm")
    # tree_empty.create_node("OR: Read manual", "obd2info_elm_read", parent="obd2info_elm")
    # tree_empty.create_node("AND: Determine serial port channel", "obd2info_channel", parent="obd2info")
    # tree_empty.create_node("OR: Use Service Discovery Protocol", "obd2info_channel_sdp", parent="obd2info_channel")
    # tree_empty.create_node("OR: Trial and error connections to open ports", "obd2info_channel_trial",
    #                        parent="obd2info_channel")
    #
    # tree_empty.create_node("AND: Determine baudrate", "obd2info_baudrate", parent="obd2info")
    # tree_empty.create_node("AND: Determine pairing mechanism", "obd2info_pairing", parent="obd2info")
    # tree_empty.create_node("OR: View device information (hcitool info)", "obd2info_pairing_info",
    #                        parent="obd2info_pairing")
    # tree_empty.create_node("OR: Read manual", "obd2info_pairing_read", parent="obd2info_pairing")
    # tree_empty.create_node("OR: Use bluetoothctl", "obd2info_pairing_bctl", parent="obd2info_pairing")
    #
    # # Vehicle information
    # tree_empty.create_node("AND: Vehicle information", "vehicleinfo", parent="recon")
    # tree_empty.create_node("OR: VIN number", "vehicle_vin", parent="vehicleinfo")
    # tree_empty.create_node("OR: Read Voltage", "vehicleinfo_voltage", parent="vehicleinfo")
    # tree_empty.create_node("OR: Determine current protocol", "vehicleinfo_protocol", parent="vehicleinfo")
    # tree_empty.create_node("OR: Determine CAN status", "vehicleinfo_can", parent="vehicleinfo")
    # tree_empty.create_node("OR: Read stored data", "vehicleinfo_stored", parent="vehicleinfo")
    # tree_empty.create_node("OR: Read IgnMon input level", "vehicleinfo_ignmon", parent="vehicleinfo")
    # tree_empty.create_node("OR: Display keywords", "vehicleinfo_keywords", parent="vehicleinfo")
    # tree_empty.create_node("OR: Display program parameters summary", "vehicleinfo_params", parent="vehicleinfo")

    # DEVICE CONNECTION
    tree_empty.create_node("SAND:2 Connect to device", "connect", parent="vehiclecomp")
    tree_empty.create_node("OR: Using legitimate device", "connect_legit", parent="connect")
    tree_empty.create_node("SAND:1 Determine pairing status", "connect_legit_pairing", parent="connect_legit")
    tree_empty.create_node("SAND:2 Connect to serial port", "connect_legit_serial", parent="connect_legit")

    tree_empty.create_node("OR: Spoof previously paired device", "connect_spoof", parent="connect")
    tree_empty.create_node("AND: Find the link key from local or remote device", "connect_spoof_linkkey",
                           parent="connect_spoof")
    tree_empty.create_node("AND: Change address of local device", "connect_spoof_changeaddr", parent="connect_spoof")

    # Vehicle Compromise
    tree_empty.create_node("SAND:3 Cause Vehicle Compromise", "vehcomp", parent="vehiclecomp")
    tree_empty.create_node("OR: Using UDS messages", "vehcomp_uds", parent="vehcomp")
    tree_empty.create_node("OR: Flood with set UDS messages", "vehcomp_flooduds", parent="vehcomp_uds")
    tree_empty.create_node("OR: Run through all messages", "vehcomp_runthru", parent="vehcomp")
    tree_empty.create_node("SAND:1 Run through 00 00 to 0A FF (standard)", "vehcomp_uds_sobd", parent="vehcomp_runthru")
    tree_empty.create_node("SAND:2 Run through 0B 00 to FF FF (non-standard)", "vehcomp_uds_nobd", parent="vehcomp_runthru")

    tree_empty.create_node("OR: Flooding with raw CAN messages", "vehcomp_can", parent="vehcomp")
    tree_empty.create_node("SAND:1 Predetermine CAN messages", "vehcomp_can_pre", parent="vehcomp_can")
    tree_empty.create_node("OR: Using passive monitoring", "vehcomp_can_pre_mon", parent="vehcomp_can_pre")
    tree_empty.create_node("OR: Using OEM CAN database", "vehcomp_can_pre_candb", parent="vehcomp_can_pre")
    tree_empty.create_node("OR: Using reverse engineering", "vehcomp_can_pre_rev", parent="vehcomp_can_pre")
    tree_empty.create_node("SAND:2 Send (flood with) CAN messages", "vehcomp_can_send", parent="vehcomp_can")
    return tree_empty
