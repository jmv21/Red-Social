import sys
from typing import Mapping
import zmq
from time import time
import threading
import hashlib
from utils import requester, bcolors
from random import Random
from functools import reduce
from socket import gethostbyname, gethostname


#Each node represents an active index in the ring.
#each node, knows its succesor.
# IMPLEMENT: predeccesor
class Node:
    def __init__(self, addr, node_to_join = None, vocal_option = False):
        self.addr = addr
        self.port = addr.split(":")[1]
        self.domain_addr = lambda value : reduce((lambda x,y : x + y), [x for x in value.split(":")[0].split(".") + [value.split(":")[1] ] ]) 
        self.turn_in_hash = lambda input_to_id : int(hashlib.sha1(bytes(self.domain_addr(input_to_id), 'utf-8') ).hexdigest(), 16 )
        self.vocal_option = vocal_option
        self.id = self.turn_in_hash(self.addr)        
        self.context_sender = zmq.Context()
        self.m = 64
        self.length_succ_list = 3        
        self.succ_list = [(self.id, self.addr) for i in range(self.length_succ_list)]
        self.start = lambda i : (self.id + 2**(i)) % 2**self.m
        self.finger_table = [None for i in range(self.m)]
        self.waiting_time = 10

        self.commands = {"JOIN": self.join_reply, "FIND_SUCC": self.find_successor_wrapper, "FIND_PRED" : self.find_predecessor_wrapper, "GET_SUCC_LIST": self.get_succ_list, "CLOSEST_PRED_FING": self.closest_pred_fing_wrap, "ALIVE": self.alive, "GET_PARAMS": self.get_params, "GET_PROP": self.get_prop, "GET_PRED": self.get_pred, "STAB": self.stabilize, "RECT": self.rectify, "GET_STORAGE": self.closest_storage_node, "GET_NON_STORAGE": self.closest_non_storage_node }        
        self.commands_that_need_request = {"RECT", "FIND_SUCC", "FIND_PRED", "CLOSEST_PRED_FING", "STAB", "GET_STORAGE"}

        #if self.vocal_option: print("Started node ", (self.id, self.addr))
        print("Started node ", (self.id, self.addr))

        # initialize this node messages manager
        client_requester = requester(context = self.context_sender, vocal_option = self.vocal_option)

        # if node_to_join is not None then this node is joining and existing chord structure
        if node_to_join:
            node_to_join_id = self.turn_in_hash(node_to_join)
            recieved_json = client_requester.make_request(json_to_send = {"command_name" : "JOIN", "method_params" : {}, "procedence_addr" : self.addr},destination_id = node_to_join_id, destination_addr = node_to_join)
            
            # if the requested join does not receive feedback from the json sended
            # then ask the user to provide an address and retry
            while recieved_json is client_requester.error_json:                
                client_requester.action_for_error(node_to_join)
                print("Enter address to retry ")
                node_to_join = input()
                node_to_join_id = self.turn_in_hash(self.domain_addr(node_to_join))            
                print("Connecting to ", (node_to_join, node_to_join_id))
                
                recieved_json = client_requester.make_request(json_to_send = {"command_name" : "JOIN", "method_params" : {}, "procedence_addr" : self.addr}, destination_id = node_to_join_id, destination_addr = node_to_join)
            
            # if the JOIN operation fails
            # then ask the user to provide an address and retry
            while not self.execute_join(node_to_join, node_to_join_id, self.start(0), client_requester):
                client_requester.action_for_error(node_to_join)
                print("Enter address to retry ")
                node_to_join = input()
                node_to_join_id = self.turn_in_hash(self.domain_addr(node_to_join))
                print("Connecting now to ", (node_to_join_id, node_to_join))                
                recieved_json = client_requester.make_request(json_to_send = {"command_name" : "JOIN", "method_params" : {}, "procedence_addr" : self.addr}, destination_id = node_to_join_id, destination_addr = node_to_join)
                        
        else:
            # if node_to_join is None then this is an initial node of the chord structure
            self.predecessor_addr, self.predecessor_id = self.addr, self.id
            
            self.isPrincipal = True

        self.wrapper_actions(client_requester)


    #In this method the nodes bind its address for possible connections, and recieve messages.
    def waiting_for_command(self, client_requester):
        
        # Bind a socket to this context
        self.sock_rep = self.context_sender.socket(zmq.REP)
        self.sock_rep.bind("tcp://" + self.addr)    
                
        while True:
            if self.vocal_option:
                print("waiting")
            
            buff = self.sock_rep.recv_json()

            if buff['command_name'] in self.commands:
                
                if self.vocal_option:
                    print(buff)
                if buff['command_name'] in self.commands_that_need_request:
                    self.commands[buff["command_name"]](**buff["method_params"], sock_req = client_requester)
                else:
                    self.commands[buff["command_name"]](**buff["method_params"])
                
            # Testing
            #print(self.succ_list)

        #self.sock_rep.close()       

    # COMMANDS METHODS:

    # Acknowledge JOIN request
    def join_reply(self):        
        self.sock_rep.send_json({"response": "ACK", "return_info": {}})

    #Acknowledge GET_PARAMS request        
    def get_params(self):        
        self.sock_rep.send_json({"response": "ACK", "return_info": {"finger_table" : self.finger_table, "predecessor_addr" : self.predecessor_addr, "predecessor_id" : self.predecessor_id, "succ_list" : self.succ_list, "id": self.id, "address": self.addr } })

    # Acknowledge GET_PROP request
    def get_prop(self, prop_name):
        if prop_name == "start_indexes":
            self.sock_rep.send_json({'response': "ACK", "return_info" : [self.start(i) for i in range(self.m)] })    

        self.sock_rep.send_json({'response': 'ACK', "return_info": self.__dict__[prop_name] })

    # Acknowledge GET_PRED request
    def get_pred(self):
        self.sock_rep.send_json({"response": "ACK", "return_info": {"predecessor_id" : self.predecessor_id, "predecessor_addr" : self.predecessor_addr } } )


    def alive(self):
        self.sock_rep.send_json({"response": "ACK", "procedence_addr": self.addr})

    def get_succ_list(self):
        
        self.sock_rep.send_json( {"response": "ACK", "return_info": {"succ_list" : self.succ_list} } )

    #The execute_join function introduce this node in the Chord ring 
    #finds the predecessor of the self.id and assigns it to self.predecessor value.
    def execute_join(self, node_to_join, node_to_join_id, id_to_found_pred, sock_req):

        # Make a request to find predecessor of node_to_join
        recv_json = sock_req.make_request(json_to_send = {"command_name" : "FIND_PRED", "method_params" : {"id" : id_to_found_pred}, "procedence_addr" : self.addr}, requester_object = self, method_for_wrap = "find_predecesor", destination_id = node_to_join_id, destination_addr = node_to_join)
        if recv_json is sock_req.error_json:
            return False
        
        self.predecessor_id, self.predecessor_addr = recv_json['return_info']['pred_id'], recv_json['return_info']['pred_addr']        
        recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_SUCC_LIST", "method_params" : {}, "procedence_addr" : self.addr}, requester_object = self, asked_properties = ("succ_list",), destination_id = recv_json['return_info']['pred_id'], destination_addr = recv_json['return_info']['pred_addr'] )         
        
        if recv_json is sock_req.error_json:
            return False
        self.succ_list = recv_json['return_info']['succ_list']
        
        
        return True


    #The stabilize step ask to the successor of the node (self), for its predecessor.
    #If the predecessor_id of the successor is between self.id and successor.id
    #then this node has a new successor: the predecessor of its successor. 
    #Then this node needs to actualize its successor list.
    def stabilize(self, socket_req : requester):
                                       
        #If the succesor query fails, then we pop the unnavailable succesor, and 
        #return. It is important to know that if the length of the succ_list
        #is and we have k succesive fails in the Chord, we can't expect a good
        #working of the network.  
        recv_json_pred = socket_req.make_request(json_to_send = {"command_name" : "GET_PRED", "method_params" : {}, "procedence_addr" : self.addr, "procedence_method": "stabilize_95"}, requester_object = self, asked_properties = ('predecessor_id', 'predecessor_addr'), destination_id = self.succ_list[0][0], destination_addr = self.succ_list[0][1])
        if recv_json_pred is socket_req.error_json:
            if self.vocal_option:
                socket_req.action_for_error(self.succ_list[0][1])
            self.succ_list.pop(0)
            self.succ_list += [(self.id, self.addr)]                                    
            return

        recv_json_succ_list = socket_req.make_request(json_to_send = {'command_name' : "GET_SUCC_LIST", 'method_params' : {}, 'procedence_addr' : self.addr, "procedence_method": "stabilize_104"}, requester_object = self, asked_properties = ("succ_list",), destination_id = self.succ_list[0][0], destination_addr = self.succ_list[0][1])
        if recv_json_succ_list is socket_req.error_json: return 
        
        self.succ_list = [self.succ_list[0]] + recv_json_succ_list['return_info']["succ_list"][:-1]
                    
        if self.between(recv_json_pred['return_info']['predecessor_id'], interval = (self.id, self.succ_list[0][0]) ):
            
            recv_json_pred_succ_list = socket_req.make_request( json_to_send = {"command_name" : "GET_SUCC_LIST", "method_params" : {}, "procedence_addr" : self.addr, "procedence_method":  "stabilize_109"}, requester_object = self, asked_properties = ('succ_list',), destination_id = recv_json_pred['return_info'][ 'predecessor_id'], destination_addr = recv_json_pred['return_info'][ 'predecessor_addr'])
            if not recv_json_pred_succ_list is socket_req.error_json:
                
                #If it's true that self has a new succesor and this new succesor is alive, then self has to actualize its succ_list    
                self.succ_list = [[recv_json_pred['return_info']['predecessor_id'], recv_json_pred['return_info']['predecessor_addr']]] + recv_json_pred_succ_list['return_info']['succ_list'][:-1]                                       
            else:
                self.vocal_option: socket_req.action_for_error(recv_json_pred['return_info'][ 'predecessor_addr'])
    

    def between(self, id, interval):
        if interval[0] < interval[1]:
            return id > interval[0] and id < interval[1] 
        return id > interval[0] or id < interval[1]

    
    # Rectify Step   
    def rectify(self, predecessor_id, predecessor_addr, sock_req):
        
        # if this node's id is between self.predecessor_id and predecessor_id
        # and self.predeccesor_id == self.id
        # then change this node predecessor to the new one
        if self.between(predecessor_id, interval = (self.predecessor_id, self.id)) or self.id == self.predecessor_id:
            
            if self.predecessor_id == self.id: 

                self.succ_list[0] = (predecessor_id, predecessor_addr)                
            self.predecessor_id, self.predecessor_addr = predecessor_id, predecessor_addr

        else:

            # Check is self.predecessor is available            
            recv_json_alive = sock_req.make_request(json_to_send = {"command_name" : "ALIVE", "method_params" : {}, "procedence_addr" : self.addr, "procedence_method": "rectify"}, destination_id = self.predecessor_id, destination_addr = self.predecessor_addr)
            
            if recv_json_alive is sock_req.error_json:
                if self.vocal_option: sock_req.action_for_error(self.predecessor_addr)   
                self.predecessor_id, self.predecessor_addr = predecessor_id, predecessor_addr             
                sock_req.action_for_error(self.predecessor_addr)
        
        self.sock_rep.send_json( { "response": "ACK" } )
        

    
    def wrapper_actions(self, client_requester):
        
        thr_stabilize = threading.Thread(target = self.wrapper_loop_stabilize, args =() )
        thr_stabilize.start()
        thr_waiting_for_command = threading.Thread(target= self.waiting_for_command, args=[client_requester])        
        thr_waiting_for_command.start()

    def wrapper_loop_stabilize(self):
        countdown = time()
        rand = Random()
        rand.seed()
        local_requester = requester(context = self.context_sender, vocal_option = self.vocal_option)
        choices = [i for i in range(self.m)]
        while True:
            if abs (countdown - time( ) ) > self.waiting_time:
                if self.predecessor_id != self.id:
                	#Periodically, the node stabilize its information about the network,
                	#and actuallize a finger table, that is an optmizitation for found succesors.
                    self.stabilize(socket_req = local_requester)
                    #Independetly of the result of the stabilize, the node sends a notify message to its succesor, asking for a rectification of the predecessor values.
                    if local_requester.make_request(json_to_send = {"command_name" : "RECT", "method_params" : { "predecessor_id": self.id, "predecessor_addr" : self.addr }, "procedence_addr" : self.addr, "procedence_method": "wrapper_loop_stabilize", "time": time()}, destination_id = self.succ_list[0][0], destination_addr = self.succ_list[0][1]) is local_requester.error_json and self.vocal_option:
                        local_requester.action_for_error(self.succ_list[0][1])

                    index = rand.choice( choices )                    
                    self.finger_table[ index ] = self.find_successor(self.start(index), sock_req = local_requester)    
                    

                countdown = time()
        



    # Sends the response to FIND_SUCC
    def find_successor_wrapper(self, id, sock_req):
            info = self.find_successor(id, sock_req)
            self.sock_rep.send_json({"response": "ACK", "return_info": info})
            pass


    def find_successor(self, id, sock_req):
        # First look for the predecessor
        tuple_info = self.find_predecessor(id, sock_req)
        if tuple_info:
            destination_id, destination_addr = tuple_info
            # Wait for the response of GET_SUCC_LIST request            
            recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_SUCC_LIST", "method_params": {}, "procedence_addr": self.addr, "procedence_method": "find_succesor_286"}, requester_object= self, asked_properties = ('succ_list', ), destination_id = destination_id, destination_addr = destination_addr ) 
            if recv_json is sock_req.error_json: return None
            # Return the succ_list
            return recv_json['return_info']['succ_list'][0]
        return None
            
    # Sends the response to FIND_PRED
    def find_predecessor_wrapper(self, id, sock_req):
        pred_id, pred_addr = self.find_predecessor(id, sock_req)

        self.sock_rep.send_json({"response": "ACK", "return_info": {"pred_id": pred_id, "pred_addr": pred_addr}, "procedence_addr": self.addr } )
        

       
    def find_predecessor(self, id, sock_req):
        # Fist find the current successor
        current_id = self.id
        current_succ_id, current_succ_addr = self.succ_list[0]
        self.finger_table[0] = self.succ_list[0]
        current_addr = self.addr  
        
         
        while not self.between(id, interval = (current_id, current_succ_id)) and current_succ_id != id :            
            
            recv_json_closest = sock_req.make_request(json_to_send = {"command_name" : "CLOSEST_PRED_FING", "method_params" : {"id": id}, "procedence_addr" : self.addr, "procedence_method": "find_predecessor"}, method_for_wrap = 'closest_pred_fing', requester_object = self, destination_id = current_id, destination_addr = current_addr)
            
            if recv_json_closest is sock_req.error_json : return None
            
            
            recv_json_succ = sock_req.make_request(json_to_send = {"command_name" : "GET_SUCC_LIST", "method_params" : {}, "procedence_addr" : self.addr, "procedence_method" : "find_predecessor" }, requester_object = self, asked_properties = ("succ_list", ), destination_id = recv_json_closest['return_info'][0], destination_addr = recv_json_closest['return_info'][1] )

            if recv_json_succ is sock_req.error_json:
                return None
            
                
            current_id, current_addr = recv_json_closest['return_info'][0], recv_json_closest['return_info'][1]
            current_succ_id, current_succ_addr = recv_json_succ['return_info']['succ_list'][0]                
        
        return current_id, current_addr

    def closest_pred_fing_wrap (self, id, sock_req):        
        closest_id, closest_addr = self.closest_pred_fing(id, sock_req)
        self.sock_rep.send_json({"response" : "ACK", "return_info" : (closest_id, closest_addr), "procedence": self.addr})
        

    def closest_pred_fing(self, id, sock_req):
        #In here is where we use the finger_table as an optimization of the search of the succesor of an id.
        for i in range(self.m-1, -1, -1):            
            if self.finger_table[i] is None : continue 
            if self.between(self.finger_table[i][0], (self.id, id) ) :
                return self.finger_table[i]
                
                
        return (self.id, self.addr)
    
    #def find_successor(self, id, sock_req):
        # First look for the predecessor
    #    tuple_info = self.find_predecessor(id, sock_req)
    #    if tuple_info:
    #        destination_id, destination_addr = tuple_info
            # Wait for the response of GET_SUCC_LIST request            
    #        recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_SUCC_LIST", "method_params": {}, "procedence_addr": self.addr, "procedence_method": "find_succesor_286"}, requester_object= self, asked_properties = ('succ_list', ), destination_id = destination_id, destination_addr = destination_addr ) 
    #        if recv_json is sock_req.error_json: return None
            # Return the succ_list
    #        return recv_json['return_info']['succ_list'][0]
    #    return None

    #def closest_storage_node(self):#, #id, #sock_req):
    #    #TESTING
    #    ip, port = self.addr.split(":")[0], self.addr.split(":")[1]
    #    port = int(port) + 1
    #    destination_addr = ip + ":{}".format(port)
    #    local_requester = requester(context = self.context_sender, vocal_option = self.vocal_option)
        
    #    recv_json = local_requester.make_request(json_to_send = {"command_name" : "GET_IF_STORAGE", "method_params": {}, "procedence_addr": self.addr}, requester_object= self, asked_properties = ('succ_list', ), destination_id = self.id, destination_addr = destination_addr ) 
    #    if recv_json is local_requester.error_json:
    #        print("error")
    #    print(recv_json["return_info"])
    
    # Params:
    # response_addr: the address of the node that requested the info
    # first_node: the first asked node
    def closest_storage_node(self, response_addr, first_node_addr, sock_req):
        ip, port = self.addr.split(":")[0], self.addr.split(":")[1]
        port = int(port) + 1
        destination_addr = ip + ":{}".format(port)

        
        # TEST
        print("ask my node if storage")
        recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_IF_STORAGE", "method_params": {}, "procedence_addr": self.addr}, requester_object= self, asked_properties = None, destination_id = self.id, destination_addr = destination_addr ) 



        if recv_json["return_info"]["Storage_Node"]:
            # TEST
            print("respond")
            #socket_req = self.context_sender.socket(zmq.REP)
            #socket_req.connect("tcp://" + response_addr)  
            
            
            self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND": True}, "procedence": self.addr})
            #socket_req.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"]}, "procedence": self.addr})
            
            
            
            #sock_req.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"]}, "procedence": self.addr})
        else:
            if first_node_addr is None: first_node_addr = self.addr

            if first_node_addr == self.succ_list[0][1]:
                self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": None, "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND": False}, "procedence": self.addr})
                return

            # TEST
            print("ask next node if storage")
            recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_STORAGE", "method_params" : { "response_addr": response_addr, "first_node_addr" : first_node_addr }, "procedence_addr": self.addr}, requester_object= self, asked_properties = None, destination_id = self.succ_list[0][0], destination_addr = self.succ_list[0][1] ) 
            if recv_json != sock_req.error_json:
                self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": recv_json["return_info"]["STORAGE_ADDR"], "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND":recv_json["return_info"]["FOUND"]}, "procedence": self.addr})


    def closest_non_storage_node(self, response_addr, first_node_addr, sock_req):
        ip, port = self.addr.split(":")[0], self.addr.split(":")[1]
        port = int(port) + 1
        destination_addr = ip + ":{}".format(port)

        
        # TEST
        print("ask my node if storage")
        recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_IF_STORAGE", "method_params": {}, "procedence_addr": self.addr}, requester_object= self, asked_properties = None, destination_id = self.id, destination_addr = destination_addr ) 



        if not recv_json["return_info"]["Storage_Node"]:
            # TEST
            print("respond")
            #socket_req = self.context_sender.socket(zmq.REP)
            #socket_req.connect("tcp://" + response_addr)  
            
            
            self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND": True}, "procedence": self.addr})
            #socket_req.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"]}, "procedence": self.addr})
            
            
            
            #sock_req.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": destination_addr, "Storage_Node": recv_json["return_info"]["Storage_Node"]}, "procedence": self.addr})
        else:
            if first_node_addr is None: first_node_addr = self.addr

            if first_node_addr == self.succ_list[0][1]:
                self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": None, "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND": False}, "procedence": self.addr})
                return

            # TEST
            print("ask next node if storage")
            recv_json = sock_req.make_request(json_to_send = {"command_name" : "GET_STORAGE", "method_params" : { "response_addr": response_addr, "first_node_addr" : first_node_addr }, "procedence_addr": self.addr}, requester_object= self, asked_properties = None, destination_id = self.succ_list[0][0], destination_addr = self.succ_list[0][1] ) 
            if recv_json != sock_req.error_json:
                self.sock_rep.send_json({"response" : "ACK", "return_info" : {"STORAGE_ADDR": recv_json["return_info"]["STORAGE_ADDR"], "Storage_Node": recv_json["return_info"]["Storage_Node"], "FOUND":recv_json["return_info"]["FOUND"]}, "procedence": self.addr})

    
    




