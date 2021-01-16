# gRPC/TLSサンプル
## TLS環境
* 秘密鍵と公開鍵を作成

```
$ openssl req -x509 -nodes -newkey rsa:2048 -days 365 -keyout privkey.pem -out cert.pem -subj "/CN=localhost"
```

* 公開鍵でroot証明書を作る

```
$ openssl  x509 -in cert.pem -out root.crt
```

* 配置

```
(venv) TetsuonacBookea:gRPCSample1 thetsuthetsu$ pwd
/Users/thetsuthetsu/PycharmProjects/gRPCSample1
(venv) TetsuonacBookea:gRPCSample1 thetsuthetsu$ ls certs
cert.pem        privkey.pem     readme.md       root.crt
```
## server実装
* proto/server.py
    * サーバの秘密キー(privkey.pem), 証明書チェイン(cert.prm)からcredentialを作成
    * serverにcredentialから構成されるsecure_portを追加
```buildoutcfg
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
simple_pb2_grpc.add_SimpleServiceServicer_to_server(SimpleServiceServicer(), server)
pkey = open("../certs/privkey.pem", "rb").read()
chain = open("../certs/cert.pem", "rb").read()
cred = grpc.ssl_server_credentials([(pkey, chain)])
server.add_secure_port('localhost:51011', cred)
server.start()
```

## client実装
* proto/clientpy
    * ルート証明書(root.crt)を開く
    * root_certificatesにルート証明書を指定したcredentialを生成
    * secure_channelを開く
```buildoutcfg
root = open("../certs/root.crt", "rb").read()
cred = grpc.ssl_channel_credentials(root_certificates=root)

with grpc.secure_channel("localhost:51011", cred) as channel:
    stub = simple_pb2_grpc.SimpleServiceStub(channel)
```

## 動作確認
1. server起動
```buildoutcfg
/Users/thetsuthetsu/PycharmProjects/gRPCSample1/venv/bin/python /Users/thetsuthetsu/PycharmProjects/gRPCSample1/proto/server.py
run server
```
2. client起動
```buildoutcfg
/Users/thetsuthetsu/PycharmProjects/gRPCSample1/venv/bin/python /Users/thetsuthetsu/PycharmProjects/gRPCSample1/proto/client.py
Reply:  Hello! Tom. Your message is Test
Reply:  ['message1', 'message2']
Reply:  {'key1': 'hogehoge'}

Process finished with exit code 0
```