import multiprocessing
from tabnanny import check
#import zmq
import hashlib
#from utils import requester
from time import time
import threading
from os.path import abspath, exists
from unicodedata import name
from uuid import uuid4
import uuid

from grpc import StatusCode, insecure_channel
import grpc
from gRPC.chord_pb2 import Addr_id, Feature, Storage_make_data, Address, Address_list
from storage_grpc.storage_pb2 import Address_listS, AddressS, Id_list
import storage_grpc.storage_pb2_grpc
from chord_node import make_stub_chord
from concurrent import futures

from storage_grpc.storage_grpc_server import StorageServicer
import DB

def make_stub_stor(addr):
        #with insecure_channel(addr) as channel:
        channel = insecure_channel(addr)
        stub = storage_grpc.storage_pb2_grpc.StorageServicerStub(channel)
        return stub
        
def make_addr_list(addr_list):
    ad_list =[]
    for node in addr_list:
        if node is not None:
            ad_list.append(Address(value=node[0], addr=node[1])) 
            
        else:
            ad_list.append(Address(value=0, addr='0'))
    ad =  Address_list(values=ad_list)
    return ad

def make_addr_listS(addr_list):
    ad_list =[]
    for node in addr_list:
        if node is not None:
            ad_list.append(AddressS(value=node[0], addr=node[1])) 
            
        else:
            ad_list.append(AddressS(value=0, addr='0'))
    ad =  Address_listS(values=ad_list)
    return ad

def unpack_posible_nones(storage_nodes):
    node_list = []
    for i in range(len(storage_nodes)):
            if storage_nodes[i].addr == '0' and storage_nodes[i].value == 0:
                node_list.append(None)
            else:    
                node_list.append((storage_nodes[i].value, storage_nodes[i].addr))
    return node_list

def define_ranges(K, max, min):
    amount_per_range = int(max/K)
    current_min = min
    ranges_list = []
    for _ in range(K-1):
        ranges_list.append((current_min, current_min+amount_per_range))
        current_min = current_min+amount_per_range
    ranges_list.append((current_min, max))

    return ranges_list

class StorageNode:
    def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
        #print("hi")
        # define domain ranges
        self.max_id = pow(2, 63) -1
        self.ranges_list = define_ranges(K, self.max_id, 0)
        self.index = index
        # main databases and backups databases paths
        self.db_name = 'DB{}'.format(self.index)
        self.db_path = None
        # BU1 is predecessor backup
        self.b1_name = 'BU1'
        self.b1_path = None
        # BU2 is successor backup
        self.b2_name = 'BU2'
        self.b2_path = None

        # chord and self ip addresses and ports
        self.addr = addr
        self.port = addr.split(":")[1]
        self.ip = addr.split(":")[0]

        self.chord_addr = addr
        #self.client_addr = self.ip + ":{}".format(int(self.port)+1)
        self.port = "{}".format(int(self.port)+2)
        self.addr = self.ip +":"+ self.port
        


        
        self.vocal_option = vocal_option
        self.id = 0   
        

        self._first_K = False
        self.total_storage_nodes = K
        # If this is the first storage node
        if storage_nodes is None:
            self.storage_nodes = [None for _ in range(self.total_storage_nodes)]
            self.storage_nodes[self.index] = (self.id, self.addr)
            # NAME + INDEX     ID
            self._first_K = True
            
        else: 
            self.storage_nodes = unpack_posible_nones(storage_nodes)
            self._first_K = None in self.storage_nodes
                
            self.storage_nodes[self.index] = (self.id, self.addr)
            self.send_updated_node_list()
            # THEN ASK FOR STORAGE NODES
        
        if self._first_K and not exists(self.db_name):
            DB.create_db(name=self.db_name, initial_id=self.ranges_list[self.index][0])
            self.db_path = abspath(self.db_name)
        
        
        self.waiting_time = 20

        
        

        self.thr_check_succ = threading.Thread(target = self.wrapper_check_on_succ, args =())
        self.thr_check_succ.start()


        self.thr_wait_for_command = threading.Thread(target = self.waiting_for_command, args=())
        self.thr_wait_for_command.start()
     
        self.check_on_databases()
        self.thr_check_db = threading.Thread(target = self.check_on_databases, args=())
        self.thr_check_db.start()

    


    def waiting_for_command(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        storage_grpc.storage_pb2_grpc.add_StorageServicerServicer_to_server(
            StorageServicer(self), server)
        server.add_insecure_port('[::]:{}'.format(self.port))
        server.start()
        server.wait_for_termination()

    def check_on_databases(self):
        countdown = time()
        waiting_time = 10
        jobs = 3
        while True:
            if abs (countdown - time() ) > waiting_time:
                if (self.db_path is None or not exists(self.db_path)) and not self._first_K:
                    if self.ask_for_db_file():
                        jobs -= 1
                #print(self.b1_path is None)
                if self.b1_path is None or not exists(self.b1_path):
                    if self.ask_for_first_backup():
                        jobs -= 1
                if self.b2_path is None or not exists(self.b2_path):
                    if self.ask_for_second_backup():
                        jobs -= 1
                if jobs <= 0:
                    break
                countdown = time()

    def wrapper_check_on_succ(self):
        countdown = time()
        #local_requester = requester(context = self.context_sender, vocal_option = True)
       
        while True:
            if abs (countdown - time( ) ) > self.waiting_time:
                #SEND UPDATED LIST 
                self.check_on_succ()
                
                countdown = time()

    

    def check_on_succ(self):
        # JUST FOR NOW
        index_check = self.index+1
        if self.index == self.total_storage_nodes -1:
            index_check = 0
        
        if self.storage_nodes[index_check] is not None:
            #print("check for succ")
            stub = make_stub_stor(self.storage_nodes[index_check][1])

            try:
                resp = stub.Alive(Feature(name="REQ"))
            except grpc.RpcError as e:
                if e.code() == StatusCode.UNAVAILABLE:
                    self.create_new_storage_node()


            
        else:
            self.create_new_storage_node()
            

    def send_updated_node_list(self):
        for node in self.storage_nodes:
            if node is not None:
                if self.addr != node[1]:
                    #recv_json = local_requester.make_request(json_to_send = {"command_name" : "UPDATE_LIST", "method_params" : {"storage_nodes": self.storage_nodes}, "procedence_addr" : self.addr}, destination_id = node[0], destination_addr = node[1])
                    stub = make_stub_stor(node[1])
                    try:
                        resp = stub.Update_list(make_addr_listS(self.storage_nodes))
                    except grpc.RpcError as e:
                        return

    def update_node_list(self, storage_nodes):
        self.storage_nodes = [storage_nodes[i] for i in range(len(storage_nodes))]
  
    def alive(self):
        pass
    
    def create_new_storage_node(self):
        
        #recv_json = local_requester.make_request(json_to_send = {"command_name" : "GET_NON_STORAGE", "method_params" : {"response_addr": self.addr, "first_node_addr": None}, "procedence_addr" : self.addr}, destination_id = self.id, destination_addr = self.chord_addr)
        stub = make_stub_chord(self.chord_addr)
        
        try:
            stor = stub.Get_non_storage(Address(value= self.id,addr=self.chord_addr))
            
        except grpc.RpcError as e:
            return

        if stor.found:
            
            index_check = self.index+1
            if self.index == self.total_storage_nodes -1:
                index_check = 0

            #destination_addr = recv_json["return_info"]["STORAGE_ADDR"]
            destination_addr = stor.addr                                                               
            #recv_json = local_requester.make_request(json_to_send = {"command_name" : "MAKE_STORAGE", "method_params" : {"K": self.total_storage_nodes, "index": index_check, "storage_nodes": self.storage_nodes}, "procedence_addr" : self.addr}, destination_id = self.id, destination_addr = destination_addr)
            
            stub = make_stub_chord(destination_addr)
            
            try:
                
                #st_md = Storage_make_data(K=self.total_storage_nodes, index=index_check, nodes=make_addr_list(self.storage_nodes))
                
                ad_list = make_addr_list(self.storage_nodes)
                resp = stub.Make_storage(Storage_make_data(K=self.total_storage_nodes,index=index_check,nodes=ad_list))
            except grpc.RpcContext as e:
                return

        if stor.error:
            try:
                stor = stub.Remove_storage(Feature(name="REQ"))
            except grpc.RpcError as e:
                return

    def parse_to_json(self, name):
        return DB.export_databse_to_json(name)


    #def print_file(self, name):
    #    print("printing created file")
    #    with open(name, 'rb') as file:
    #        print(file.read())
        #DB.test()

    def ask_for_db_file(self):
        index_check = self.index-1
        if self.index == 0:
            index_check = self.total_storage_nodes -1

        if self.storage_nodes[index_check] is not None:
            stub = make_stub_stor(self.storage_nodes[index_check][1])
            try:
                file = stub.Ask_for_file(Feature(name='DB{}'.format(index_check)))
                with open('DB{}'.format(self.index), 'wb') as new_file:
                    for data in file:
                        new_file.write(data.data)
                self.db_path = abspath('DB{}'.format(self.index))
                return True
            except grpc.RpcError as e:
                return False
        return False

                    

    def ask_for_first_backup(self):
        index_check = self.index-1
        if self.index == 0:
            index_check = self.total_storage_nodes -1

        if self.storage_nodes[index_check] is not None:
            stub = make_stub_stor(self.storage_nodes[index_check][1])
            try:
                file = stub.Ask_for_file(Feature(name='DB{}'.format(index_check)))
                with open('BU1'.format(self.index), 'wb') as new_file:
                    for data in file:
                        new_file.write(data.data)
                self.b1_path = abspath('BU1')
                return True
            except grpc.RpcError as e:
                return False
        return False

    def ask_for_second_backup(self):
        index_check = self.index+1
        if self.index == self.total_storage_nodes -1:
            index_check = 0

        if self.storage_nodes[index_check] is not None:
            stub = make_stub_stor(self.storage_nodes[index_check][1])
            try:
                file = stub.Ask_for_file(Feature(name='DB{}'.format(index_check)))
                with open('BU2'.format(self.index), 'wb') as new_file:
                    for data in file:
                        new_file.write(data.data)
                #self.print_file('BU2')
                self.b2_path = abspath('BU2')
                return True
            except grpc.RpcError as e:
                return False
        return False
    
    def contains(self, id):
        
        return self.ranges_list[self.index][0] <= id < self.ranges_list[self.index][1]

    def name_exist(self, name):
        res = DB.user_exist_name(name, self.db_name)
        return res
    
    def register(self, name, password, id):
       
        res = DB.execute_order([0, name, password, id, self.db_name])
        
        return res
    
    def login(self, name, password, id):
        res = DB.execute_order([1, name, password, self.db_name])#, id])
        return res

    def random_n(self,n):
        tweets = DB.execute_order([5, n, self.db_name])
        json= DB.export_models_to_json(tweets)
        json_bytes = json_bytes.encode("utf-8")
        return json_bytes
    
    def get_following(self, id):
        friends = DB.get_friends(id, self.db_name)
        return Id_list(values=friends)

    def followed_tweets(self, ids):
        tweets = DB.execute_order([4, ids, self.db_name])
        json= DB.export_models_to_json(tweets)
        json_bytes = json_bytes.encode("utf-8")
        return json_bytes

    def tweet(self, text, id):
        DB.execute_order([2, id, text,-1, -1,'', self.db_name, -1])
        return
    
    def retweet(self, id, text,  ret_text_id, ret_id, ret_name):
        DB.execute_order([2, id, text, ret_text_id, ret_id, ret_name, self.db_name, -1])
        return

    def comment(self, id, text,   ret_text_id, ret_id, ret_name):
        DB.execute_order([7, id, text,-1, ret_id, ret_name, self.db_name, ret_text_id])
        return