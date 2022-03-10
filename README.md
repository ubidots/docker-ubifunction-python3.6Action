# Docker-UbiFunction-python3.6Action

Base Docker to execute UbiFunction python3.6 actions. Based on the original IBM Openwhisk action runner: https://github.com/ibm-functions/runtime-python.

The runtime is based on python3.6, older and newer versions are not supported.

## Supported Libraries

Default Python packages supported by the container

### Setup modules

- gevent == 21.1.1
- flask == 1.1.2

### Default available packages for python3action

- beautifulsoup4 == 4.9.3
- httplib2 == 0.19.0
- lxml == 4.6.2
- python-dateutil == 2.8.1
- requests == 2.25.1
- scrapy == 2.4.1
- simplejson == 3.17.2
- twisted == 20.3.0
- paho-mqtt == 1.5.1
- pynt==0.8.2
- pytz == 2020.5

### Packages for numerics

- numpy == 1.19.5
- scikit-learn == 0.24.0
- scipy == 1.5.4
- pandas == 1.1.5
- matplotlib == 3.3.3
- fbprophet == 0.7.1
- arrow == 0.17

### Packages for image processing

- Pillow == 8.1.0
- pytesseract == 0.3.7

### Compose Libs

- psycopg2 == 2.8.6
- pymongo==3.11.3
- pymongo[srv]==3.11.3
- redis == 3.5.3
- pika == 1.1.0
- elasticsearch == 7.10.1
- etcd3 == 0.12.0

### Notification Packages

- sentry-sdk==0.19.5

### AWS specific modules

- boto3==1.16.56
- botocore==1.19.56

### Google Modules

- google-api-core == 1.30.0
- dialogflow == 1.1.0

### Crypto module

- cryptography==3.3.2

### 3rd party API management

- zeep==4.0.0
- pyodbc==4.0.30
- python-aqi==0.6.1
- lunarcalendar==0.0.9
- convertdate==2.2.0
- holidays==0.10.4
- tqdm==4.56.0
- pystan==2.19.1.1
- firebase-admin==4.5.1
- google-api-python-client==2.39.0
- google-auth-httplib2==0.1.0
- google-auth-oauthlib==0.5.0

## Examples

### Hello Action

Write a simple function and save it as hello.py

```py
def main(args):
    name = args.get("name", "stranger")
    greeting = "Hello " + name + "!"
    print(greeting)
    return {"greeting": greeting}
```

#### IBM Cloud Functions (based on Apache OpenWhisk)

To use as a python kind action

```
ibmcloud wsk action create helloPython hello.py --kind python:3.6
```

Invoke the action

```
ibmcloud wsk action invoke helloPython
```

#### How to use as a docker Action locally

To use as a docker action based on this container

```
ibmcloud wsk action update helloPython hello.py --docker ubidots/docker-ubifunction-python3.6action
```
