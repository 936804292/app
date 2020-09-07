#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
from snap7.util import *
from threading import Thread
import snap7, json, time
from opcua import ua, uamethod, Server


class StackUnderflow(ValueError):
    pass


class UAStack:
    def __init__(self):
        self._elems = []
        self.current_num = 0

    def is_empty(self):
        return self._elems == []

    def push(self, elem):
        self._elems.append(elem)

    def pop(self):
        if self._elems == []:
            raise StackUnderflow("in UAStack.pop()")
        return self._elems.pop()

    def top(self):
        if self._elems == []:
            raise StackUnderflow("in UAStack.top()")
        return self._elems[-1]

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_num<len(self._elems):
            temp = self._elems[self.current_num]
            self.current_num += 1
            return temp
        else:
            raise StopIteration


class VarUpdater(Thread):
    def __init__(self, var, value):
        Thread.__init__(self)
        self._stopev = False
        self.var = var
        self.value = value

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            self.var.set_value(self.value)


class DBObject(object):

    def __init__(self):
        self.client = snap7.client.Client()
        self.offset = {"Bool": 2, "Int": 2, "Real": 4, "Dint": 4, "String[12]": 256}
        self.DB = snap7.snap7types.areas.DB
        # self.MK = snap7.snap7types.areas.MK

    def get_db_length(self, json_data):
        a = list()
        b = list()
        for k, v in json_data.items():
            for i, j in v.items():
                a.append(k)                 #tagName
                b.append(int(float(j)))     #tagValue
        max_value_type = max(zip(b, a))

        return max_value_type[0] + self.offset[max_value_type[1]]

    def DBRead(self, db_num, length, arr, _stack):
        data = self.client.read_area(self.DB, db_num, 0, length)
        for types, val in arr.items():
            for tname, _value in val.items():
                value = None
                offset = int(_value.split('.')[0])
                if types == "Real":
                    value = get_real(data, offset)
                    _stack.push({tname: value})
                if types == "Bool":
                    bit = int(_value.split('.')[1])
                    value = get_bool(data, offset, bit)
                    _stack.push({tname: value})
                if types == "Int":
                    value = get_int(data, offset)
                    _stack.push({tname: value})
                if types == "String[12]":
                    value = get_string(data, offset, 256)
                    _stack.push({tname: value})
                else:
                    continue
        return _stack


class UA_Object(object):

    def __init__(self, url, spaceName, security_num):
        self.server = Server()
        self.endPoint = self.server.set_endpoint(url)
        self.security_num = security_num
        self.spaceName = self.server.register_namespace(spaceName)
        self.node_obj = self.server.get_objects_node()  # root_id

    def set_security(self):
        security = [ua.SecurityPolicyType.NoSecurity,
                    ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                    ua.SecurityPolicyType.Basic256Sha256_Sign]
        self.server.set_security_policy([security[self.security_num]])

    def read_json(self, jsonPath):
        with open(jsonPath, 'r') as f:
            data = f.read()
            return json.loads(data)

    def get_server_tagName(self, jsonDict):
        s_server_tag = UAStack()
        for k, v in jsonDict.items():
            for i, j in v.items():
                s_server_tag.push({k: i})
        return s_server_tag

    def add_serverName(self, s_tags):
        temp = list()
        for k in s_tags.keys():
            serverObj = self.node_obj.add_object(self.spaceName, str(k))
            temp.append(serverObj)
        return temp

    def get_browse_name(self, tagNameObj):
        temp = list()
        for nodeObj in tagNameObj:
            tag_TagName = nodeObj.get_browse_name().Name
            temp.append(tag_TagName)
        return temp

    def add_tagName(self, s_tags, serverObj):
        tagNameObj = list()
        for val in s_tags:
            for q, w in val.items():
                for i in serverObj:
                    serverName = i.get_browse_name().Name
                    if serverName == q:
                        tag = i.add_variable(self.spaceName, w, None)
                        tag.set_writable()
                        tagNameObj.append(tag)
        return tagNameObj

    def change_node(self, res_stack, tagNodeObj):
        for tagObj in tagNodeObj:
            b_name = tagObj.get_browse_name().Name
            for values in res_stack:
                if b_name in values:
                    tagObj.set_value(values[b_name])
                    break
