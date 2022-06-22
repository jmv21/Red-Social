
from socket import gethostbyname, gethostname
import zmq
import argparse
import re
from chord_node import Node
import threading
from time import time
from utils import requester
from storage_node import StorageNode


class client:
    def __init__(self, ip_port, c_node, storage_node = None):
        self.context = zmq.Context()
        self.sock_req = self.context.socket(zmq.REP)
        self.c_node = c_node
        self.ip_port = c_node.addr
        self._storage = False
        if storage_node is not None: self._storage = True
        self.storage_node = storage_node
        
        
        
        ip, port = self.ip_port.split(":")[0], self.ip_port.split(":")[1]
        port = int(port) + 1
        self.ip = ip
        self.ip_port = ip + ":{}".format(port)

        #if self.ip == '172.17.0.4':
            #self._storage = True
        

        self.sock_req.bind("tcp://" + self.ip_port)   
        self.waiting_time = 20

        self.commands = {"GET_IF_STORAGE": self.is_storage, "MAKE_STORAGE": self.make_storage_node}        
        self.commands_that_need_request = {}


        
        if self.ip == '172.17.0.7': 
            print('started thread')
            thr_stabilize = threading.Thread(target = self.ask_myself, args =())
            thr_stabilize.start()
        self.send_info()
        


    def ask_myself(self):
        countdown = time()
        local_requester = requester(context = self.context, vocal_option = True)
       
        while True:
            if abs (countdown - time( ) ) > self.waiting_time:
                # TEST
                print("request nearest storage node")
                recv_json = local_requester.make_request(json_to_send = {"command_name" : "GET_STORAGE", "method_params" : { "response_addr": self.ip_port, "first_node_addr" : None }, "procedence_addr": self.ip_port}, requester_object= self, asked_properties = None, destination_id = self.c_node.id, destination_addr = self.c_node.addr ) 
                
                if recv_json["return_info"]["FOUND"]:
                    print("storage node is {}".format(recv_json["return_info"]["STORAGE_ADDR"]))
                else: print("STORAGE NOT FOUND")
                countdown = time()
        

    def send_info(self):
        a = True
        local_requester = requester(context = self.context, vocal_option = True)
        while True:
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
            
            buff = self.sock_req.recv_json()
            
            if buff['command_name'] in self.commands:
                

                if buff['command_name'] in self.commands_that_need_request:
                    self.commands[buff["command_name"]](**buff["method_params"], sock_req = local_requester)
                else:
                    self.commands[buff["command_name"]](**buff["method_params"])
            #self.sock_req.disconnect("tcp://"+ buff[0])


    def is_storage(self):
        res = self._storage
        print("ASKED IF STORAGE")
        self.sock_req.send_json({"response": "ACK", "return_info": {"Storage_Node": res}})
    
    #def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
    def make_storage_node(self, K, index, storage_nodes):

        self.storage_node = StorageNode(self.c_node.addr, K, index, storage_nodes)
        self._storage = True





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
    

    n = Node(addr = args.addr_id, node_to_join = args.addr_known, vocal_option = args.v)   
    sn = StorageNode(args.addr_id, 2, True)
    cl = client(None, n, sn)
    
    
    