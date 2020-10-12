# OpcUA Server of Kezhi
---
## Signature Certificate	
```shell script
pip3 install cryptography
openssl req -x509 -newkey rsa:2048 -keyout kz_private_key.pem -out kz_cert.pem -days 355 -nodes -config ssl.conf
openssl x509 -outform der -in kz_cert.pem -out kz_cert.der
```
---
## Set Project Configuration
``` shell script
Config:
vim ./config/config.json

Node:节点是根据json数据格式设置的，需要事先知道DB模块的字段，然后写入json文件中。
vim ./config/data0.json

Build docker image:第二种image小，layer层少，比较精简，之前我配置ok的，建议用第二种;

(1)docker build -t kezhi/da2ua:v1 .

(2)docker pull laoweisir/kezhi:latest
   docker build -t kezhi/da2ua:v1 .
```
---
## Start the Project

```python
python3 app.py
```
