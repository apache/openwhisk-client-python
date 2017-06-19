# incubator-openwhisk-client-python
[![Build Status](https://api.travis-ci.org/apache/incubator-openwhisk-client-python.svg?branch=master)](https://api.travis-ci.org/apache/incubator-openwhisk-client-python)

There is no official Python client for Apache OpenWhisk at the moment. However, the REST API of OpenWhisk can be used directly from Python. Here is an example of Python code using the `requests` library to invoke `echo` action in OpenWhisk (using IBM's Bluemix as a target host):

``` python
import subprocess
import requests

APIHOST = 'https://openwhisk.ng.bluemix.net'
AUTH_KEY = subprocess.check_output("wsk property get --auth", shell=True).split()[2] 
NAMESPACE = 'whisk.system'
ACTION = 'utils/echo'
PARAMS = {'myKey':'myValue'}
BLOCKING = 'true'
RESULT = 'true'

url = APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
user_pass = AUTH_KEY.split(':')
response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
print(response.text)
```
Swagger documentation for full API is available [here](http://petstore.swagger.io/?url=https://raw.githubusercontent.com/apache/incubator-openwhisk/master/core/controller/src/main/resources/apiv1swagger.json).

There is an [open issue](apache/incubator-openwhisk#450) to create a Python client library to make this easier.

NOTE: This repository used to comprise an OpenWhisk CLI written in Python. The CLI has been [superseded by a version written in Go](https://github.com/apache/incubator-openwhisk-cli).
