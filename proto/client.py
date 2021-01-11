import grpc
import simple_pb2
import simple_pb2_grpc

root = open("../certs/root.crt", "rb").read()
cred = grpc.ssl_channel_credentials(root_certificates=root)

#with grpc.insecure_channel('localhost:5051') as channel:
with grpc.secure_channel("localhost:51011", cred) as channel:
    stub = simple_pb2_grpc.SimpleServiceStub(channel)
    name = "Tom"
    msg = "Test"
    response = stub.SimpleSend(simple_pb2.SimpleRequest(name=name, msg=msg))

print('Reply: ', response.reply_msg)

#with grpc.insecure_channel('localhost:5051') as channel:
with grpc.secure_channel("localhost:51011", cred) as channel:
    stub = simple_pb2_grpc.SimpleServiceStub(channel)
    key = "key1"
    response = stub.ListSend(simple_pb2.ListRequest(key=key))

print('Reply: ', response.reply_list)

#with grpc.insecure_channel('localhost:5051') as channel:
with grpc.secure_channel("localhost:51011", cred) as channel:
    stub = simple_pb2_grpc.SimpleServiceStub(channel)
    key = "key1"
    response = stub.DictSend(simple_pb2.DictRequest(key=key))

print('Reply: ', response.reply_kv)
