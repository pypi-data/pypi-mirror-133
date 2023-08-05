# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: account.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from . import annotations_pb2 as annotations__pb2
from . import auth_pb2 as auth__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='account.proto',
  package='org.couchers.api.account',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\raccount.proto\x12\x18org.couchers.api.account\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x11\x61nnotations.proto\x1a\nauth.proto\"\x81\x02\n\x11GetAccountInfoRes\x12M\n\x0clogin_method\x18\x01 \x01(\x0e\x32\x37.org.couchers.api.account.GetAccountInfoRes.LoginMethod\x12\x14\n\x0chas_password\x18\x02 \x01(\x08\x12\x10\n\x08username\x18\x07 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x18\n\x10profile_complete\x18\x04 \x01(\x08\x12\r\n\x05phone\x18\x05 \x01(\t\x12\x10\n\x08timezone\x18\x06 \x01(\t\"+\n\x0bLoginMethod\x12\x0e\n\nMAGIC_LINK\x10\x00\x12\x0c\n\x08PASSWORD\x10\x01\"\x87\x01\n\x11\x43hangePasswordReq\x12\x38\n\x0cold_password\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x04\x80\xb5\x18\x01\x12\x38\n\x0cnew_password\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x04\x80\xb5\x18\x01\"Y\n\x0e\x43hangeEmailReq\x12\x34\n\x08password\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x04\x80\xb5\x18\x01\x12\x11\n\tnew_email\x18\x02 \x01(\t\"<\n\x19GetContributorFormInfoRes\x12\x1f\n\x17\x66illed_contributor_form\x18\x01 \x01(\x08\"V\n\x16\x46illContributorFormReq\x12<\n\x10\x63ontributor_form\x18\x01 \x01(\x0b\x32\".org.couchers.auth.ContributorForm\"\x1f\n\x0e\x43hangePhoneReq\x12\r\n\x05phone\x18\x01 \x01(\t\"%\n\x0eVerifyPhoneReq\x12\x13\n\x05token\x18\x01 \x01(\tB\x04\x80\xb5\x18\x01\x32\x86\x05\n\x07\x41\x63\x63ount\x12W\n\x0eGetAccountInfo\x12\x16.google.protobuf.Empty\x1a+.org.couchers.api.account.GetAccountInfoRes\"\x00\x12W\n\x0e\x43hangePassword\x12+.org.couchers.api.account.ChangePasswordReq\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0b\x43hangeEmail\x12(.org.couchers.api.account.ChangeEmailReq\x1a\x16.google.protobuf.Empty\"\x00\x12g\n\x16GetContributorFormInfo\x12\x16.google.protobuf.Empty\x1a\x33.org.couchers.api.account.GetContributorFormInfoRes\"\x00\x12\x61\n\x13\x46illContributorForm\x12\x30.org.couchers.api.account.FillContributorFormReq\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0b\x43hangePhone\x12(.org.couchers.api.account.ChangePhoneReq\x1a\x16.google.protobuf.Empty\"\x00\x12Q\n\x0bVerifyPhone\x12(.org.couchers.api.account.VerifyPhoneReq\x1a\x16.google.protobuf.Empty\"\x00\x1a\x04\x88\xb5\x18\x03\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,annotations__pb2.DESCRIPTOR,auth__pb2.DESCRIPTOR,])



_GETACCOUNTINFORES_LOGINMETHOD = _descriptor.EnumDescriptor(
  name='LoginMethod',
  full_name='org.couchers.api.account.GetAccountInfoRes.LoginMethod',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MAGIC_LINK', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='PASSWORD', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=350,
  serialized_end=393,
)
_sym_db.RegisterEnumDescriptor(_GETACCOUNTINFORES_LOGINMETHOD)


_GETACCOUNTINFORES = _descriptor.Descriptor(
  name='GetAccountInfoRes',
  full_name='org.couchers.api.account.GetAccountInfoRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='login_method', full_name='org.couchers.api.account.GetAccountInfoRes.login_method', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='has_password', full_name='org.couchers.api.account.GetAccountInfoRes.has_password', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='username', full_name='org.couchers.api.account.GetAccountInfoRes.username', index=2,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='org.couchers.api.account.GetAccountInfoRes.email', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='profile_complete', full_name='org.couchers.api.account.GetAccountInfoRes.profile_complete', index=4,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phone', full_name='org.couchers.api.account.GetAccountInfoRes.phone', index=5,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timezone', full_name='org.couchers.api.account.GetAccountInfoRes.timezone', index=6,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GETACCOUNTINFORES_LOGINMETHOD,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=136,
  serialized_end=393,
)


_CHANGEPASSWORDREQ = _descriptor.Descriptor(
  name='ChangePasswordReq',
  full_name='org.couchers.api.account.ChangePasswordReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='old_password', full_name='org.couchers.api.account.ChangePasswordReq.old_password', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_password', full_name='org.couchers.api.account.ChangePasswordReq.new_password', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=396,
  serialized_end=531,
)


_CHANGEEMAILREQ = _descriptor.Descriptor(
  name='ChangeEmailReq',
  full_name='org.couchers.api.account.ChangeEmailReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='password', full_name='org.couchers.api.account.ChangeEmailReq.password', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='new_email', full_name='org.couchers.api.account.ChangeEmailReq.new_email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=533,
  serialized_end=622,
)


_GETCONTRIBUTORFORMINFORES = _descriptor.Descriptor(
  name='GetContributorFormInfoRes',
  full_name='org.couchers.api.account.GetContributorFormInfoRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='filled_contributor_form', full_name='org.couchers.api.account.GetContributorFormInfoRes.filled_contributor_form', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=624,
  serialized_end=684,
)


_FILLCONTRIBUTORFORMREQ = _descriptor.Descriptor(
  name='FillContributorFormReq',
  full_name='org.couchers.api.account.FillContributorFormReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='contributor_form', full_name='org.couchers.api.account.FillContributorFormReq.contributor_form', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=686,
  serialized_end=772,
)


_CHANGEPHONEREQ = _descriptor.Descriptor(
  name='ChangePhoneReq',
  full_name='org.couchers.api.account.ChangePhoneReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='phone', full_name='org.couchers.api.account.ChangePhoneReq.phone', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=774,
  serialized_end=805,
)


_VERIFYPHONEREQ = _descriptor.Descriptor(
  name='VerifyPhoneReq',
  full_name='org.couchers.api.account.VerifyPhoneReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='token', full_name='org.couchers.api.account.VerifyPhoneReq.token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\200\265\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=807,
  serialized_end=844,
)

_GETACCOUNTINFORES.fields_by_name['login_method'].enum_type = _GETACCOUNTINFORES_LOGINMETHOD
_GETACCOUNTINFORES_LOGINMETHOD.containing_type = _GETACCOUNTINFORES
_CHANGEPASSWORDREQ.fields_by_name['old_password'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGEPASSWORDREQ.fields_by_name['new_password'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_CHANGEEMAILREQ.fields_by_name['password'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_FILLCONTRIBUTORFORMREQ.fields_by_name['contributor_form'].message_type = auth__pb2._CONTRIBUTORFORM
DESCRIPTOR.message_types_by_name['GetAccountInfoRes'] = _GETACCOUNTINFORES
DESCRIPTOR.message_types_by_name['ChangePasswordReq'] = _CHANGEPASSWORDREQ
DESCRIPTOR.message_types_by_name['ChangeEmailReq'] = _CHANGEEMAILREQ
DESCRIPTOR.message_types_by_name['GetContributorFormInfoRes'] = _GETCONTRIBUTORFORMINFORES
DESCRIPTOR.message_types_by_name['FillContributorFormReq'] = _FILLCONTRIBUTORFORMREQ
DESCRIPTOR.message_types_by_name['ChangePhoneReq'] = _CHANGEPHONEREQ
DESCRIPTOR.message_types_by_name['VerifyPhoneReq'] = _VERIFYPHONEREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GetAccountInfoRes = _reflection.GeneratedProtocolMessageType('GetAccountInfoRes', (_message.Message,), {
  'DESCRIPTOR' : _GETACCOUNTINFORES,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.GetAccountInfoRes)
  })
_sym_db.RegisterMessage(GetAccountInfoRes)

ChangePasswordReq = _reflection.GeneratedProtocolMessageType('ChangePasswordReq', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEPASSWORDREQ,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.ChangePasswordReq)
  })
_sym_db.RegisterMessage(ChangePasswordReq)

ChangeEmailReq = _reflection.GeneratedProtocolMessageType('ChangeEmailReq', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEEMAILREQ,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.ChangeEmailReq)
  })
_sym_db.RegisterMessage(ChangeEmailReq)

GetContributorFormInfoRes = _reflection.GeneratedProtocolMessageType('GetContributorFormInfoRes', (_message.Message,), {
  'DESCRIPTOR' : _GETCONTRIBUTORFORMINFORES,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.GetContributorFormInfoRes)
  })
_sym_db.RegisterMessage(GetContributorFormInfoRes)

FillContributorFormReq = _reflection.GeneratedProtocolMessageType('FillContributorFormReq', (_message.Message,), {
  'DESCRIPTOR' : _FILLCONTRIBUTORFORMREQ,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.FillContributorFormReq)
  })
_sym_db.RegisterMessage(FillContributorFormReq)

ChangePhoneReq = _reflection.GeneratedProtocolMessageType('ChangePhoneReq', (_message.Message,), {
  'DESCRIPTOR' : _CHANGEPHONEREQ,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.ChangePhoneReq)
  })
_sym_db.RegisterMessage(ChangePhoneReq)

VerifyPhoneReq = _reflection.GeneratedProtocolMessageType('VerifyPhoneReq', (_message.Message,), {
  'DESCRIPTOR' : _VERIFYPHONEREQ,
  '__module__' : 'account_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.account.VerifyPhoneReq)
  })
_sym_db.RegisterMessage(VerifyPhoneReq)


_CHANGEPASSWORDREQ.fields_by_name['old_password']._options = None
_CHANGEPASSWORDREQ.fields_by_name['new_password']._options = None
_CHANGEEMAILREQ.fields_by_name['password']._options = None
_VERIFYPHONEREQ.fields_by_name['token']._options = None

_ACCOUNT = _descriptor.ServiceDescriptor(
  name='Account',
  full_name='org.couchers.api.account.Account',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\210\265\030\003',
  create_key=_descriptor._internal_create_key,
  serialized_start=847,
  serialized_end=1493,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetAccountInfo',
    full_name='org.couchers.api.account.Account.GetAccountInfo',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_GETACCOUNTINFORES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ChangePassword',
    full_name='org.couchers.api.account.Account.ChangePassword',
    index=1,
    containing_service=None,
    input_type=_CHANGEPASSWORDREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ChangeEmail',
    full_name='org.couchers.api.account.Account.ChangeEmail',
    index=2,
    containing_service=None,
    input_type=_CHANGEEMAILREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetContributorFormInfo',
    full_name='org.couchers.api.account.Account.GetContributorFormInfo',
    index=3,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_GETCONTRIBUTORFORMINFORES,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='FillContributorForm',
    full_name='org.couchers.api.account.Account.FillContributorForm',
    index=4,
    containing_service=None,
    input_type=_FILLCONTRIBUTORFORMREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ChangePhone',
    full_name='org.couchers.api.account.Account.ChangePhone',
    index=5,
    containing_service=None,
    input_type=_CHANGEPHONEREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='VerifyPhone',
    full_name='org.couchers.api.account.Account.VerifyPhone',
    index=6,
    containing_service=None,
    input_type=_VERIFYPHONEREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_ACCOUNT)

DESCRIPTOR.services_by_name['Account'] = _ACCOUNT

# @@protoc_insertion_point(module_scope)
