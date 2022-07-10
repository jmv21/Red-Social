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
"""The Python implementation of the gRPC route guide client."""

from __future__ import print_function

import logging
from os import name
import random

import grpc
import gRPC.route_guide_pb2
import gRPC.route_guide_pb2_grpc


def make_route_note(message, latitude, longitude):
    return gRPC.route_guide_pb2.RouteNote(
        message=message,
        location=gRPC.route_guide_pb2.Point(latitude=latitude, longitude=longitude))


def guide_alive(stub, name):
    feature = stub.Alive(name)
    if not feature.name == "ACK":
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s" % (feature.name))
    else:
        print("Found no feature")


def alive(stub):
    guide_alive(stub, gRPC.route_guide_pb2.Feature(name="IS ALIVE"))

class GrpcClient:

    def __init__(self, channel):
        self.channel = grpc.insecure_channel(channel)
        self.stub = gRPC.route_guide_pb2_grpc.RouteGuideStub(self.channel)
    
    def close(self):
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()




def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('172.17.0.2:8080') as channel:
        stub = gRPC.route_guide_pb2_grpc.RouteGuideStub(channel)
        print("-------------- GetFeature --------------")
        alive(stub)
        #print("-------------- ListFeatures --------------")
        #guide_list_features(stub)
        #print("-------------- RecordRoute --------------")
        #guide_record_route(stub)
        #print("-------------- RouteChat --------------")
        #guide_route_chat(stub)


#if __name__ == '__main__':
    #logging.basicConfig()
    #run()
