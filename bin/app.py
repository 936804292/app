#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from kz_opc import DBObject, UA_Object, UAStack
import json


def read_config():
    with open('../config/config.json', 'r') as f:
        data = f.read()
        result = json.loads(data)
    return result


if __name__ == "__main__":

    #read config
    result = read_config()
    jsonpath = result['OPCUA_SERVER']['TagPath']
    endpoint = result['OPCUA_SERVER']['EndPoint']
    uri = result['OPCUA_SERVER']['uri']
    PLC_IP = result['S7PLC']['IP']
    PLC_DBNumber = int(result['S7PLC']['DB_Number'])
    logPath = result['OPCUA_SERVER']['logPath']
    security_num = int(result['security']['security_num'])
    my_cert = result['security']['certificate']
    private_key = result['security']['private-key']

    if security_num == 0:
        myua = UA_Object(endpoint, uri, security_num)
        myua.set_security()
    if security_num == 1:
        myua = UA_Object(endpoint, uri, security_num)
        myua.set_security()
        myua.server.load_certificate(my_cert)
        myua.server.load_private_key(private_key)

    #init opcua_server
    json_res = myua.read_json(jsonpath)
    s_tags = myua.get_server_tagName(json_res)
    serverObj = myua.add_serverName(json_res)
    tagNodeObj = myua.add_tagName(s_tags, serverObj)
    myua.server.start()

    db = DBObject()
    db.client.connect(PLC_IP, rack=0, slot=1)
    length = db.get_db_length(json_res)

    try:
        while True:
            _stack = UAStack()
            plc_data = db.DBRead(PLC_DBNumber, length, json_res, _stack)
            myua.change_node(plc_data, tagNodeObj)
    finally:
        myua.server.stop()