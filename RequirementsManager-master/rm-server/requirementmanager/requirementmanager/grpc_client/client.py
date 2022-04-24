import json

import grpc

from requirementmanager.grpc_client.Proto import (
    Requirement_pb2, Requirement_pb2_grpc
)
from requirementmanager.config import GRPC_SERVER_ADDRESS


class GrpcClient:
    def __init__(self, address: str = None):
        address = address or GRPC_SERVER_ADDRESS
        self.address = address

    def itemized(self, data: str):
        # 包装data
        data = {'id': '0', 'description': data, 'keyword': ['包括']}
        channel = grpc.insecure_channel(self.address)
        stub = Requirement_pb2_grpc.RequirementStub(channel)
        revalue = Requirement_pb2.ReSplitValue(value=json.dumps(data))
        response = stub.Itemized(revalue)
        return response.value1

    def structurization(self, data: str):
        channel = grpc.insecure_channel(self.address)
        stub = Requirement_pb2_grpc.RequirementStub(channel)
        value = Requirement_pb2.Value(value=data)
        response = stub.structurization(value)
        return response.value

    def conflictdetect(self, data: str):
        channel = grpc.insecure_channel(self.address)
        stub = Requirement_pb2_grpc.RequirementStub(channel)
        value = Requirement_pb2.Value(value=data)
        response = stub.conflictdetect(value)
        return response.value

    def relationship(self, data: str):
        channel = grpc.insecure_channel(self.address)
        stub = Requirement_pb2_grpc.RequirementStub(channel)
        value = Requirement_pb2.Value(value=data)
        response = stub.relationship(value)
        return response.value

    def similarity(self, data: str):
        channel = grpc.insecure_channel(self.address)
        stub = Requirement_pb2_grpc.RequirementStub(channel)
        value = Requirement_pb2.Value(value=data)
        response = stub.similarity(value)
        return response.value
