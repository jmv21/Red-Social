
from ast import arg
import ctypes
from socket import gethostbyname, gethostname
#import zmq
import argparse
import re
import chord_node
import threading
from time import time
import storage_node
import multiprocessing

import netaddr
import uuid






class Client:
    def __init__(self, ip_port, c_node, storage = None):
        #self.context = zmq.Context()
        #self.sock_req = self.context.socket(zmq.REP)
        print("hi bro")
        self.c_node = c_node
        self.c_node.bind_client(self)



        self.ip_port = c_node.addr
        self._storage = False
        if storage is not None: self._storage = True
        self.storage_node = storage

        K = 3
        if ip_port == '172.17.0.2:8080':
            print('first addr stor')
            self._storage = True
            self.storage_node = storage_node.StorageNode(ip_port, K, 0, storage_nodes=None, vocal_option=True)
            

        if storage is not None:
            print("I am first storage")
        
        
        
        ip, port = self.ip_port.split(":")[0], self.ip_port.split(":")[1]
        port = int(port) + 1
        self.ip = ip
        self.ip_port = ip + ":{}".format(port)
        

        #self.sock_req.bind("tcp://" + self.ip_port)   
        self.waiting_time = 20


        self.commands = {"GET_IF_STORAGE": self.is_storage, "MAKE_STORAGE": self.make_storage_node}        
        self.commands_that_need_request = {}


        
        #if self.ip == '172.17.0.2': 
            #print('started thread')
            #thr_stabilize = threading.Thread(target = self.ask_myself, args =())
            #thr_stabilize.start()
        
        #self.c_node.bind_client(self)

        self.send_info()
        
    
    


    def ask_myself(self):
        countdown = time()
        #local_requester = requester(context = self.context, vocal_option = True)
       
        #while True:
            #if abs (countdown - time( ) ) > self.waiting_time:
                # TEST
                #print("request nearest storage node")
                #recv_json = local_requester.make_request(json_to_send = {"command_name" : "GET_STORAGE", "method_params" : { "response_addr": self.ip_port, "first_node_addr" : None }, "procedence_addr": self.ip_port}, requester_object= self, asked_properties = None, destination_id = self.c_node.id, destination_addr = self.c_node.addr ) 
                
                #if recv_json["return_info"]["FOUND"]:
                    #print("storage node is {}".format(recv_json["return_info"]["STORAGE_ADDR"]))
                #else: print("STORAGE NOT FOUND")
                #countdown = time()
        

    def send_info(self):
        a = True
        #local_requester = requester(context = self.context, vocal_option = True)
        #while True:
            #buff = input().split()
            
            #params = {buff[i] : buff[i + 1] for i in range(2, len(buff), 2) }
            
            #if "BELONG" in buff:
                #params['interval'] = params['interval'].split(',')
                #params['interval'] = ( int ( params['interval'][0][1:]), int(params['interval'][1][:-1] ) )
                #params['id'] = int(params['id'])
                
            #if "FIND_SUCC" in buff:
                #params['id'] = int(params["id"])
                

            #self.sock_req.send_json({"command_name": buff[1], "method_params": params , "procedence_addr": "127.0.0.1:5050"})
            
            #print(info)
        if a:
            print("my ip {}".format(self.ip_port.split(":")[0]))
            print("my port {}".format(self.ip_port.split(":")[1]))
            a = False
            

            #buff = self.sock_req.recv_json()
            
            #if buff['command_name'] in self.commands:
                
                #print("received json")
                #if buff['command_name'] in self.commands_that_need_request:
                    #print("I made request {}".format(buff['command_name']))
                    #self.commands[buff["command_name"]](**buff["method_params"], sock_req = local_requester)
                #else:
                    #self.commands[buff["command_name"]](**buff["method_params"])
            

            #self.sock_req.disconnect("tcp://"+ buff[0])


    def is_storage(self):
        return self._storage
    
    def make_storage_wrapper(self, K, index, storage_nodes):
        #thr_make_stor = threading.Thread(target = self.make_storage_node, args =[K, index, storage_nodes])
        #thr_make_stor.start()
        #thr_make_stor = multiprocessing.Process( target=self.make_storage_node, args =[K, index, storage_nodes])
        #thr_make_stor.start()
        return

    #def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
    def make_storage_node(self, K, index, storage_nodes):
        
        print("NOW I AM STORAGE")
        self.storage_node = storage_node.StorageNode(self.c_node.addr, K, index, storage_nodes)
        self._storage = True

    def remove_storage(self):
        print("removing storage")

        #Thread = self.storage_node.thr_wait_for_command
        self._stop_threads([self.storage_node.thr_wait_for_command, self.storage_node.thr_check_succ])
        #self.storage_node.thr_wait_for_command.terminate()
        #self.storage_node = None
        #self._storage = False

        self._stop_threads([self.storage_node.thr_wait_for_command, self.storage_node.thr_check_succ])
        
    def storage_contains(self, id):
        print("6")
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
        
        print("successful")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--addr_id', default = gethostbyname(gethostname()) + ":8080", help= "This is the address of the node that identifies it in the hash space.\nIf no address is set, this automatically set the local address asigned from the local network.")
    parser.add_argument('--addr_known', default = None, help = "This is an IP address that identifies reference a node in the network.\nIf you wanna join new nodes to an existing network, you have to enter this value, otherwise your node never bee connected to the network.")
    
    parser.add_argument('--v', action = "store_false", help = "This is the vocal option. You can see the activity of the node if you enter it.")
    
    matcher = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}")
    args = parser.parse_args()
    error_message = "The %s must have an IP:port like format first, and after that, because the code uses this info for the hash function, if you want\n to avoide colisions, you must enter an unique string. This %s is a bad input"
    if not matcher.fullmatch(args.addr_id.split()[0]) :
        parser.error(error_message %("addr_id", args.addr_id))
    if args.addr_known and not matcher.fullmatch(args.addr_known.split()[0]):
        parser.error(error_message %("addr_known", args.addr_known))
    



    n = chord_node.Node(addr = args.addr_id, node_to_join = args.addr_known, vocal_option = args.v)

    if args.addr_id == '172.17.0.2:8080':
        print('first addr stor')
        sn = storage_node.StorageNode(args.addr_id, 2, 0, storage_nodes=None, vocal_option=True)
    else: sn = None
    #sn = None
    
    cl = Client(None, n, storage_node=sn)

    #if args.addr_id == '172.17.0.2:8080':
        #print('first addr stor')
        #sn = storage_node.StorageNode(args.addr_id, 2, 0, storage_nodes=None, vocal_option=True)
    #else: sn = None
    #sn = None
    
    cl = Client(args.addr_id, n, None)


    
    
