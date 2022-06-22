from tabnanny import check
import zmq
import hashlib
from utils import requester
from time import time
import threading


class StorageNode:
    def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
        self.addr = addr
        self.port = addr.split(":")[1]
        self.ip = addr.split(":")[0]

        self.chord_addr = addr
        self.client_addr = self.ip + ":{}".format(int(self.port)+1)
        self.port = "{}".format(int(self.port)+2)
        self.addr = self.ip +":"+ self.port
        

        self.index = index
        
        self.vocal_option = vocal_option
        self.id = 0#self.turn_in_hash(self.addr)        
        self.context_sender = zmq.Context()
        self.sock_rep = self.context_sender.socket(zmq.REP)
        self.sock_rep.bind("tcp://" + self.addr)  


        self.total_storage_nodes = K
        if storage_nodes is None:        
            self.storage_nodes = [(self.id, self.addr) for _ in range(self.total_storage_nodes)]
        else: self.storage_nodes = [storage_nodes[i] for i in range(self.total_storage_nodes)]
        

        local_requester = requester(context = self.context_sender, vocal_option = True)
   
        #self.finger_table = [None for i in range(self.m)]
        self.waiting_time = 20
        

        self.commands = {"ALIVE": self.alive, "UPDATE_LIST": self.update_node_list}      
        self.commands_that_need_request = {}
        
        #SEND UPDATED LIST 
        self.update_node_list(local_requester)

        thr_check_succ = threading.Thread(target = self.wrapper_check_on_succ, args =())
        thr_check_succ.start()
        print('started thread')

        thr_check_succ = threading.Thread(target = self.waiting_for_command, args=[local_requester])
        thr_check_succ.start()
        

    


    def waiting_for_command(self, local_requester):
        a = True
        
        while True:
            
            buff = self.sock_rep.recv_json()
            
            if buff['command_name'] in self.commands:
                

                if buff['command_name'] in self.commands_that_need_request:
                    self.commands[buff["command_name"]](**buff["method_params"], sock_req = local_requester)
                else:
                    self.commands[buff["command_name"]](**buff["method_params"])

    

    def wrapper_check_on_succ(self):
        countdown = time()
        local_requester = requester(context = self.context_sender, vocal_option = True)
       
        while True:
            if abs (countdown - time( ) ) > self.waiting_time:
                self.check_on_succ(local_requester)
                countdown = time()


    def check_on_succ(self, local_requester: requester):
        # JUST FOR NOW
        index_check = self.index+1
        if self.index == self.total_storage_nodes -1:
            index_check = 0
        
        if self.storage_nodes[index_check] is not None:
            recv_json = local_requester.make_request(json_to_send = {"command_name" : "ALIVE", "method_params" : {}, "procedence_addr" : self.addr}, destination_id = self.storage_nodes[index_check][0], destination_addr = self.storage_nodes[index_check][1])

            if recv_json == local_requester.error_json:
                self.create_new_storage_node(local_requester)
            else: print("{} is Cool".format(self.storage_nodes[index_check][1]))
            
        else: self.create_new_storage_node(local_requester)
            

    def send_updated_node_list(self, local_requester):

        for node in self.storage_nodes:
            if node is not None:
                recv_json = local_requester.make_request(json_to_send = {"command_name" : "UPDATE_LIST", "method_params" : {"storage_nodes": self.storage_nodes}, "procedence_addr" : self.addr}, destination_id = node[0], destination_addr = node[1])


    def update_node_list(self, storage_nodes):
        self.storage_nodes = [storage_nodes[i] for i in range(self.total_storage_nodes)]
        self.sock_rep.send_json({"response": "ACK", "procedence_addr": self.addr})



    def alive(self):
        self.sock_rep.send_json({"response": "ACK", "procedence_addr": self.addr})
    
    def create_new_storage_node(self, local_requester: requester):
        
        recv_json = local_requester.make_request(json_to_send = {"command_name" : "GET_NON_STORAGE", "method_params" : {}, "procedence_addr" : self.addr}, destination_id = self.id, destination_addr = self.chord_addr)

        if recv_json == local_requester.error_json:
                pass
        elif recv_json["return_info"]["FOUND"]:
            index_check = self.index+1
            if self.index == self.total_storage_nodes -1:
                index_check = 0
                                                                                                    
            recv_json = local_requester.make_request(json_to_send = {"command_name" : "MAKE_STORAGE", "method_params" : {"K": self.total_storage_nodes, "index": index_check, "storage_nodes": self.storage_nodes}, "procedence_addr" : self.addr}, destination_id = self.storage_nodes[index_check][0], destination_addr = self.storage_nodes[index_check][1])
            
            # IF THIS REQUEST FAILS
            if recv_json == local_requester.error_json:
                pass
