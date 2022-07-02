# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC route guide server."""

from array import array
from concurrent import futures
import logging
import math
import time
from xml.etree.ElementTree import tostring

import grpc


from storage_grpc.storage_pb2 import  AddressS, Address_listS, DataS, FeatureS, StorageS
#import route_guide_pb2
import storage_grpc.storage_pb2_grpc

#import chord_node
#from chord_node import Node


class StorageServicer(storage_grpc.storage_pb2_grpc.StorageServicerServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, node):
        self.storage_node = node

    def Alive(self, request, context):
        return FeatureS(name="ACK")

    def Update_list(self, request, context):
        print("kla")
        list_addr = [(item.value, item.addr) for item in request.values]
        print("klap")
        self.storage_node.update_node_list(list_addr)
        return FeatureS(name="ACK")

    def Ask_for_file(self, request, context):
        #file_name = self.storage_node.parse_to_json('DB1')
        #print("first try")
        #response = str(file_name).encode('utf-8')
        #print("parsed")
        #file_name = open('DB1', 'rb')
        #response = file_name.read()
        with open('DB1', 'rb') as content_file:
            content = content_file.read()
        #yield my_generated_module_pb2.Response(data=content)
        response = DataS(data=content)
        yield response