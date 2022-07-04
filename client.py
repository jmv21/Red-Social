
from ast import arg
import ctypes
from socket import gethostbyname, gethostname
#import zmq
import argparse
import re

import grpc
import chord_node
import threading
from time import time
from gRPC.chord_pb2 import Address, Feature
from storage_grpc.storage_pb2 import Comment_info, FeatureS, Id_list, IdvalueS, User_data
import storage_node
import multiprocessing
import netaddr
import uuid
from DB import load_json_to_database





class Client:
    def __init__(self, ip_port, chord_args,storage = None):
        self.id = uuid.uuid4().int & (1<<63)-1
        chord_args.append(self.id)
        self.c_node = chord_node.Node(*chord_args)
        self.c_node.bind_client(self)
        self.id = uuid.uuid4().int & (1<<63)-1
        self.token = None

        self.ip_port = self.c_node.addr
        self._storage = False
        if storage is not None: self._storage = True
        self.storage_node = storage

        K = 2
        self.ranges = storage_node.define_ranges(K,pow(2, 63) -1, 0)
        if ip_port == '172.17.0.2:8080':
            self._storage = True
            self.storage_node = storage_node.StorageNode(ip_port, K, 0, storage_nodes=None, vocal_option=True)
            

        
        
        
        
        ip, port = self.ip_port.split(":")[0], self.ip_port.split(":")[1]
        port = int(port) + 1
        self.ip = ip
        self.ip_port = ip + ":{}".format(port)
        
 
        self.waiting_time = 20

   
        #if self.ip == '172.17.0.2': 
            #print('started thread')
            #thr_stabilize = threading.Thread(target = self.ask_myself, args =())
            #thr_stabilize.start()
        
        #self.c_node.bind_client(self)

        self.send_info()
        
    
    


    def ask_myself(self):
        countdown = time()
        

    def send_info(self):
        a = True
        
            

    def is_storage(self):
        return self._storage
    
    def make_storage_wrapper(self, K, index, storage_nodes):
        return

    #def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
    def make_storage_node(self, K, index, storage_nodes):
        
        self.storage_node = storage_node.StorageNode(self.c_node.addr, K, index, storage_nodes)
        self._storage = True

    def remove_storage(self):
        self._stop_threads([self.storage_node.thr_wait_for_command, self.storage_node.thr_check_succ])
        
    def storage_contains(self, id):
        return self.storage_node.contains(id)
        
        
      
    
    def _stop_threads(self, threads):

        for item in threads:
            thread = item
            exc = ctypes.py_object(SystemExit)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_long(thread.ident), exc)
            if res == 0:
                raise ValueError("nonexistent thread id")
            elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")
    
    def login(self, name, password):
        # Get closest storage node
        stub = chord_node.make_stub_chord(self.c_node.addr)
       
        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return False, 'error'

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
            return False, 'error'
        
        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        # ASK IF CORRESPONDING STOR BY ID CONTAINS THIS USER NAME
        stub = storage_node.make_stub_stor(stor_nodes[index][1])
        try:
            log_try = stub.Login_user(User_data(name=name, password=password, value=self.id))
            if log_try.b:
                self.token = log_try.token
                self.id = log_try.value
                return True, log_try.token
        except grpc.RpcError as e:
            pass

        
        # If is not in corresponding nodes ask the rest of the storage nodes
        for i in range(index):
            stub = storage_node.make_stub_stor(stor_nodes[i][1])
            try:
                log_try = stub.Login_user(User_data(name=name, password=password, value=self.id))
                if log_try.b:
                    self.token = log_try.token
                    self.id = log_try.value
                    return True, log_try.token
            except grpc.RpcError as e:
                pass
        
        for i in range(index, len(stor_nodes)):
            stub = storage_node.make_stub_stor(stor_nodes[i][1])
            try:
                log_try = stub.Login_user(User_data(name=name, password=password, value=self.id))
                if log_try.b:
                    self.token = log_try.token
                    self.id = log_try.value
                    return True, log_try.token
            except grpc.RpcError as e:
                pass

        return False, 'fail'


    
    def _get_range(self, id):
        for i in range(len(self.ranges)):
            if self.ranges[i][0] <= id < self.ranges[i][1]:
                return i
        return -1
    
    def register(self, name, password):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return False, 'error'

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
  
            return False, 'error'
        
        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        # Check if username already exists
        for node in stor_nodes:
            if node is not None:
                stub = storage_node.make_stub_stor(node[1])
                
                try:
                    res = stub.Ask_if_name_belongs(FeatureS(name=name))
                    if res.b:
                        #raise Exception("Username already exists")
                        return False, 'error'
                except grpc.RpcError as e:
                    return False, 'error'


        stub = storage_node.make_stub_stor(stor_nodes[index][1])
  
        try:
            res = stub.Register_user(User_data(name=name, password=password, value=self.id))
            if res.b:
                self.token = res.token
                return True, res.token
            else:
                return False, 'error'
        except grpc.RpcError as e:
            raise Exception("Fail to create account: {}".format(e.details()))

    def random_n(self, n):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return None, True

        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            file = stub.Random_n(IdvalueS(value=n))
            with open('js', 'wb') as new_file:
                    for data in file:
                        new_file.write(data.data)
            with open('js', 'rb') as jsf:
                js = jsf.read()
                needed_val = load_json_to_database(js, self.storage_node.db_name)
                return needed_val, False
            
        except grpc.RpcError as e:
            
            return None, True

    def followed_tweets(self):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return None, True

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
            return None, True

        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        stub = storage_node.make_stub_stor(stor_nodes[index])
        try:
            ids = stub.Get_following(self.id)
        except grpc.RpcError as e:
            return None, True
        
        
        try:
            file = stub.Followed_tweets(Id_list(values=ids))
            with open('js', 'wb') as new_file:
                    for data in file:
                        new_file.write(data.data)
            with open('js', 'rb') as jsf:
                js = jsf.read()
                needed_val = load_json_to_database(js, self.storage_node.db_name)
                return needed_val, False
            
        except grpc.RpcError as e:
            
            return None, True

    def tweet(self, text):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return None, True

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
            return False

        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        stub = storage_node.make_stub_stor(stor_nodes[index])
        try:
           feat = stub.Tweet(Address(value=self.id, addr= text))
           return True
        except grpc.RpcError as e:
            return False
        
    def retweet(self, id, text,  ret_text_id, ret_id, ret_name):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return None, True

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
            return False

        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        stub = storage_node.make_stub_stor(stor_nodes[index])
        try:
           feat = stub.Retweet(Comment_info(value= id, text=text, tweet_value=ret_text_id, ret_user_value=ret_id, ret_user_name=ret_name))
           return True
        except grpc.RpcError as e:
            return False
        
        
    def retweet(self, id, text,  ret_text_id, ret_id, ret_name):
        # Get closest storage node
        
        stub = chord_node.make_stub_chord(self.c_node.addr)

        try:
            stor_addr = stub.Get_storage(Address(value=0, addr=self.c_node.addr))
        except grpc.RpcError as e:
            return None, True

        # Get all storage addresses
        stub = storage_node.make_stub_stor(stor_addr.addr)
        try:
            stor_nodes = stub.Get_stor_nodes(FeatureS(name="REQ"))
        except grpc.RpcError as e:
            return False

        stor_nodes = storage_node.unpack_posible_nones(stor_nodes.values)
        index = self._get_range(self.id)

        stub = storage_node.make_stub_stor(stor_nodes[index])
        try:
           feat = stub.Comment(Comment_info(value= id, text=text, tweet_value=ret_text_id, ret_user_value=ret_id, ret_user_name=ret_name))
           return True
        except grpc.RpcError as e:
            return False



    
    
    