# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: SchoolInfo.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='SchoolInfo.proto',
  package='Schools',
  syntax='proto2',
  serialized_options=_b('\n\035com.zillow.mobile.webservicesB\007Schools\242\002\010Protobuf'),
  serialized_pb=_b('\n\x10SchoolInfo.proto\x12\x07Schools\"\xa0\x02\n\nSchoolInfo\x12\x11\n\tregion_id\x18\x01 \x01(\x05\x12\x1c\n\x14students_per_teacher\x18\x02 \x01(\x05\x12\x0e\n\x06grades\x18\x03 \x01(\t\x12\x0c\n\x04link\x18\x04 \x01(\t\x12\x0c\n\x04size\x18\x05 \x01(\x05\x12\x0c\n\x04name\x18\x06 \x01(\t\x12#\n\x05level\x18\x07 \x03(\x0e\x32\x14.Schools.SchoolLevel\x12\x10\n\x08latitude\x18\x08 \x01(\x01\x12\x11\n\tlongitude\x18\t \x01(\x01\x12\x11\n\tgs_rating\x18\n \x01(\x05\x12!\n\x04type\x18\x0b \x01(\x0e\x32\x13.Schools.SchoolType\x12\x11\n\tschool_id\x18\x0c \x01(\x05\x12\x14\n\x0c\x66ragment_ids\x18\r \x03(\x05\"h\n\x13SchoolSearchResults\x12$\n\x07schools\x18\x01 \x03(\x0b\x32\x13.Schools.SchoolInfo\x12\x14\n\x0c\x66ragment_ids\x18\x02 \x03(\x05\x12\x15\n\rtotal_schools\x18\x03 \x01(\x05*2\n\nSchoolType\x12\n\n\x06PUBLIC\x10\x00\x12\x0b\n\x07PRIVATE\x10\x01\x12\x0b\n\x07\x43HARTER\x10\x02*3\n\x0bSchoolLevel\x12\x0e\n\nELEMENTARY\x10\x00\x12\n\n\x06MIDDLE\x10\x01\x12\x08\n\x04HIGH\x10\x02\x42\x33\n\x1d\x63om.zillow.mobile.webservicesB\x07Schools\xa2\x02\x08Protobuf')
)

_SCHOOLTYPE = _descriptor.EnumDescriptor(
  name='SchoolType',
  full_name='Schools.SchoolType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PUBLIC', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PRIVATE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHARTER', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=426,
  serialized_end=476,
)
_sym_db.RegisterEnumDescriptor(_SCHOOLTYPE)

SchoolType = enum_type_wrapper.EnumTypeWrapper(_SCHOOLTYPE)
_SCHOOLLEVEL = _descriptor.EnumDescriptor(
  name='SchoolLevel',
  full_name='Schools.SchoolLevel',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ELEMENTARY', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MIDDLE', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='HIGH', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=478,
  serialized_end=529,
)
_sym_db.RegisterEnumDescriptor(_SCHOOLLEVEL)

SchoolLevel = enum_type_wrapper.EnumTypeWrapper(_SCHOOLLEVEL)
PUBLIC = 0
PRIVATE = 1
CHARTER = 2
ELEMENTARY = 0
MIDDLE = 1
HIGH = 2



_SCHOOLINFO = _descriptor.Descriptor(
  name='SchoolInfo',
  full_name='Schools.SchoolInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='region_id', full_name='Schools.SchoolInfo.region_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='students_per_teacher', full_name='Schools.SchoolInfo.students_per_teacher', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='grades', full_name='Schools.SchoolInfo.grades', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='link', full_name='Schools.SchoolInfo.link', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='size', full_name='Schools.SchoolInfo.size', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='Schools.SchoolInfo.name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='level', full_name='Schools.SchoolInfo.level', index=6,
      number=7, type=14, cpp_type=8, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='Schools.SchoolInfo.latitude', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='Schools.SchoolInfo.longitude', index=8,
      number=9, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gs_rating', full_name='Schools.SchoolInfo.gs_rating', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='Schools.SchoolInfo.type', index=10,
      number=11, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='school_id', full_name='Schools.SchoolInfo.school_id', index=11,
      number=12, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fragment_ids', full_name='Schools.SchoolInfo.fragment_ids', index=12,
      number=13, type=5, cpp_type=1, label=3,
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
  serialized_start=30,
  serialized_end=318,
)


_SCHOOLSEARCHRESULTS = _descriptor.Descriptor(
  name='SchoolSearchResults',
  full_name='Schools.SchoolSearchResults',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='schools', full_name='Schools.SchoolSearchResults.schools', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fragment_ids', full_name='Schools.SchoolSearchResults.fragment_ids', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_schools', full_name='Schools.SchoolSearchResults.total_schools', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=320,
  serialized_end=424,
)

_SCHOOLINFO.fields_by_name['level'].enum_type = _SCHOOLLEVEL
_SCHOOLINFO.fields_by_name['type'].enum_type = _SCHOOLTYPE
_SCHOOLSEARCHRESULTS.fields_by_name['schools'].message_type = _SCHOOLINFO
DESCRIPTOR.message_types_by_name['SchoolInfo'] = _SCHOOLINFO
DESCRIPTOR.message_types_by_name['SchoolSearchResults'] = _SCHOOLSEARCHRESULTS
DESCRIPTOR.enum_types_by_name['SchoolType'] = _SCHOOLTYPE
DESCRIPTOR.enum_types_by_name['SchoolLevel'] = _SCHOOLLEVEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SchoolInfo = _reflection.GeneratedProtocolMessageType('SchoolInfo', (_message.Message,), dict(
  DESCRIPTOR = _SCHOOLINFO,
  __module__ = 'SchoolInfo_pb2'
  # @@protoc_insertion_point(class_scope:Schools.SchoolInfo)
  ))
_sym_db.RegisterMessage(SchoolInfo)

SchoolSearchResults = _reflection.GeneratedProtocolMessageType('SchoolSearchResults', (_message.Message,), dict(
  DESCRIPTOR = _SCHOOLSEARCHRESULTS,
  __module__ = 'SchoolInfo_pb2'
  # @@protoc_insertion_point(class_scope:Schools.SchoolSearchResults)
  ))
_sym_db.RegisterMessage(SchoolSearchResults)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
