# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: discussions.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import annotations_pb2 as annotations__pb2
from . import threads_pb2 as threads__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='discussions.proto',
  package='org.couchers.api.discussions',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x64iscussions.proto\x12\x1corg.couchers.api.discussions\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x11\x61nnotations.proto\x1a\rthreads.proto\"\xa0\x02\n\nDiscussion\x12\x15\n\rdiscussion_id\x18\x01 \x01(\x03\x12\x0c\n\x04slug\x18\x02 \x01(\t\x12+\n\x07\x63reated\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x17\n\x0f\x63reator_user_id\x18\x04 \x01(\x03\x12\x1c\n\x12owner_community_id\x18\x05 \x01(\x03H\x00\x12\x18\n\x0eowner_group_id\x18\x06 \x01(\x03H\x00\x12\r\n\x05title\x18\x07 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x08 \x01(\t\x12\x30\n\x06thread\x18\x0b \x01(\x0b\x32 .org.couchers.api.threads.Thread\x12\x14\n\x0c\x63\x61n_moderate\x18\n \x01(\x08\x42\x07\n\x05owner\"v\n\x13\x43reateDiscussionReq\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\x12\x1c\n\x12owner_community_id\x18\x03 \x01(\x03H\x00\x12\x18\n\x0eowner_group_id\x18\x04 \x01(\x03H\x00\x42\x07\n\x05owner\")\n\x10GetDiscussionReq\x12\x15\n\rdiscussion_id\x18\x01 \x01(\x03\x32\xf3\x01\n\x0b\x44iscussions\x12q\n\x10\x43reateDiscussion\x12\x31.org.couchers.api.discussions.CreateDiscussionReq\x1a(.org.couchers.api.discussions.Discussion\"\x00\x12k\n\rGetDiscussion\x12..org.couchers.api.discussions.GetDiscussionReq\x1a(.org.couchers.api.discussions.Discussion\"\x00\x1a\x04\x88\xb5\x18\x03\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,annotations__pb2.DESCRIPTOR,threads__pb2.DESCRIPTOR,])




_DISCUSSION = _descriptor.Descriptor(
  name='Discussion',
  full_name='org.couchers.api.discussions.Discussion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='discussion_id', full_name='org.couchers.api.discussions.Discussion.discussion_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='slug', full_name='org.couchers.api.discussions.Discussion.slug', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created', full_name='org.couchers.api.discussions.Discussion.created', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='creator_user_id', full_name='org.couchers.api.discussions.Discussion.creator_user_id', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner_community_id', full_name='org.couchers.api.discussions.Discussion.owner_community_id', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner_group_id', full_name='org.couchers.api.discussions.Discussion.owner_group_id', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='org.couchers.api.discussions.Discussion.title', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='org.couchers.api.discussions.Discussion.content', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='thread', full_name='org.couchers.api.discussions.Discussion.thread', index=8,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='can_moderate', full_name='org.couchers.api.discussions.Discussion.can_moderate', index=9,
      number=10, type=8, cpp_type=7, label=1,
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
    _descriptor.OneofDescriptor(
      name='owner', full_name='org.couchers.api.discussions.Discussion.owner',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=119,
  serialized_end=407,
)


_CREATEDISCUSSIONREQ = _descriptor.Descriptor(
  name='CreateDiscussionReq',
  full_name='org.couchers.api.discussions.CreateDiscussionReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='org.couchers.api.discussions.CreateDiscussionReq.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='content', full_name='org.couchers.api.discussions.CreateDiscussionReq.content', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner_community_id', full_name='org.couchers.api.discussions.CreateDiscussionReq.owner_community_id', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='owner_group_id', full_name='org.couchers.api.discussions.CreateDiscussionReq.owner_group_id', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
    _descriptor.OneofDescriptor(
      name='owner', full_name='org.couchers.api.discussions.CreateDiscussionReq.owner',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=409,
  serialized_end=527,
)


_GETDISCUSSIONREQ = _descriptor.Descriptor(
  name='GetDiscussionReq',
  full_name='org.couchers.api.discussions.GetDiscussionReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='discussion_id', full_name='org.couchers.api.discussions.GetDiscussionReq.discussion_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=529,
  serialized_end=570,
)

_DISCUSSION.fields_by_name['created'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_DISCUSSION.fields_by_name['thread'].message_type = threads__pb2._THREAD
_DISCUSSION.oneofs_by_name['owner'].fields.append(
  _DISCUSSION.fields_by_name['owner_community_id'])
_DISCUSSION.fields_by_name['owner_community_id'].containing_oneof = _DISCUSSION.oneofs_by_name['owner']
_DISCUSSION.oneofs_by_name['owner'].fields.append(
  _DISCUSSION.fields_by_name['owner_group_id'])
_DISCUSSION.fields_by_name['owner_group_id'].containing_oneof = _DISCUSSION.oneofs_by_name['owner']
_CREATEDISCUSSIONREQ.oneofs_by_name['owner'].fields.append(
  _CREATEDISCUSSIONREQ.fields_by_name['owner_community_id'])
_CREATEDISCUSSIONREQ.fields_by_name['owner_community_id'].containing_oneof = _CREATEDISCUSSIONREQ.oneofs_by_name['owner']
_CREATEDISCUSSIONREQ.oneofs_by_name['owner'].fields.append(
  _CREATEDISCUSSIONREQ.fields_by_name['owner_group_id'])
_CREATEDISCUSSIONREQ.fields_by_name['owner_group_id'].containing_oneof = _CREATEDISCUSSIONREQ.oneofs_by_name['owner']
DESCRIPTOR.message_types_by_name['Discussion'] = _DISCUSSION
DESCRIPTOR.message_types_by_name['CreateDiscussionReq'] = _CREATEDISCUSSIONREQ
DESCRIPTOR.message_types_by_name['GetDiscussionReq'] = _GETDISCUSSIONREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Discussion = _reflection.GeneratedProtocolMessageType('Discussion', (_message.Message,), {
  'DESCRIPTOR' : _DISCUSSION,
  '__module__' : 'discussions_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.discussions.Discussion)
  })
_sym_db.RegisterMessage(Discussion)

CreateDiscussionReq = _reflection.GeneratedProtocolMessageType('CreateDiscussionReq', (_message.Message,), {
  'DESCRIPTOR' : _CREATEDISCUSSIONREQ,
  '__module__' : 'discussions_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.discussions.CreateDiscussionReq)
  })
_sym_db.RegisterMessage(CreateDiscussionReq)

GetDiscussionReq = _reflection.GeneratedProtocolMessageType('GetDiscussionReq', (_message.Message,), {
  'DESCRIPTOR' : _GETDISCUSSIONREQ,
  '__module__' : 'discussions_pb2'
  # @@protoc_insertion_point(class_scope:org.couchers.api.discussions.GetDiscussionReq)
  })
_sym_db.RegisterMessage(GetDiscussionReq)



_DISCUSSIONS = _descriptor.ServiceDescriptor(
  name='Discussions',
  full_name='org.couchers.api.discussions.Discussions',
  file=DESCRIPTOR,
  index=0,
  serialized_options=b'\210\265\030\003',
  create_key=_descriptor._internal_create_key,
  serialized_start=573,
  serialized_end=816,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateDiscussion',
    full_name='org.couchers.api.discussions.Discussions.CreateDiscussion',
    index=0,
    containing_service=None,
    input_type=_CREATEDISCUSSIONREQ,
    output_type=_DISCUSSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='GetDiscussion',
    full_name='org.couchers.api.discussions.Discussions.GetDiscussion',
    index=1,
    containing_service=None,
    input_type=_GETDISCUSSIONREQ,
    output_type=_DISCUSSION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_DISCUSSIONS)

DESCRIPTOR.services_by_name['Discussions'] = _DISCUSSIONS

# @@protoc_insertion_point(module_scope)
