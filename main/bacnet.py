import json
import logging

import requests

# logging.basicConfig(level=logging.INFO)

# HVAC Settings

zone_north_temp = "BACnet_101_Room_Temperature.PRESENT_VALUE"

zone_north_low = "BACnet_102_Room_Setpoint_-_low_limit.PRESENT_VALUE"
zone_north_low_set = "BACnet_102_Room_Setpoint_-_low_limit.SET_VALUE"

zone_north_high = "BACnet_102_Room_Setpoint_-_high_limit.PRESENT_VALUE"
zone_north_high_set = "BACnet_102_Room_Setpoint_-_high_limit.SET_VALUE"


zone_west_temp= "BACnet_101_Room_Temperature.PRESENT_VALUE"

zone_west_low = "BACnet_101_Room_Setpoint_-_low_limit.PRESENT_VALUE"
zone_west_low_set = "BACnet_101_Room_Setpoint_-_low_limit.SET_VALUE"

zone_west_high = "BACnet_101_Room_Setpoint_-_high_limit.PRESENT_VALUE"
zone_west_high_set = "BACnet_101_Room_Setpoint_-_high_limit.SET_VALUE"


# Light Settings

zone_1_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_1_Window_Level.PRESENT_VALUE"
zone_1_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_1_Window_Level.SET_VALUE"

zone_2_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_2_Window_Level.PRESENT_VALUE"
zone_2_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_2_Window_Level.SET_VALUE"

zone_3_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_3_Window_Level.PRESENT_VALUE"
zone_3_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_3_Window_Level.SET_VALUE"

zone_4_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_4_Window_Level.PRESENT_VALUE"
zone_4_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_4_Window_Level.SET_VALUE"

zone_5_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_5_Window_Level.PRESENT_VALUE"
zone_5_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_5_Window_Level.SET_VALUE"

zone_6_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_6_Window_Level.PRESENT_VALUE"
zone_6_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_6_Window_Level.SET_VALUE"

zone_7_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_7_Window_Level.PRESENT_VALUE"
zone_7_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_7_Window_Level.SET_VALUE"

zone_8_window_light = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_8_Window_Level.PRESENT_VALUE"
zone_8_window_light_set = "BACnet_OPEN_OFFICE_406_1761004_Open_Office_Zone_8_Window_Level.SET_VALUE"


# Roller Sun Blinds

roller_blind_left = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Left_1-1-B-14_Level.PRESENT_VALUE"
roller_blind_left_set = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Left_1-1-B-14_Level.SET_VALUE"

roller_blind_center = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Center_1-1-B-15_Level.PRESENT_VALUE"
roller_blind_center_set = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Center_1-1-B-15_Level.PRESENT_VALUE"

roller_blind_right = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Right_1-1-B-16_Level.PRESENT_VALUE"
roller_blind_right_set = "BACnet_OPEN_OFFICE_406_1761004_Shade_Group_Shade_Right_1-1-B-16_Level.SET_VALUE"


PI_WEBAPI_URL = "https://sbb03.eecs.berkeley.edu/piwebapi"
PI_WEBAPI_USERNAME = "albertxu"
PI_WEBAPI_PASSWORD = "Welcome2pi"

piwebapi_sess = requests.Session()
piwebapi_sess.auth = (PI_WEBAPI_USERNAME, PI_WEBAPI_PASSWORD)


def get_web_id(name):
    req = piwebapi_sess.get("{0}/points?path=\\\\sbb03.eecs.berkeley.edu\\{1}".format(PI_WEBAPI_URL, name), verify=True)
    if req.status_code == requests.codes.ok:
        results = req.json()
        web_id = results['WebId']
        return web_id
    else:
        return None


def set_pi_bacnet(tag, value):
    # need to swap out the "PRESENT_VALUE" tag for a "SET_VALUE" tag for Pi based control of BACnet Resources.

    web_id = get_web_id(tag)

    # use the PI * = Now convention instead.
    data = {"Timestamp": "*", "Value": value}

    req = piwebapi_sess.post("{0}/streams/{1}//value".format(PI_WEBAPI_URL, web_id), data=json.dumps(data),
                             headers={'Content-type': 'application/json'})
    if req.status_code == requests.codes.ok:
        logging.info("Successfully Posted")
    else:
        req.raise_for_status()


def get_pi_bacnet(tag, interval, start, end):
    # need to swap out the "PRESENT_VALUE" tag for a "SET_VALUE" tag for Pi based control of BACnet Resources.

    web_id = get_web_id(tag)

    req = piwebapi_sess.get(
        "{0}/streams/{1}/interpolated?interval={2}&startTime={3}&endTime={4}".format(PI_WEBAPI_URL, web_id, interval, start, end))
    if req.status_code == requests.codes.ok:
        results = req.json()
        return results
    else:
        req.raise_for_status()

def getHVAC(loc, kat):
    temp = ""
    if(loc == "north"):
        if kat == "low":
            temp = zone_north_low
        elif kat == "high":
            temp = zone_north_high
        else:
            temp = zone_north_temp
    else:
        if kat == "low":
            temp = zone_west_low
        elif kat == "high":
            temp = zone_west_high
        else:
            temp = zone_west_temp

    data = get_pi_bacnet(temp, '1s', '-1s', '*')
    return int(data['Items'][-1]['Value'])

def getLighting(zoneNum):
    temp = ""
    if zoneNum == 1:
        temp = zone_1_window_light
    if zoneNum == 2:
        temp = zone_2_window_light
    if zoneNum == 3:
        temp = zone_3_window_light
    if zoneNum == 4:
        temp = zone_4_window_light
    if zoneNum == 5:
        temp = zone_5_window_light
    if zoneNum == 6:
        temp = zone_6_window_light
    if zoneNum == 7:
        temp = zone_7_window_light
    if zoneNum == 8:
        temp = zone_8_window_light
        
    data = get_pi_bacnet(temp, '10m', '-10m', '*')
    return int(data['Items'][-1]['Value'])

def setHVAC(loc, kat, temperature):
    temp = ""

    if(loc == "north"):
        if kat == "low":
            temp = zone_north_low_set
        else:
            temp = zone_north_high_set
    else:
        if kat == "low":
            temp = zone_west_low_set
        else:
            temp = zone_west_temp_set

    set_pi_bacnet(temp, temperature)

def setLighting(zoneNum, brightness):
    temp = ""

    if zoneNum == 1:
        temp = zone_1_window_light_set
    if zoneNum == 2:
        temp = zone_2_window_light_set
    if zoneNum == 3:
        temp = zone_3_window_light_set
    if zoneNum == 4:
        temp = zone_4_window_light_set
    if zoneNum == 5:
        temp = zone_5_window_light_set
    if zoneNum == 6:
        temp = zone_6_window_light_set
    if zoneNum == 7:
        temp = zone_7_window_light_set
    if zoneNum == 8:
        temp = zone_8_window_light_set

    set_pi_bacnet(temp, brightness)




# READ data from PI (10 minute data from 1 hour ago until present)

#data = get_pi_bacnet(zone_3_window_light, '10m', '-10m', '*')
#print(int(data['Items'][0]['Value']))


# read data from PI (hourly  data from 1 day ago until present)

#data = get_pi_bacnet(zone_north_temp, '1h', '-1d', '*')
#logging.info(data)


# read data from PI (hourly data from specified date until present)

#data = get_pi_bacnet(roller_blind_left, '1h', '2016-11-28', '*')
#logging.info(data)



# SET data to PI output tags in PI (which PI sends to BACnet)


# set brightness to 80%
#set_pi_bacnet(zone_8_window_light_set, 80)

# set high setpoint temp to 74
#set_pi_bacnet(zone_north_high_set, 74)

# set left rollerblind to 100% open
#set_pi_bacnet(roller_blind_left_set, 100)


