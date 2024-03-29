# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: status.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import action_pb2 as action__pb2
import err_pb2 as err__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='status.proto',
  package='status',
  syntax='proto3',
  serialized_options=_b('\n\031com.supremainc.sdk.statusP\001Z\026biostar/service/status'),
  serialized_pb=_b('\n\x0cstatus.proto\x12\x06status\x1a\x0c\x61\x63tion.proto\x1a\terr.proto\"j\n\tLEDStatus\x12*\n\x0c\x64\x65viceStatus\x18\x01 \x01(\x0e\x32\x14.status.DeviceStatus\x12\r\n\x05\x63ount\x18\x02 \x01(\r\x12\"\n\x07signals\x18\x03 \x03(\x0b\x32\x11.action.LEDSignal\"p\n\x0c\x42uzzerStatus\x12*\n\x0c\x64\x65viceStatus\x18\x01 \x01(\x0e\x32\x14.status.DeviceStatus\x12\r\n\x05\x63ount\x18\x02 \x01(\r\x12%\n\x07signals\x18\x03 \x03(\x0b\x32\x14.action.BuzzerSignal\"^\n\x0cStatusConfig\x12#\n\x08LEDState\x18\x01 \x03(\x0b\x32\x11.status.LEDStatus\x12)\n\x0b\x42uzzerState\x18\x02 \x03(\x0b\x32\x14.status.BuzzerStatus\"$\n\x10GetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\"9\n\x11GetConfigResponse\x12$\n\x06\x63onfig\x18\x01 \x01(\x0b\x32\x14.status.StatusConfig\"J\n\x10SetConfigRequest\x12\x10\n\x08\x64\x65viceID\x18\x01 \x01(\r\x12$\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x14.status.StatusConfig\"\x13\n\x11SetConfigResponse\"P\n\x15SetConfigMultiRequest\x12\x11\n\tdeviceIDs\x18\x01 \x03(\r\x12$\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x14.status.StatusConfig\"B\n\x16SetConfigMultiResponse\x12(\n\x0c\x64\x65viceErrors\x18\x01 \x03(\x0b\x32\x12.err.ErrorResponse*\xce\x03\n\x0c\x44\x65viceStatus\x12\x18\n\x14\x44\x45VICE_STATUS_NORMAL\x10\x00\x12\x18\n\x14\x44\x45VICE_STATUS_LOCKED\x10\x01\x12\x1b\n\x17\x44\x45VICE_STATUS_RTC_ERROR\x10\x02\x12\x1f\n\x1b\x44\x45VICE_STATUS_WAITING_INPUT\x10\x03\x12\x1e\n\x1a\x44\x45VICE_STATUS_WAITING_DHCP\x10\x04\x12\x1d\n\x19\x44\x45VICE_STATUS_SCAN_FINGER\x10\x05\x12\x1b\n\x17\x44\x45VICE_STATUS_SCAN_CARD\x10\x06\x12\x19\n\x15\x44\x45VICE_STATUS_SUCCESS\x10\x07\x12\x16\n\x12\x44\x45VICE_STATUS_FAIL\x10\x08\x12\x18\n\x14\x44\x45VICE_STATUS_DURESS\x10\t\x12%\n!DEVICE_STATUS_PROCESS_CONFIG_CARD\x10\n\x12%\n!DEVICE_STATUS_SUCCESS_CONFIG_CARD\x10\x0b\x12\x1b\n\x17\x44\x45VICE_STATUS_SCAN_FACE\x10\x0c\x12\x1b\n\x17\x44\x45VICE_STATUS_RESERVED3\x10\r\x12\x1b\n\x17\x44\x45VICE_STATUS_RESERVED4\x10\x0e\x32\xdd\x01\n\x06Status\x12@\n\tGetConfig\x12\x18.status.GetConfigRequest\x1a\x19.status.GetConfigResponse\x12@\n\tSetConfig\x12\x18.status.SetConfigRequest\x1a\x19.status.SetConfigResponse\x12O\n\x0eSetConfigMulti\x12\x1d.status.SetConfigMultiRequest\x1a\x1e.status.SetConfigMultiResponseB5\n\x19\x63om.supremainc.sdk.statusP\x01Z\x16\x62iostar/service/statusb\x06proto3')
  ,
  dependencies=[action__pb2.DESCRIPTOR,err__pb2.DESCRIPTOR,])

_DEVICESTATUS = _descriptor.EnumDescriptor(
  name='DeviceStatus',
  full_name='status.DeviceStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_NORMAL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_LOCKED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_RTC_ERROR', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_WAITING_INPUT', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_WAITING_DHCP', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_SCAN_FINGER', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_SCAN_CARD', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_SUCCESS', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_FAIL', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_DURESS', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_PROCESS_CONFIG_CARD', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_SUCCESS_CONFIG_CARD', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_SCAN_FACE', index=12, number=12,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_RESERVED3', index=13, number=13,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DEVICE_STATUS_RESERVED4', index=14, number=14,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=712,
  serialized_end=1174,
)
_sym_db.RegisterEnumDescriptor(_DEVICESTATUS)

DeviceStatus = enum_type_wrapper.EnumTypeWrapper(_DEVICESTATUS)
DEVICE_STATUS_NORMAL = 0
DEVICE_STATUS_LOCKED = 1
DEVICE_STATUS_RTC_ERROR = 2
DEVICE_STATUS_WAITING_INPUT = 3
DEVICE_STATUS_WAITING_DHCP = 4
DEVICE_STATUS_SCAN_FINGER = 5
DEVICE_STATUS_SCAN_CARD = 6
DEVICE_STATUS_SUCCESS = 7
DEVICE_STATUS_FAIL = 8
DEVICE_STATUS_DURESS = 9
DEVICE_STATUS_PROCESS_CONFIG_CARD = 10
DEVICE_STATUS_SUCCESS_CONFIG_CARD = 11
DEVICE_STATUS_SCAN_FACE = 12
DEVICE_STATUS_RESERVED3 = 13
DEVICE_STATUS_RESERVED4 = 14



_LEDSTATUS = _descriptor.Descriptor(
  name='LEDStatus',
  full_name='status.LEDStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceStatus', full_name='status.LEDStatus.deviceStatus', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='status.LEDStatus.count', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signals', full_name='status.LEDStatus.signals', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=155,
)


_BUZZERSTATUS = _descriptor.Descriptor(
  name='BuzzerStatus',
  full_name='status.BuzzerStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceStatus', full_name='status.BuzzerStatus.deviceStatus', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='count', full_name='status.BuzzerStatus.count', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='signals', full_name='status.BuzzerStatus.signals', index=2,
      number=3, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=157,
  serialized_end=269,
)


_STATUSCONFIG = _descriptor.Descriptor(
  name='StatusConfig',
  full_name='status.StatusConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='LEDState', full_name='status.StatusConfig.LEDState', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='BuzzerState', full_name='status.StatusConfig.BuzzerState', index=1,
      number=2, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=271,
  serialized_end=365,
)


_GETCONFIGREQUEST = _descriptor.Descriptor(
  name='GetConfigRequest',
  full_name='status.GetConfigRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='status.GetConfigRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=367,
  serialized_end=403,
)


_GETCONFIGRESPONSE = _descriptor.Descriptor(
  name='GetConfigResponse',
  full_name='status.GetConfigResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='config', full_name='status.GetConfigResponse.config', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=405,
  serialized_end=462,
)


_SETCONFIGREQUEST = _descriptor.Descriptor(
  name='SetConfigRequest',
  full_name='status.SetConfigRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceID', full_name='status.SetConfigRequest.deviceID', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='status.SetConfigRequest.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=464,
  serialized_end=538,
)


_SETCONFIGRESPONSE = _descriptor.Descriptor(
  name='SetConfigResponse',
  full_name='status.SetConfigResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=540,
  serialized_end=559,
)


_SETCONFIGMULTIREQUEST = _descriptor.Descriptor(
  name='SetConfigMultiRequest',
  full_name='status.SetConfigMultiRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceIDs', full_name='status.SetConfigMultiRequest.deviceIDs', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='status.SetConfigMultiRequest.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=561,
  serialized_end=641,
)


_SETCONFIGMULTIRESPONSE = _descriptor.Descriptor(
  name='SetConfigMultiResponse',
  full_name='status.SetConfigMultiResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='deviceErrors', full_name='status.SetConfigMultiResponse.deviceErrors', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=643,
  serialized_end=709,
)

_LEDSTATUS.fields_by_name['deviceStatus'].enum_type = _DEVICESTATUS
_LEDSTATUS.fields_by_name['signals'].message_type = action__pb2._LEDSIGNAL
_BUZZERSTATUS.fields_by_name['deviceStatus'].enum_type = _DEVICESTATUS
_BUZZERSTATUS.fields_by_name['signals'].message_type = action__pb2._BUZZERSIGNAL
_STATUSCONFIG.fields_by_name['LEDState'].message_type = _LEDSTATUS
_STATUSCONFIG.fields_by_name['BuzzerState'].message_type = _BUZZERSTATUS
_GETCONFIGRESPONSE.fields_by_name['config'].message_type = _STATUSCONFIG
_SETCONFIGREQUEST.fields_by_name['config'].message_type = _STATUSCONFIG
_SETCONFIGMULTIREQUEST.fields_by_name['config'].message_type = _STATUSCONFIG
_SETCONFIGMULTIRESPONSE.fields_by_name['deviceErrors'].message_type = err__pb2._ERRORRESPONSE
DESCRIPTOR.message_types_by_name['LEDStatus'] = _LEDSTATUS
DESCRIPTOR.message_types_by_name['BuzzerStatus'] = _BUZZERSTATUS
DESCRIPTOR.message_types_by_name['StatusConfig'] = _STATUSCONFIG
DESCRIPTOR.message_types_by_name['GetConfigRequest'] = _GETCONFIGREQUEST
DESCRIPTOR.message_types_by_name['GetConfigResponse'] = _GETCONFIGRESPONSE
DESCRIPTOR.message_types_by_name['SetConfigRequest'] = _SETCONFIGREQUEST
DESCRIPTOR.message_types_by_name['SetConfigResponse'] = _SETCONFIGRESPONSE
DESCRIPTOR.message_types_by_name['SetConfigMultiRequest'] = _SETCONFIGMULTIREQUEST
DESCRIPTOR.message_types_by_name['SetConfigMultiResponse'] = _SETCONFIGMULTIRESPONSE
DESCRIPTOR.enum_types_by_name['DeviceStatus'] = _DEVICESTATUS
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LEDStatus = _reflection.GeneratedProtocolMessageType('LEDStatus', (_message.Message,), dict(
  DESCRIPTOR = _LEDSTATUS,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.LEDStatus)
  ))
_sym_db.RegisterMessage(LEDStatus)

BuzzerStatus = _reflection.GeneratedProtocolMessageType('BuzzerStatus', (_message.Message,), dict(
  DESCRIPTOR = _BUZZERSTATUS,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.BuzzerStatus)
  ))
_sym_db.RegisterMessage(BuzzerStatus)

StatusConfig = _reflection.GeneratedProtocolMessageType('StatusConfig', (_message.Message,), dict(
  DESCRIPTOR = _STATUSCONFIG,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.StatusConfig)
  ))
_sym_db.RegisterMessage(StatusConfig)

GetConfigRequest = _reflection.GeneratedProtocolMessageType('GetConfigRequest', (_message.Message,), dict(
  DESCRIPTOR = _GETCONFIGREQUEST,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.GetConfigRequest)
  ))
_sym_db.RegisterMessage(GetConfigRequest)

GetConfigResponse = _reflection.GeneratedProtocolMessageType('GetConfigResponse', (_message.Message,), dict(
  DESCRIPTOR = _GETCONFIGRESPONSE,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.GetConfigResponse)
  ))
_sym_db.RegisterMessage(GetConfigResponse)

SetConfigRequest = _reflection.GeneratedProtocolMessageType('SetConfigRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGREQUEST,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.SetConfigRequest)
  ))
_sym_db.RegisterMessage(SetConfigRequest)

SetConfigResponse = _reflection.GeneratedProtocolMessageType('SetConfigResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGRESPONSE,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.SetConfigResponse)
  ))
_sym_db.RegisterMessage(SetConfigResponse)

SetConfigMultiRequest = _reflection.GeneratedProtocolMessageType('SetConfigMultiRequest', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGMULTIREQUEST,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.SetConfigMultiRequest)
  ))
_sym_db.RegisterMessage(SetConfigMultiRequest)

SetConfigMultiResponse = _reflection.GeneratedProtocolMessageType('SetConfigMultiResponse', (_message.Message,), dict(
  DESCRIPTOR = _SETCONFIGMULTIRESPONSE,
  __module__ = 'status_pb2'
  # @@protoc_insertion_point(class_scope:status.SetConfigMultiResponse)
  ))
_sym_db.RegisterMessage(SetConfigMultiResponse)


DESCRIPTOR._options = None

_STATUS = _descriptor.ServiceDescriptor(
  name='Status',
  full_name='status.Status',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1177,
  serialized_end=1398,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetConfig',
    full_name='status.Status.GetConfig',
    index=0,
    containing_service=None,
    input_type=_GETCONFIGREQUEST,
    output_type=_GETCONFIGRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetConfig',
    full_name='status.Status.SetConfig',
    index=1,
    containing_service=None,
    input_type=_SETCONFIGREQUEST,
    output_type=_SETCONFIGRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetConfigMulti',
    full_name='status.Status.SetConfigMulti',
    index=2,
    containing_service=None,
    input_type=_SETCONFIGMULTIREQUEST,
    output_type=_SETCONFIGMULTIRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_STATUS)

DESCRIPTOR.services_by_name['Status'] = _STATUS

# @@protoc_insertion_point(module_scope)
