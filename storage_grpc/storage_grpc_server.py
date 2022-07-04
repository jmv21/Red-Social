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
import re
import time
from xml.etree.ElementTree import tostring

import grpc


from storage_grpc.storage_pb2 import  AddressS, Address_listS, Bool, DataS, FeatureS, Log_token, StorageS
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
        
        list_addr = [(item.value, item.addr) for item in request.values]
        
        self.storage_node.update_node_list(list_addr)
        return FeatureS(name="ACK")
    
    def Get_stor_nodes(self, request, context):
        print("entered in get stor nodes")
        ad_list =[]
        
        for node in self.storage_node.storage_nodes:
            if node is not None:
                ad_list.append(AddressS(value=node[0], addr=node[1])) 
                
            else:
                ad_list.append(AddressS(value=0, addr='0'))
        addrs =  Address_listS(values=ad_list)
        return addrs
    

    def Ask_for_file(self, request, context):
        with open(request.name, 'rb') as content_file:
            content = content_file.read()
        response = DataS(data=content)
        yield response

    def Ask_if_name_belongs(self, request, context):
        res = self.storage_node.name_exist(request.name)
        return Bool(b=res)
    
    def Register_user(self, request, context):
        res, token = self.storage_node.register( request.name, request.password, request.value)
        return Log_token(b=res,token = token)

    def Login_user(self, request, context):
        res, token, id = self.storage_node.login(self, request.name, request.password, request.value)
        return Log_token(b=res,token=token, value=id)
    
    def Random_n(self, request, context):
        content = self.storage_node.random_n(request.value)
        response = DataS(data=content)
        yield response

    def Get_following(self, request, context):
        content = self.storage_node.get_following(request.value)
        return content
    
    def Followed_tweets(self, request, context):
        content = self.storage_node.followed_tweets(request.values)
        response = DataS(data=content)
        yield response
    
    def Tweet(self, request, context):
        self.storage_node.tweet(request.addr, request.value)
        return FeatureS(name="ACK")
    
    def Retweet(self, request, context):
        self.storage_node.tweet(request.value, request.text, request.tweet_value, request.ret_user_value, request.ret_user_name)
        return FeatureS(name="ACK")
    
    def Comment(self, request, context):
        self.storage_node.tweet(request.vaue, request.text, request.tweet_value, request.ret_user_value, request.ret_user_name)
        return FeatureS(name="ACK")