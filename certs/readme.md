# 秘密鍵と公開鍵を作成
```
$ openssl req -x509 -nodes -newkey rsa:2048 -days 365 -keyout privkey.pem -out cert.pem -subj "/CN=localhost"
```

# 公開鍵でroot証明書を作る
```
$ openssl  x509 -in cert.pem -out root.crt
```