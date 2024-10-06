import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 
api_url = "https://<ip address>/restconf"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json",
            "Content-type": "application/yang-data+json"
           }
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070104",
            "description": "create loopback",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": "172.30.104.1",
                        "netmask": "255.255.255.0"
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }

    resp = requests.put(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070104", 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )
    if(resp.status_code == 204):
        return "Cannot create: Interface loopback 65070104"
    elif(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070104 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete():
    resp = requests.delete(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070104", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "loopback 65070104 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 65070104"


def enable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070104",
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
        }
    }


    resp = requests.patch(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070104",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070104 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 65070104"

def disable():
    yangConfig = {
        "ietf-interfaces:interface": {
            "name": "Loopback65070104",
            "type": "iana-if-type:softwareLoopback",
            "enabled": False,
        }
    }

    resp = requests.patch(
        api_url+"/data/ietf-interfaces:interfaces/interface=Loopback65070104",
        data=json.dumps(yangConfig),
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070104 is disabled"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 65070104"

def status():
    api_url_status = "https://10.0.15.111/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070104"

    resp = requests.get(
        api_url_status,
        auth=basicauth,
        headers=headers,
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        #print(json.dumps(response_json, indent=4))
        admin_status = response_json["ietf-interfaces:interfaces-state"]["interface"][0]["admin-status"]
        oper_status = response_json["ietf-interfaces:interfaces-state"]["interface"][0]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback65070104 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback65070104 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 65070104"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
