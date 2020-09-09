#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from kz_opc import DBObject, UA_Object, UAStack
import json, time, logging, os.path


def read_config(config_dir):
    with open(config_dir, 'r') as f:
        data = f.read()
        return json.loads(data)

def get_config_arr():
    config_dir = os.path.dirname(os.getcwd()+'/config/')
    config_file = os.path.join(config_dir, "config.json")
    result = read_config(config_file)
    return config_dir, config_file, result

def set_log():
    logger = logging.getLogger()
    logger.setLevel(logging.WARN)
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_dir = os.path.dirname(os.getcwd()+'/logs/')
    log_name = log_dir+'/'+rq+'.log'
    file_handle = logging.FileHandler(log_name, mode='w')
    file_handle.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    file_handle.setFormatter(formatter)
    logger.addHandler(file_handle)
    return logger

def run():
    config_dir, config_file, result = get_config_arr()

    security_dir = os.path.dirname(os.getcwd() + '/security/')

    tag_dir = result['OPCUA_SERVER']['TagFile']
    tag_file = os.path.join(config_dir, tag_dir)

    endpoint = result['OPCUA_SERVER']['EndPoint']
    uri = result['OPCUA_SERVER']['uri']
    PLC_IP = result['OPCDA_CLIENT']['IP']
    PLC_DBNumber = int(result['OPCDA_CLIENT']['DB_Number'])
    security_num = int(result['security']['security_num'])

    my_cert_dir = result['security']['certificate']
    my_cert = os.path.join(security_dir, my_cert_dir)
    private_key_dir = result['security']['private-key']
    private_key = os.path.join(security_dir, private_key_dir)

    logger = set_log()

    if security_num == 0:
        logger.warning('NoSecurity')
        myua = UA_Object(endpoint, uri, security_num)
        myua.set_security()
    if security_num == 1:
        logger.warning('Basic256Sha256_SignAndEncrypt')
        myua = UA_Object(endpoint, uri, security_num)
        myua.set_security()
        myua.server.load_certificate(my_cert)
        myua.server.load_private_key(private_key)
    #init opcua_server
    json_res = myua.read_json(tag_file)
    s_tags = myua.get_server_tagName(json_res)
    serverObj = myua.add_serverName(json_res)
    tagNodeObj = myua.add_tagName(s_tags, serverObj)
    myua.server.start()
    logger.warning('--------------------OpcUA server started!--------------------------')

    db = DBObject()
    try:
        db.client.connect(PLC_IP, rack=0, slot=1)
    except Exception as ex:
        logger.error(ex)
    finally:
        logger.warning('-----------')

    length = db.get_db_length(json_res)

    try:
        while True:
            _stack = UAStack()
            plc_data = db.DBRead(PLC_DBNumber, length, json_res, _stack)
            myua.change_node(plc_data, tagNodeObj)

    finally:
        if db.client.get_connected():
            db.client.disconnect()
            logger.warning('OpcDA client has been disconnected;')

            myua.server.stop()
            logger.warning('OpcUA server has been disconnected;')


if __name__ == "__main__":
    run()