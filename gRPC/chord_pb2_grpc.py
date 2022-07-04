# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import gRPC.chord_pb2 as chord__pb2


class RouteGuideStub(object):
    """Interface exported by the server.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Alive = channel.unary_unary(
                '/routeguide.RouteGuide/Alive',
                request_serializer=chord__pb2.Feature.SerializeToString,
                response_deserializer=chord__pb2.Feature.FromString,
                )
        self.Join = channel.unary_unary(
                '/routeguide.RouteGuide/Join',
                request_serializer=chord__pb2.Feature.SerializeToString,
                response_deserializer=chord__pb2.Feature.FromString,
                )
        self.Find_succ = channel.unary_unary(
                '/routeguide.RouteGuide/Find_succ',
                request_serializer=chord__pb2.Idvalue.SerializeToString,
                response_deserializer=chord__pb2.Address.FromString,
                )
        self.Find_pred = channel.unary_unary(
                '/routeguide.RouteGuide/Find_pred',
                request_serializer=chord__pb2.Idvalue.SerializeToString,
                response_deserializer=chord__pb2.Address.FromString,
                )
        self.Get_succ_list = channel.unary_unary(
                '/routeguide.RouteGuide/Get_succ_list',
                request_serializer=chord__pb2.Feature.SerializeToString,
                response_deserializer=chord__pb2.Address_list.FromString,
                )
        self.Closest_pred_fing = channel.unary_unary(
                '/routeguide.RouteGuide/Closest_pred_fing',
                request_serializer=chord__pb2.Idvalue.SerializeToString,
                response_deserializer=chord__pb2.Address.FromString,
                )
        self.Get_pred = channel.unary_unary(
                '/routeguide.RouteGuide/Get_pred',
                request_serializer=chord__pb2.Feature.SerializeToString,
                response_deserializer=chord__pb2.Address.FromString,
                )
        self.Rectify = channel.unary_unary(
                '/routeguide.RouteGuide/Rectify',
                request_serializer=chord__pb2.Address.SerializeToString,
                response_deserializer=chord__pb2.Feature.FromString,
                )
        self.Get_storage = channel.unary_unary(
                '/routeguide.RouteGuide/Get_storage',
                request_serializer=chord__pb2.Address.SerializeToString,
                response_deserializer=chord__pb2.Storage.FromString,
                )
        self.Get_non_storage = channel.unary_unary(
                '/routeguide.RouteGuide/Get_non_storage',
                request_serializer=chord__pb2.Address.SerializeToString,
                response_deserializer=chord__pb2.Storage.FromString,
                )
        self.Make_storage = channel.unary_unary(
                '/routeguide.RouteGuide/Make_storage',
                request_serializer=chord__pb2.Storage_make_data.SerializeToString,
                response_deserializer=chord__pb2.Feature.FromString,
                )
        self.Remove_storage = channel.unary_unary(
                '/routeguide.RouteGuide/Remove_storage',
                request_serializer=chord__pb2.Feature.SerializeToString,
                response_deserializer=chord__pb2.Feature.FromString,
                )
        self.Get_storage_by_id = channel.unary_unary(
                '/routeguide.RouteGuide/Get_storage_by_id',
                request_serializer=chord__pb2.Address.SerializeToString,
                response_deserializer=chord__pb2.Address.FromString,
                )


class RouteGuideServicer(object):
    """Interface exported by the server.
    """

    def Alive(self, request, context):
        """Basic message to recognize if there is a steady connection
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Join(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Find_succ(self, request, context):
        """Returns the address of the succesor node
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Find_pred(self, request, context):
        """Returns the address of the predecessor node after looking for it
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_succ_list(self, request, context):
        """Returns list of successor nodes
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Closest_pred_fing(self, request, context):
        """Returns the address of the closest predecessor node
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_pred(self, request, context):
        """Returns the address of the predecessor node
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Rectify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_storage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_non_storage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Make_storage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Remove_storage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get_storage_by_id(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RouteGuideServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Alive': grpc.unary_unary_rpc_method_handler(
                    servicer.Alive,
                    request_deserializer=chord__pb2.Feature.FromString,
                    response_serializer=chord__pb2.Feature.SerializeToString,
            ),
            'Join': grpc.unary_unary_rpc_method_handler(
                    servicer.Join,
                    request_deserializer=chord__pb2.Feature.FromString,
                    response_serializer=chord__pb2.Feature.SerializeToString,
            ),
            'Find_succ': grpc.unary_unary_rpc_method_handler(
                    servicer.Find_succ,
                    request_deserializer=chord__pb2.Idvalue.FromString,
                    response_serializer=chord__pb2.Address.SerializeToString,
            ),
            'Find_pred': grpc.unary_unary_rpc_method_handler(
                    servicer.Find_pred,
                    request_deserializer=chord__pb2.Idvalue.FromString,
                    response_serializer=chord__pb2.Address.SerializeToString,
            ),
            'Get_succ_list': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_succ_list,
                    request_deserializer=chord__pb2.Feature.FromString,
                    response_serializer=chord__pb2.Address_list.SerializeToString,
            ),
            'Closest_pred_fing': grpc.unary_unary_rpc_method_handler(
                    servicer.Closest_pred_fing,
                    request_deserializer=chord__pb2.Idvalue.FromString,
                    response_serializer=chord__pb2.Address.SerializeToString,
            ),
            'Get_pred': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_pred,
                    request_deserializer=chord__pb2.Feature.FromString,
                    response_serializer=chord__pb2.Address.SerializeToString,
            ),
            'Rectify': grpc.unary_unary_rpc_method_handler(
                    servicer.Rectify,
                    request_deserializer=chord__pb2.Address.FromString,
                    response_serializer=chord__pb2.Feature.SerializeToString,
            ),
            'Get_storage': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_storage,
                    request_deserializer=chord__pb2.Address.FromString,
                    response_serializer=chord__pb2.Storage.SerializeToString,
            ),
            'Get_non_storage': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_non_storage,
                    request_deserializer=chord__pb2.Address.FromString,
                    response_serializer=chord__pb2.Storage.SerializeToString,
            ),
            'Make_storage': grpc.unary_unary_rpc_method_handler(
                    servicer.Make_storage,
                    request_deserializer=chord__pb2.Storage_make_data.FromString,
                    response_serializer=chord__pb2.Feature.SerializeToString,
            ),
            'Remove_storage': grpc.unary_unary_rpc_method_handler(
                    servicer.Remove_storage,
                    request_deserializer=chord__pb2.Feature.FromString,
                    response_serializer=chord__pb2.Feature.SerializeToString,
            ),
            'Get_storage_by_id': grpc.unary_unary_rpc_method_handler(
                    servicer.Get_storage_by_id,
                    request_deserializer=chord__pb2.Address.FromString,
                    response_serializer=chord__pb2.Address.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'routeguide.RouteGuide', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RouteGuide(object):
    """Interface exported by the server.
    """

    @staticmethod
    def Alive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Alive',
            chord__pb2.Feature.SerializeToString,
            chord__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Join(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Join',
            chord__pb2.Feature.SerializeToString,
            chord__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Find_succ(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Find_succ',
            chord__pb2.Idvalue.SerializeToString,
            chord__pb2.Address.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Find_pred(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Find_pred',
            chord__pb2.Idvalue.SerializeToString,
            chord__pb2.Address.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_succ_list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Get_succ_list',
            chord__pb2.Feature.SerializeToString,
            chord__pb2.Address_list.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Closest_pred_fing(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Closest_pred_fing',
            chord__pb2.Idvalue.SerializeToString,
            chord__pb2.Address.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_pred(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Get_pred',
            chord__pb2.Feature.SerializeToString,
            chord__pb2.Address.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Rectify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Rectify',
            chord__pb2.Address.SerializeToString,
            chord__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_storage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Get_storage',
            chord__pb2.Address.SerializeToString,
            chord__pb2.Storage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_non_storage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Get_non_storage',
            chord__pb2.Address.SerializeToString,
            chord__pb2.Storage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Make_storage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Make_storage',
            chord__pb2.Storage_make_data.SerializeToString,
            chord__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Remove_storage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Remove_storage',
            chord__pb2.Feature.SerializeToString,
            chord__pb2.Feature.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get_storage_by_id(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/routeguide.RouteGuide/Get_storage_by_id',
            chord__pb2.Address.SerializeToString,
            chord__pb2.Address.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
