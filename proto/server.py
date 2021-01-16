import grpc
import time
import simple_pb2
import simple_pb2_grpc
from concurrent import futures


class SimpleServiceServicer(simple_pb2_grpc.SimpleServiceServicer):
    def __init__(self):
        pass

    def SimpleSend(self, request, context):
        print('logging: name {}, msg {}'.format(request.name, request.msg))
        # protoファイルのResponseと一致させる
        return simple_pb2.SimpleResponse(
            reply_msg='Hello! ' + request.name + '. Your message is ' + request.msg
        )

    def ListSend(self, request, context):
        print('logging: key {}'.format(request.key))
        return simple_pb2.ListResponse(
            reply_list=['message1', 'message2']
        )

    def DictSend(self, request, context):
        print('logging: key {}'.format(request.key))
        # protoファイルのResponseと一致させる
        return simple_pb2.DictResponse(
            reply_kv=dict(key1="hogehoge")
        )


# start server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
simple_pb2_grpc.add_SimpleServiceServicer_to_server(SimpleServiceServicer(), server)
# server.add_insecure_port('[::]:5051')
pkey = open("../certs/privkey.pem", "rb").read()
chain = open("../certs/cert.pem", "rb").read()
cred = grpc.ssl_server_credentials([(pkey, chain)])
server.add_secure_port('localhost:51011', cred)
server.start()
print('run server')

# wait
try:
    while True:
        time.sleep(3600)
except KeyboardInterrupt:
    # stop server
    server.stop(0)
