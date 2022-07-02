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
from distutils.log import error
import logging
import math
import time
from xml.etree.ElementTree import tostring

import grpc

from gRPC.chord_pb2 import  Address, Address_list, Feature, Storage
#import route_guide_pb2
import gRPC.chord_pb2_grpc

#import chord_node
#from chord_node import Node


class ChordServicer(gRPC.chord_pb2_grpc.RouteGuideServicer):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, node):
        self.chord_node = node

    def Alive(self, request, context):
        return Feature(name="ACK")

    def Join(self, request, context):
        return Feature(name="ACK")

    #def Get_params not defined
    #def Get_prop not defined

    def Find_succ(self, request, context):
        n_id, n_addr = self.chord_node.find_successor(request.value)
        return Address(value=n_id, addr=n_addr)

    def Find_pred(self, request, context):
        print(request)
        n_id, n_addr = self.chord_node.find_predecessor(request.value)
        #n_addr = "{}".format(n_addr)
        return Address(value=n_id, addr=n_addr)

    def Get_succ_list(self, request, context):
        addr_list = self.chord_node.get_succ_list()
        to_ret = []
        for item in addr_list:
            to_ret.append(Address(value=item[0], addr=item[1]))
        return Address_list(values=to_ret)
    
    def Closest_pred_fing(self, request, context):
        n_id, n_addr = self.chord_node.closest_pred_fing(request.value)
        return Address(value=n_id, addr=n_addr)

    def Get_pred(self, request, context):
        n_id, n_addr = self.chord_node.get_pred()
        return Address(value=n_id, addr=n_addr)

    def Rectify(self, request, context):
        self.chord_node.rectify(request.value, request.addr)
        return Feature(name="ACK")

    def Get_storage(self, request, context):
        st_is_storage, st_addr, st_found, st_error = self.chord_node.closest_storage_node(request.addr)
        return Storage(addr=st_addr, is_storage=st_is_storage, found=st_found, error=st_error)

    def Get_non_storage(self, request, context):
        st_is_storage, st_addr, st_found, st_error = self.chord_node.closest_non_storage_node(request.addr)
        return Storage(addr=st_addr, is_storage=st_is_storage, found=st_found, error=st_error)

    def Make_storage(self, request, context):
        print("9")
        self.chord_node.make_storage(request.K, request.index, request.nodes.values)
        return Feature(name="ACK")
    
    def Remove_storage(self, request, context):
        self.chord_node.remove_storage()
        return Feature(name="ACK")


