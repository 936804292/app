# OpcUA Server of Kezhi
---
## install of CA	
```shell script
pip3 install cryptography
openssl req -x509 -newkey rsa:2048 -keyout kz_private_key.pem -out kz_cert.pem -days 355 -nodes -config ssl.conf
openssl x509 -outform der -in kz_cert.pem -out kz_cert.der
```
---
## .
### Set Project Configuration
``` shell script
'config:'
vim ./config/config.json
'node:'
vim ./config/data.json
'build docker image:'
docker build kezhi/da2ua:v1 .
```
---
## Start the project
```python
python3 app.py
```
