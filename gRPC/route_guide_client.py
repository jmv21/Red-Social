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
import gRPC.chord_pb2
import gRPC.chord_pb2_grpc


class GrpcClient:

    def __init__(self, channel):
        self.channel = grpc.insecure_channel(channel)
        self.stub = gRPC.chord_pb2_grpc.RouteGuideStub(self.channel)
    
    def close(self):
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()


