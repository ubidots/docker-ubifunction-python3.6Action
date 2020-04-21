# Docker-UbiFunction-python3.6Action
Base Docker to execute UbiFunction python3.6 actions. Based on the original IBM Openwhisk action runner: https://github.com/ibm-functions/runtime-python.

The runtime is based on python3.6, older and newer versions are not supported.

## Supported Libraries

Default Python packages supported by the container

**Setup modules**
- gevent == 1.4.0
- flask == 1.0.2

**default available packages for python3action**
- beautifulsoup4 == 4.8.0
- httplib2 == 0.13.0
- kafka_python == 1.4.6
- lxml == 4.3.4
- python-dateutil == 2.8.0
- requests == 2.22.0
- scrapy == 1.6.0
- simplejson == 3.16.0
- virtualenv == 16.7.1
- twisted == 20.3.0
- paho-mqtt == 1.4.0

**packages for numerics**
- numpy == 1.16.4
- scikit-learn == 0.20.3
- scipy == 1.2.1
- pandas == 0.24.2

**packages for image processing**
- Pillow == 6.0.0

**IBM specific python modules**
- ibm_db == 3.0.1
- cloudant == 2.12.0
- watson-developer-cloud == 2.8.1
- ibm-cos-sdk == 2.5.1
- ibmcloudsql == 0.2.23

**Compose Libs**
- psycopg2 == 2.8.2
- pymongo == 3.8.0
- redis == 3.2.1
- pika == 1.0.1
- elasticsearch == 6.3.1
- cassandra-driver == 3.18.0
- etcd3 == 0.10.0

**AWS specific modules**
- boto3==1.10.29
- botocore==1.13.29

**Crypto modules**
cryptography==2.9.1


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
