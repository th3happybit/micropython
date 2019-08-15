import network

def connect():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    wlan.scan()             # scan for access points
    wlan.isconnected()      # check if the station is connected to an AP
    wlan.connect('DJAWEB', 'intoNet=x=2x=3x') # connect to an AP
    wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses