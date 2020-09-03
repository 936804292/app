`Kezhi OpcUA Server`
---
##install	
```shell script
pip3 install cryptography
openssl req -x509 -newkey rsa:2048 -keyout kz_private_key.pem -out kz_cert.pem -days 355 -nodes -config ssl.conf
openssl x509 -outform der -in kz_cert.pem -out kz_cert.der
```
##CA json

```json
"security_num": {
    "NoSecurity": "0",
    "Basic256Sha256_SignAndEncrypt": "1",
    "Basic256Sha256_Sign": "2"
}
```


