# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chord.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x63hord.proto\x12\nrouteguide\"\x17\n\x07\x46\x65\x61ture\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x18\n\x07Idvalue\x12\r\n\x05value\x18\x01 \x01(\x03\"&\n\x07\x41\x64\x64ress\x12\r\n\x05value\x18\x01 \x01(\x03\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\"3\n\x0c\x41\x64\x64ress_list\x12#\n\x06values\x18\x01 \x03(\x0b\x32\x13.routeguide.Address\"I\n\x07Storage\x12\x0c\n\x04\x61\x64\x64r\x18\x01 \x01(\t\x12\x12\n\nis_storage\x18\x02 \x01(\x08\x12\r\n\x05\x66ound\x18\x03 \x01(\x08\x12\r\n\x05\x65rror\x18\x04 \x01(\x08\"V\n\x11Storage_make_data\x12\t\n\x01K\x18\x01 \x01(\x05\x12\r\n\x05index\x18\x02 \x01(\x05\x12\'\n\x05nodes\x18\x03 \x01(\x0b\x32\x18.routeguide.Address_list\"&\n\x07\x41\x64\x64r_id\x12\r\n\x05value\x18\x01 \x01(\t\x12\x0c\n\x04\x61\x64\x64r\x18\x02 \x01(\t\"b\n\x0cRouteSummary\x12\x13\n\x0bpoint_count\x18\x01 \x01(\x05\x12\x15\n\rfeature_count\x18\x02 \x01(\x05\x12\x10\n\x08\x64istance\x18\x03 \x01(\x05\x12\x14\n\x0c\x65lapsed_time\x18\x04 \x01(\x05\x32\x98\x06\n\nRouteGuide\x12\x33\n\x05\x41live\x12\x13.routeguide.Feature\x1a\x13.routeguide.Feature\"\x00\x12\x32\n\x04Join\x12\x13.routeguide.Feature\x1a\x13.routeguide.Feature\"\x00\x12\x37\n\tFind_succ\x12\x13.routeguide.Idvalue\x1a\x13.routeguide.Address\"\x00\x12\x37\n\tFind_pred\x12\x13.routeguide.Idvalue\x1a\x13.routeguide.Address\"\x00\x12@\n\rGet_succ_list\x12\x13.routeguide.Feature\x1a\x18.routeguide.Address_list\"\x00\x12?\n\x11\x43losest_pred_fing\x12\x13.routeguide.Idvalue\x1a\x13.routeguide.Address\"\x00\x12\x36\n\x08Get_pred\x12\x13.routeguide.Feature\x1a\x13.routeguide.Address\"\x00\x12\x35\n\x07Rectify\x12\x13.routeguide.Address\x1a\x13.routeguide.Feature\"\x00\x12\x39\n\x0bGet_storage\x12\x13.routeguide.Address\x1a\x13.routeguide.Storage\"\x00\x12=\n\x0fGet_non_storage\x12\x13.routeguide.Address\x1a\x13.routeguide.Storage\"\x00\x12\x44\n\x0cMake_storage\x12\x1d.routeguide.Storage_make_data\x1a\x13.routeguide.Feature\"\x00\x12<\n\x0eRemove_storage\x12\x13.routeguide.Feature\x1a\x13.routeguide.Feature\"\x00\x12?\n\x11Get_storage_by_id\x12\x13.routeguide.Addr_id\x1a\x13.routeguide.Address\"\x00\x42\x36\n\x1bio.grpc.examples.routeguideB\x0fRouteGuideProtoP\x01\xa2\x02\x03RTGb\x06proto3')



_FEATURE = DESCRIPTOR.message_types_by_name['Feature']
_IDVALUE = DESCRIPTOR.message_types_by_name['Idvalue']
_ADDRESS = DESCRIPTOR.message_types_by_name['Address']
_ADDRESS_LIST = DESCRIPTOR.message_types_by_name['Address_list']
_STORAGE = DESCRIPTOR.message_types_by_name['Storage']
_STORAGE_MAKE_DATA = DESCRIPTOR.message_types_by_name['Storage_make_data']
_ADDR_ID = DESCRIPTOR.message_types_by_name['Addr_id']
_ROUTESUMMARY = DESCRIPTOR.message_types_by_name['RouteSummary']
Feature = _reflection.GeneratedProtocolMessageType('Feature', (_message.Message,), {
  'DESCRIPTOR' : _FEATURE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Feature)
  })
_sym_db.RegisterMessage(Feature)

Idvalue = _reflection.GeneratedProtocolMessageType('Idvalue', (_message.Message,), {
  'DESCRIPTOR' : _IDVALUE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Idvalue)
  })
_sym_db.RegisterMessage(Idvalue)

Address = _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Address)
  })
_sym_db.RegisterMessage(Address)

Address_list = _reflection.GeneratedProtocolMessageType('Address_list', (_message.Message,), {
  'DESCRIPTOR' : _ADDRESS_LIST,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Address_list)
  })
_sym_db.RegisterMessage(Address_list)

Storage = _reflection.GeneratedProtocolMessageType('Storage', (_message.Message,), {
  'DESCRIPTOR' : _STORAGE,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Storage)
  })
_sym_db.RegisterMessage(Storage)

Storage_make_data = _reflection.GeneratedProtocolMessageType('Storage_make_data', (_message.Message,), {
  'DESCRIPTOR' : _STORAGE_MAKE_DATA,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Storage_make_data)
  })
_sym_db.RegisterMessage(Storage_make_data)

Addr_id = _reflection.GeneratedProtocolMessageType('Addr_id', (_message.Message,), {
  'DESCRIPTOR' : _ADDR_ID,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.Addr_id)
  })
_sym_db.RegisterMessage(Addr_id)

RouteSummary = _reflection.GeneratedProtocolMessageType('RouteSummary', (_message.Message,), {
  'DESCRIPTOR' : _ROUTESUMMARY,
  '__module__' : 'chord_pb2'
  # @@protoc_insertion_point(class_scope:routeguide.RouteSummary)
  })
_sym_db.RegisterMessage(RouteSummary)

_ROUTEGUIDE = DESCRIPTOR.services_by_name['RouteGuide']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\033io.grpc.examples.routeguideB\017RouteGuideProtoP\001\242\002\003RTG'
  _FEATURE._serialized_start=27
  _FEATURE._serialized_end=50
  _IDVALUE._serialized_start=52
  _IDVALUE._serialized_end=76
  _ADDRESS._serialized_start=78
  _ADDRESS._serialized_end=116
  _ADDRESS_LIST._serialized_start=118
  _ADDRESS_LIST._serialized_end=169
  _STORAGE._serialized_start=171
  _STORAGE._serialized_end=244
  _STORAGE_MAKE_DATA._serialized_start=246
  _STORAGE_MAKE_DATA._serialized_end=332
  _ADDR_ID._serialized_start=334
  _ADDR_ID._serialized_end=372
  _ROUTESUMMARY._serialized_start=374
  _ROUTESUMMARY._serialized_end=472
  _ROUTEGUIDE._serialized_start=475
  _ROUTEGUIDE._serialized_end=1267
# @@protoc_insertion_point(module_scope)
