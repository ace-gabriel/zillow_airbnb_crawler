# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: HomeInfoPropertyNotification.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='HomeInfoPropertyNotification.proto',
  package='HomeInfoPropertyNotification',
  syntax='proto2',
  serialized_options=_b('\n*com.zillow.mobile.webservices.notificationB\034HomeInfoPropertyNotification\242\002\010Protobuf'),
  serialized_pb=_b('\n\"HomeInfoPropertyNotification.proto\x12\x1cHomeInfoPropertyNotification\"A\n\x14HomeInfoNotification\x12\x1b\n\x13\x63hangeStatusDisplay\x18\x01 \x01(\t\x12\x0c\n\x04read\x18\x02 \x01(\x08\x42U\n*com.zillow.mobile.webservices.notificationB\x1cHomeInfoPropertyNotification\xa2\x02\x08Protobuf')
)




_HOMEINFONOTIFICATION = _descriptor.Descriptor(
  name='HomeInfoNotification',
  full_name='HomeInfoPropertyNotification.HomeInfoNotification',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='changeStatusDisplay', full_name='HomeInfoPropertyNotification.HomeInfoNotification.changeStatusDisplay', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='read', full_name='HomeInfoPropertyNotification.HomeInfoNotification.read', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=133,
)

DESCRIPTOR.message_types_by_name['HomeInfoNotification'] = _HOMEINFONOTIFICATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HomeInfoNotification = _reflection.GeneratedProtocolMessageType('HomeInfoNotification', (_message.Message,), dict(
  DESCRIPTOR = _HOMEINFONOTIFICATION,
  __module__ = 'HomeInfoPropertyNotification_pb2'
  # @@protoc_insertion_point(class_scope:HomeInfoPropertyNotification.HomeInfoNotification)
  ))
_sym_db.RegisterMessage(HomeInfoNotification)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)