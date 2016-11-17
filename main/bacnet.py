import json
import logging
import requests

zone_north_low = "BACnet_102_Room_Setpoint_-_low_limit.SET_VALUE"
zone_north_high = "BACnet_102_Room_Setpoint_-_high_limit.SET_VALUE"

zone_west_low = "BACnet_101_Room_Setpoint_-_low_limit.SET_VALUE"
zone_west_high = "BACnet_101_Room_Setpoint_-_high_limit.SET_VALUE"



PI_WEBAPI_URL = "https://sbb03.eecs.berkeley.edu/piwebapi"
PI_WEBAPI_USERNAME = "ruoxijia"
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
        logging.info("Messed Up Somewhere")
        req.raise_for_status()



set_pi_bacnet(zone_west_high,73)