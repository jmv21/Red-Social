import multiprocessing
from tabnanny import check
#import zmq
import hashlib
#from utils import requester
from time import time
import threading

from grpc import StatusCode, insecure_channel
import grpc
from gRPC.chord_pb2 import Feature, Storage_make_data, Address, Address_list
from storage_grpc.storage_pb2 import Address_listS, AddressS
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
    print("unp")
    for i in range(len(storage_nodes)):
            if storage_nodes[i].addr == '0' and storage_nodes[i].value == 0:
                node_list.append(None)
            else:    
                node_list.append((storage_nodes[i].value, storage_nodes[i].addr))
    return node_list


class StorageNode:
    def __init__(self, addr, K, index, storage_nodes = None, vocal_option = False):
        db = DB.create_db()
        print("did create db")
        self.addr = addr
        self.port = addr.split(":")[1]
        self.ip = addr.split(":")[0]

        self.chord_addr = addr
        self.client_addr = self.ip + ":{}".format(int(self.port)+1)
        self.port = "{}".format(int(self.port)+2)
        self.addr = self.ip +":"+ self.port
        

        self.index = index
        
        self.vocal_option = vocal_option
        self.id = 0   
        #self.context_sender = zmq.Context()
        #self.sock_rep = self.context_sender.socket(zmq.REP)
        #self.sock_rep.bind("tcp://" + self.addr)  


        self.total_storage_nodes = K
        if storage_nodes is None:        
            self.storage_nodes = [None for _ in range(self.total_storage_nodes)]
            self.storage_nodes[self.index] = (self.id, self.addr)
        else: 
            self.storage_nodes = unpack_posible_nones(storage_nodes)
            self.storage_nodes[self.index] = (self.id, self.addr)
            self.send_updated_node_list()
        

        #local_requester = requester(context = self.context_sender, vocal_option = True)
        
        self.waiting_time = 30
        

        self.commands = {"ALIVE": self.alive, "UPDATE_LIST": self.update_node_list}      
        self.commands_that_need_request = {}
        
        

        self.thr_check_succ = threading.Thread(target = self.wrapper_check_on_succ, args =())
        self.thr_check_succ.start()
        #thr_check_succ = multiprocessing.Process(target = self.wrapper_check_on_succ, args =())
        #thr_check_succ.start()
        print('started thread')

        self.thr_wait_for_command = threading.Thread(target = self.waiting_for_command, args=())
        self.thr_wait_for_command.start()
        #self.thr_wait_for_command = multiprocessing.Process( target=self.waiting_for_command, args =())
        #self.thr_wait_for_command.start()
        #self.waiting_for_command()
        


    


    def waiting_for_command(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        storage_grpc.storage_pb2_grpc.add_StorageServicerServicer_to_server(
            StorageServicer(self), server)
        server.add_insecure_port('[::]:{}'.format(self.port))
        server.start()
        print("started server")
        server.wait_for_termination()

    

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
            print("check for succ")
            #recv_json = local_requester.make_request(json_to_send = {"command_name" : "ALIVE", "method_params" : {}, "procedence_addr" : self.addr}, destination_id = self.storage_nodes[index_check][0], destination_addr = self.storage_nodes[index_check][1])
            stub = make_stub_stor(self.storage_nodes[index_check][1])

            try:
                resp = stub.Alive(Feature(name="REQ"))
            except grpc.RpcError as e:
                if e.code() == StatusCode.UNAVAILABLE:
                    print("make new node")
                    self.create_new_storage_node()

            else: 
                print("{} is Cool".format(self.storage_nodes[index_check][1]))
                try:
                    file = stub.Ask_for_file(Feature(name="REQ"))
                    #print("now printing file")
                    #for data in file:
                        #print(data.data)
                    #print(file.data)
                    with open('DB2', 'wb') as new_file:
                        bytelist = []
                        for data in file:
                        #print(data.data)
                            bytelist.append(data.data)
                            new_file.write(data.data)
                        #json_str = ''.join(bytelist)#.decode('utf-8')
                        #print("json_string")
                        #print(json_str)
                        self.print_file()
                    
                    #DB.load_json_to_database()
                    #DB.db_connect('DB2')
                except grpc.RpcError as e:
                    print("fail to ask for file")
                    print(e.code())
                    print(e.details())
            
        else:
            print("request creation") 
            self.create_new_storage_node()
            

    def send_updated_node_list(self):
        print("sendind updated list")
        for node in self.storage_nodes:
            if node is not None:
                if self.addr != node[1]:
                    #recv_json = local_requester.make_request(json_to_send = {"command_name" : "UPDATE_LIST", "method_params" : {"storage_nodes": self.storage_nodes}, "procedence_addr" : self.addr}, destination_id = node[0], destination_addr = node[1])
                    stub = make_stub_stor(node[1])
                    try:
                        resp = stub.Update_list(make_addr_listS(self.storage_nodes))
                    except grpc.RpcError as e:
                        print("fail to send update")
                        print(e.code())
                        print(e.details())


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
            print("4")
            print(e.code())
            print(e.details())
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
                print("res")
            except grpc.RpcContext as e:
                print("8")
                print(e.code())
                print(e.details())
        
        if stor.error:
            try:
                stor = stub.Remove_storage(Feature(name="REQ"))
                print("9")
            except grpc.RpcError as e:
                print("10")
                print(e.code())
                print(e.details())
                return

    def parse_to_json(self, name):
        return DB.export_databse_to_json(name)


    def print_file(self):
        print("printing created file")
        with open('DB2', 'rb') as file:
            print(file.read())
        DB.test()
