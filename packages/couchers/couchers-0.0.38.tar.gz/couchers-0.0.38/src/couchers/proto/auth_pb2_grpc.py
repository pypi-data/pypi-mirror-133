# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import auth_pb2 as auth__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class AuthStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SignupFlow = channel.unary_unary(
                '/org.couchers.auth.Auth/SignupFlow',
                request_serializer=auth__pb2.SignupFlowReq.SerializeToString,
                response_deserializer=auth__pb2.SignupFlowRes.FromString,
                )
        self.UsernameValid = channel.unary_unary(
                '/org.couchers.auth.Auth/UsernameValid',
                request_serializer=auth__pb2.UsernameValidReq.SerializeToString,
                response_deserializer=auth__pb2.UsernameValidRes.FromString,
                )
        self.Login = channel.unary_unary(
                '/org.couchers.auth.Auth/Login',
                request_serializer=auth__pb2.LoginReq.SerializeToString,
                response_deserializer=auth__pb2.LoginRes.FromString,
                )
        self.CompleteTokenLogin = channel.unary_unary(
                '/org.couchers.auth.Auth/CompleteTokenLogin',
                request_serializer=auth__pb2.CompleteTokenLoginReq.SerializeToString,
                response_deserializer=auth__pb2.AuthRes.FromString,
                )
        self.Authenticate = channel.unary_unary(
                '/org.couchers.auth.Auth/Authenticate',
                request_serializer=auth__pb2.AuthReq.SerializeToString,
                response_deserializer=auth__pb2.AuthRes.FromString,
                )
        self.Deauthenticate = channel.unary_unary(
                '/org.couchers.auth.Auth/Deauthenticate',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ResetPassword = channel.unary_unary(
                '/org.couchers.auth.Auth/ResetPassword',
                request_serializer=auth__pb2.ResetPasswordReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.CompletePasswordReset = channel.unary_unary(
                '/org.couchers.auth.Auth/CompletePasswordReset',
                request_serializer=auth__pb2.CompletePasswordResetReq.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.ConfirmChangeEmail = channel.unary_unary(
                '/org.couchers.auth.Auth/ConfirmChangeEmail',
                request_serializer=auth__pb2.ConfirmChangeEmailReq.SerializeToString,
                response_deserializer=auth__pb2.ConfirmChangeEmailRes.FromString,
                )


class AuthServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SignupFlow(self, request, context):
        """
        Authentication API

        This API facilitates authentication actions: signup and signin. Users need to use this before logging in, so you don't
        need to be authorized to use it.

        The signup flow is as follows:
        A user enters their email and submits a form, which fires off a Signup call
        Signup validates the email isn't in the database yet, creates a signup_token, and emails it to the email address
        User clicks on the signup link, which brings them onto the signup completion form
        When this form loads, the app queries SignupTokenInfo for the email address associated to that login token to
        display in the UI
        User chooses a username (possibly querying UsernameValid to check possibly usernames) and fills in other basic
        information
        User submits the signup completion form, which validates this input, creates the user and logs them in, returns a
        session token (signup token is invalidated)

        The login flow is as follows:
        The user enters an identifier field and submits the form
        The backend finds the user based on either username/user id/email address
        If that user _does not_ have a password, we email a one-click signin token and return SENT_LOGIN_EMAIL
        If that user _does not_ have a password, they click that link and the app logs them in through a
        CompleteTokenLoginReq (login token is invalidated)
        If that user _does_ have a password, the app asks for that password, and submits an Authenticate Call to log the
        user in

        Signup and login tokens expire after some time, and once used cannot be reused.

        There can be multiple signup requests simultaneously with the same email address. Email address uniqueness is checked
        once when creating the signup request, and again when creating the user.

        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UsernameValid(self, request, context):
        """Check whether the username is valid and available
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Login(self, request, context):
        """First step of login flow.

        The user is searched for using their id, username, or email.

        If the user does not exist or has been deleted, throws a NOT_FOUND rpc error.

        If the user has a password, returns NEED_PASSWORD.

        If the user exists but does not have a password, generates a login token, send it in the email and returns
        SENT_LOGIN_EMAIL.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CompleteTokenLogin(self, request, context):
        """Complete a login after receiving an email with a login token
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Authenticate(self, request, context):
        """Auth a user with username + password
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deauthenticate(self, request, context):
        """Invalidate a session, deauthing a user
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ResetPassword(self, request, context):
        """Sends a forgot password email to the given user if the user exists, returns no output (so you can't go around
        guessing email addresses)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CompletePasswordReset(self, request, context):
        """Triggered when the user goes to the link sent in the forgot password email
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmChangeEmail(self, request, context):
        """Triggered when the user goes to the link sent in the either email_changed_confirmation_*_email
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AuthServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SignupFlow': grpc.unary_unary_rpc_method_handler(
                    servicer.SignupFlow,
                    request_deserializer=auth__pb2.SignupFlowReq.FromString,
                    response_serializer=auth__pb2.SignupFlowRes.SerializeToString,
            ),
            'UsernameValid': grpc.unary_unary_rpc_method_handler(
                    servicer.UsernameValid,
                    request_deserializer=auth__pb2.UsernameValidReq.FromString,
                    response_serializer=auth__pb2.UsernameValidRes.SerializeToString,
            ),
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=auth__pb2.LoginReq.FromString,
                    response_serializer=auth__pb2.LoginRes.SerializeToString,
            ),
            'CompleteTokenLogin': grpc.unary_unary_rpc_method_handler(
                    servicer.CompleteTokenLogin,
                    request_deserializer=auth__pb2.CompleteTokenLoginReq.FromString,
                    response_serializer=auth__pb2.AuthRes.SerializeToString,
            ),
            'Authenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=auth__pb2.AuthReq.FromString,
                    response_serializer=auth__pb2.AuthRes.SerializeToString,
            ),
            'Deauthenticate': grpc.unary_unary_rpc_method_handler(
                    servicer.Deauthenticate,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ResetPassword': grpc.unary_unary_rpc_method_handler(
                    servicer.ResetPassword,
                    request_deserializer=auth__pb2.ResetPasswordReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'CompletePasswordReset': grpc.unary_unary_rpc_method_handler(
                    servicer.CompletePasswordReset,
                    request_deserializer=auth__pb2.CompletePasswordResetReq.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'ConfirmChangeEmail': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmChangeEmail,
                    request_deserializer=auth__pb2.ConfirmChangeEmailReq.FromString,
                    response_serializer=auth__pb2.ConfirmChangeEmailRes.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'org.couchers.auth.Auth', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Auth(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SignupFlow(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/SignupFlow',
            auth__pb2.SignupFlowReq.SerializeToString,
            auth__pb2.SignupFlowRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UsernameValid(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/UsernameValid',
            auth__pb2.UsernameValidReq.SerializeToString,
            auth__pb2.UsernameValidRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/Login',
            auth__pb2.LoginReq.SerializeToString,
            auth__pb2.LoginRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CompleteTokenLogin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/CompleteTokenLogin',
            auth__pb2.CompleteTokenLoginReq.SerializeToString,
            auth__pb2.AuthRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Authenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/Authenticate',
            auth__pb2.AuthReq.SerializeToString,
            auth__pb2.AuthRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Deauthenticate(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/Deauthenticate',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ResetPassword(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/ResetPassword',
            auth__pb2.ResetPasswordReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CompletePasswordReset(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/CompletePasswordReset',
            auth__pb2.CompletePasswordResetReq.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConfirmChangeEmail(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/org.couchers.auth.Auth/ConfirmChangeEmail',
            auth__pb2.ConfirmChangeEmailReq.SerializeToString,
            auth__pb2.ConfirmChangeEmailRes.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
