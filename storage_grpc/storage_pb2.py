# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: storage.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstorage.proto\x12\nrouteguide\"\x18\n\x08\x46\x65\x61tureS\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x19\n\x08IdvalueS\x12\r\n\x05value\x18\x01 \x01(\x03\"\'\n\x08\x41\x64\x64ressS\x12\r\n\x05value\x18\x01 \x01(\x03\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\"5\n\rAddress_listS\x12$\n\x06values\x18\x01 \x03(\x0b\x32\x14.routeguide.AddressS\";\n\x08StorageS\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\t\x12\x12\n\nis_storage\x18\x02 \x01(\x08\x12\r\n\x05\x66ound\x18\x03 \x01(\x08\"\x15\n\x05\x44\x61taS\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x11\n\x04\x42ool\x12\t\n\x01\x62\x18\x01 \x01(\x08\":\n\tUser_data\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x03\"4\n\tLog_token\x12\t\n\x01\x62\x18\x01 \x01(\x08\x12\r\n\x05token\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x03\"\x19\n\x07Id_list\x12\x0e\n\x06values\x18\x01 \x01(\x03\"f\n\x0cRetweet_info\x12\x12\n\nuser_value\x18\x01 \x01(\x03\x12\x13\n\x0btweet_value\x18\x02 \x01(\x03\x12\x16\n\x0eret_user_value\x18\x03 \x01(\x03\x12\x15\n\rret_user_name\x18\x04 \x01(\t\"t\n\x0c\x43omment_info\x12\x12\n\nuser_value\x18\x01 \x01(\x03\x12\x13\n\x0btweet_value\x18\x02 \x01(\x03\x12\x16\n\x0eret_user_value\x18\x03 \x01(\x03\x12\x15\n\rret_user_name\x18\x04 \x01(\t\x12\x0c\n\x04text\x18\x05 \x01(\t\"7\n\x0b\x46ollow_info\x12\x12\n\nuser_value\x18\x01 \x01(\x03\x12\x14\n\x0c\x66ollow_value\x18\x02 \x01(\x03\x32\xee\x06\n\x0fStorageServicer\x12\x35\n\x05\x41live\x12\x14.routeguide.FeatureS\x1a\x14.routeguide.FeatureS\"\x00\x12@\n\x0bUpdate_list\x12\x19.routeguide.Address_listS\x1a\x14.routeguide.FeatureS\"\x00\x12\x43\n\x0eGet_stor_nodes\x12\x14.routeguide.FeatureS\x1a\x19.routeguide.Address_listS\"\x00\x12;\n\x0c\x41sk_for_file\x12\x14.routeguide.FeatureS\x1a\x11.routeguide.DataS\"\x00\x30\x01\x12?\n\x13\x41sk_if_name_belongs\x12\x14.routeguide.FeatureS\x1a\x10.routeguide.Bool\"\x00\x12?\n\rRegister_user\x12\x15.routeguide.User_data\x1a\x15.routeguide.Log_token\"\x00\x12<\n\nLogin_user\x12\x15.routeguide.User_data\x1a\x15.routeguide.Log_token\"\x00\x12\x37\n\x08Random_n\x12\x14.routeguide.IdvalueS\x1a\x11.routeguide.DataS\"\x00\x30\x01\x12<\n\rGet_following\x12\x14.routeguide.IdvalueS\x1a\x13.routeguide.Id_list\"\x00\x12=\n\x0f\x46ollowed_tweets\x12\x13.routeguide.Id_list\x1a\x11.routeguide.DataS\"\x00\x30\x01\x12\x35\n\x05Tweet\x12\x14.routeguide.AddressS\x1a\x14.routeguide.FeatureS\"\x00\x12;\n\x07Retweet\x12\x18.routeguide.Comment_info\x1a\x14.routeguide.FeatureS\"\x00\x12\x39\n\x06\x46ollow\x12\x17.routeguide.Follow_info\x1a\x14.routeguide.FeatureS\"\x00\x12;\n\x07\x43omment\x12\x18.routeguide.Comment_info\x1a\x14.routeguide.FeatureS\"\x00\x42\x36\n\x1bio.grpc.examples.routeguideB\x0fRouteGuideProtoP\x01\xa2\x02\x03RTGb\x06proto3')



_FEATURES = DESCRIPTOR.message_types_by_name['FeatureS']
_IDVALUES = DESCRIPTOR.message_types_by_name['IdvalueS']
_ADDRESSS = DESCRIPTOR.message_types_by_name['AddressS']
_ADDRESS_LISTS = DESCRIPTOR.message_types_by_name['Address_listS']
_STORAGES = DESCRIPTOR.message_types_by_name['StorageS']
_DATAS = DESCRIPTOR.message_types_by_name['DataS']
_BOOL = DESCRIPTOR.message_types_by_name['Bool']
_USER_DATA = DESCRIPTOR.message_types_by_name['User_data']
_LOG_TOKEN = DESCRIPTOR.message_types_by_name['Log_token']
_ID_LIST = DESCRIPTOR.message_types_by_name['Id_list']
_RETWEET_INFO = DESCRIPTOR.message_types_by_name['Retweet_info']
_COMMENT_INFO = DESCRIPTOR.message_types_by_name['Comment_info']
_FOLLOW_INFO = DESCRIPTOR.message_types_by_name['Follow_info']
FeatureS = _reflection.GeneratedProtocolMessageType('FeatureS', (_message.Message,), {
  'DESCRIPTOR' : _FEATURES,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.FeatureS)
  })
_sym_db.RegisterMessage(FeatureS)

IdvalueS = _reflection.GeneratedProtocolMessageType('IdvalueS', (_message.Message,), {
  'DESCRIPTOR' : _IDVALUES,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.IdvalueS)
  })
_sym_db.RegisterMessage(IdvalueS)

AddressS = _reflection.GeneratedProtocolMessageType('AddressS', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESSS,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.AddressS)
  })
_sym_db.RegisterMessage(AddressS)

Address_listS = _reflection.GeneratedProtocolMessageType('Address_listS', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS_LISTS,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Address_listS)
  })
_sym_db.RegisterMessage(Address_listS)

StorageS = _reflection.GeneratedProtocolMessageType('StorageS', (_message.Message,), {
  'DESCRIPTOR' : _STORAGES,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.StorageS)
  })
_sym_db.RegisterMessage(StorageS)

DataS = _reflection.GeneratedProtocolMessageType('DataS', (_message.Message,), {
  'DESCRIPTOR' : _DATAS,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.DataS)
  })
_sym_db.RegisterMessage(DataS)

Bool = _reflection.GeneratedProtocolMessageType('Bool', (_message.Message,), {
  'DESCRIPTOR' : _BOOL,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Bool)
  })
_sym_db.RegisterMessage(Bool)

User_data = _reflection.GeneratedProtocolMessageType('User_data', (_message.Message,), {
  'DESCRIPTOR' : _USER_DATA,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.User_data)
  })
_sym_db.RegisterMessage(User_data)

Log_token = _reflection.GeneratedProtocolMessageType('Log_token', (_message.Message,), {
  'DESCRIPTOR' : _LOG_TOKEN,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Log_token)
  })
_sym_db.RegisterMessage(Log_token)

Id_list = _reflection.GeneratedProtocolMessageType('Id_list', (_message.Message,), {
  'DESCRIPTOR' : _ID_LIST,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Id_list)
  })
_sym_db.RegisterMessage(Id_list)

Retweet_info = _reflection.GeneratedProtocolMessageType('Retweet_info', (_message.Message,), {
  'DESCRIPTOR' : _RETWEET_INFO,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Retweet_info)
  })
_sym_db.RegisterMessage(Retweet_info)

Comment_info = _reflection.GeneratedProtocolMessageType('Comment_info', (_message.Message,), {
  'DESCRIPTOR' : _COMMENT_INFO,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Comment_info)
  })
_sym_db.RegisterMessage(Comment_info)

Follow_info = _reflection.GeneratedProtocolMessageType('Follow_info', (_message.Message,), {
  'DESCRIPTOR' : _FOLLOW_INFO,
  '__module__' : 'storage_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Follow_info)
  })
_sym_db.RegisterMessage(Follow_info)

_STORAGESERVICER = DESCRIPTOR.services_by_name['StorageServicer']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033io.grpc.examples.routeguideB\017RouteGuideProtoP\001\242\002\003RTG'
  _FEATURES._serialized_start=29
  _FEATURES._serialized_end=53
  _IDVALUES._serialized_start=55
  _IDVALUES._serialized_end=80
  _ADDRESSS._serialized_start=82
  _ADDRESSS._serialized_end=121
  _ADDRESS_LISTS._serialized_start=123
  _ADDRESS_LISTS._serialized_end=176
  _STORAGES._serialized_start=178
  _STORAGES._serialized_end=237
  _DATAS._serialized_start=239
  _DATAS._serialized_end=260
  _BOOL._serialized_start=262
  _BOOL._serialized_end=279
  _USER_DATA._serialized_start=281
  _USER_DATA._serialized_end=339
  _LOG_TOKEN._serialized_start=341
  _LOG_TOKEN._serialized_end=393
  _ID_LIST._serialized_start=395
  _ID_LIST._serialized_end=420
  _RETWEET_INFO._serialized_start=422
  _RETWEET_INFO._serialized_end=524
  _COMMENT_INFO._serialized_start=526
  _COMMENT_INFO._serialized_end=642
  _FOLLOW_INFO._serialized_start=644
  _FOLLOW_INFO._serialized_end=699
  _STORAGESERVICER._serialized_start=702
  _STORAGESERVICER._serialized_end=1580
# @@protoc_insertion_point(module_scope)
