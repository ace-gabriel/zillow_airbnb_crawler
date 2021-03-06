# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PropertyNoteListResults.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='PropertyNoteListResults.proto',
  package='PropertyNoteListResults',
  syntax='proto2',
  serialized_options=_b('\n\035com.zillow.mobile.webservicesB\027PropertyNoteListResults\242\002\010Protobuf'),
  serialized_pb=_b('\n\x1dPropertyNoteListResults.proto\x12\x17PropertyNoteListResults\",\n\x0cPropertyNote\x12\x0e\n\x06noteId\x18\x01 \x01(\t\x12\x0c\n\x04note\x18\x02 \x01(\t\"\xa0\x01\n\x10PropertyNoteList\x12\x12\n\napiVersion\x18\x01 \x02(\x05\x12\x14\n\x0cresponseCode\x18\x02 \x02(\x05\x12\x17\n\x0fresponseMessage\x18\x03 \x01(\t\x12\x0c\n\x04zpid\x18\x04 \x01(\t\x12;\n\x0cpropertyNote\x18\x05 \x03(\x0b\x32%.PropertyNoteListResults.PropertyNoteBC\n\x1d\x63om.zillow.mobile.webservicesB\x17PropertyNoteListResults\xa2\x02\x08Protobuf')
)




_PROPERTYNOTE = _descriptor.Descriptor(
  name='PropertyNote',
  full_name='PropertyNoteListResults.PropertyNote',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='noteId', full_name='PropertyNoteListResults.PropertyNote.noteId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='note', full_name='PropertyNoteListResults.PropertyNote.note', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=58,
  serialized_end=102,
)


_PROPERTYNOTELIST = _descriptor.Descriptor(
  name='PropertyNoteList',
  full_name='PropertyNoteListResults.PropertyNoteList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='apiVersion', full_name='PropertyNoteListResults.PropertyNoteList.apiVersion', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='responseCode', full_name='PropertyNoteListResults.PropertyNoteList.responseCode', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='responseMessage', full_name='PropertyNoteListResults.PropertyNoteList.responseMessage', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zpid', full_name='PropertyNoteListResults.PropertyNoteList.zpid', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='propertyNote', full_name='PropertyNoteListResults.PropertyNoteList.propertyNote', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=105,
  serialized_end=265,
)

_PROPERTYNOTELIST.fields_by_name['propertyNote'].message_type = _PROPERTYNOTE
DESCRIPTOR.message_types_by_name['PropertyNote'] = _PROPERTYNOTE
DESCRIPTOR.message_types_by_name['PropertyNoteList'] = _PROPERTYNOTELIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PropertyNote = _reflection.GeneratedProtocolMessageType('PropertyNote', (_message.Message,), dict(
  DESCRIPTOR = _PROPERTYNOTE,
  __module__ = 'PropertyNoteListResults_pb2'
  # @@protoc_insertion_point(class_scope:PropertyNoteListResults.PropertyNote)
  ))
_sym_db.RegisterMessage(PropertyNote)

PropertyNoteList = _reflection.GeneratedProtocolMessageType('PropertyNoteList', (_message.Message,), dict(
  DESCRIPTOR = _PROPERTYNOTELIST,
  __module__ = 'PropertyNoteListResults_pb2'
  # @@protoc_insertion_point(class_scope:PropertyNoteListResults.PropertyNoteList)
  ))
_sym_db.RegisterMessage(PropertyNoteList)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
