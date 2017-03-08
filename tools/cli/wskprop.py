#!/usr/bin/env python

#
# Copyright 2015-2016 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

##
# Helper methods for whisk properties
##

import os
import pkg_resources

WHISK_VERSION_DATE = 'WHISK_VERSION_DATE'
CLI_API_HOST = 'CLI_API_HOST'


def propfile(base):
    if base != '':
        filename = '%s/whisk.properties' % base
        if os.path.isfile(filename) and os.path.exists(filename):
            return filename
        else:
            parent = os.path.dirname(base)
            return propfile(parent) if parent != base else ''
    else:
        return ''


def importPropsIfAvailable(filename):
    thefile = open(filename, 'r') if (os.path.isfile(filename) and
                                      os.path.exists(filename)) else []
    return importProps(thefile)


def importDefaultProps():
    packagename = 'whisk'
    filename = 'default.props'
    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            filename)
    theFile = open(filepath, 'r') if (os.path.isfile(filepath) and
                                      os.path.exists(filepath)) else None
    if not theFile:
        try:
            theFile = pkg_resources.resource_stream(packagename, filename)
        except ImportError:
            theFile = None
    return importProps(theFile) if theFile else None


def importProps(stream):
    return {key.strip().upper().replace('.', '_'): val.strip()
            for key, _, val in (line.partition('=') for line in stream)
            if key.strip()}


def updateProps(key, value, filename):
    userProps = importPropsIfAvailable(filename)
    userProps[key] = value
    writeProps(userProps, filename)


def writeProps(props, filename):
    with open(filename, 'w') as fileHandle:
        for key, val in props.items():
            fileHandle.write(key.upper() + '=' + val + '\n')


#
# Returns a triple of (length(requiredProperties), requiredProperties,
# deferredInfo)  Prints a message if a required property is not found
def checkRequiredProperties(requiredPropertiesByName, properties):
    requiredPropertiesByValue = [getPropertyValue(key, properties) for key
                                 in requiredPropertiesByName]
    requiredProperties = dict(zip(requiredPropertiesByName,
                                  requiredPropertiesByValue))
    invalidProperties = [key for key in requiredPropertiesByName
                         if requiredProperties[key] is None]
    deferredInfo = ''
    for key, value in requiredProperties.items():
        if not value:
            print('property "%s" not found in environment or property file' %
                  key)
        else:
            deferredInfo += 'using %(key)s = %(value)s\n' % {'key': key,
                                                             'value': value}
    return (len(invalidProperties) == 0, requiredProperties, deferredInfo)


def getPropertyValue(key, properties):
    return os.environ.get(key) or properties.get(key)


def merge(props1, props2):
    props = props1.copy()
    props.update(props2)
    return props
