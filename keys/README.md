All the key material in this directory is intended for private demonstration purposes only
and should be regarded as insecure.

To generate keys:
```
openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=webhook.webhook.svc" -out server.csr
openssl x509 -req -extfile <(printf "subjectAltName=DNS:webhook.webhook.svc") -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
```
