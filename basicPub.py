'''
/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

Note: This is an acknowledgement that the following code is a modification the basicPubSub sample available for testing
aws-iot-python sdk.
The original version can be obtained at https://github.com/aws/aws-iot-device-sdk-python.

changes made:
1] Added command line options to specify clientID,topicName.
(this is just to make the code more generic)

2] The subscribe function is not called as I just need to publish data at specific time intervals to
   simulate a real device transmitting data.


 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import json
from pprint import pprint


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


#retriving message attributes from saved measurement data:

def getattributes(data_file, index):
    data = json.load(data_file)
    DataID = str(index)
    Reading = str(data["data"][index][12])
    Cost = str(data["data"][index][13])
    Month = str(data["data"][index][15])
    if len(Month) == 1:
        Month = "0"+Month
    Year = str(data["data"][index][16])
    CreatedAt = Year+"-"+Month+"-"+"01"
    Place = data["data"][index][9]
    return DataID,CreatedAt,Reading,Cost,Place

#Generating message from meassage attributes:
def getPayload(index, filename, clientID):
    with open(filename) as data_file:
        DataID,CreatedAt,Reading,Cost,Location = getattributes(data_file, index)
        jsonPayload = json.dumps({'NodeID': clientID, 'DataID': DataID, 'CreatedAt': CreatedAt, 'Reading': Reading, 'Cost': Cost, "Place": Location})
        return jsonPayload

def usageNConfig():
    ##  Usage
    usageInfo = """Usage:

	Use certificate based mutual authentication:
	python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath> -t <topicname> -cl <clientID> -f <fileName>

	Type "python basicPubSub.py -h" for available options.
	"""
    # Help info
    helpInfo = """-e, --endpoint
		Your AWS IoT custom endpoint
	-r, --rootCA
		Root CA file path
	-c, --cert
		Certificate file path
	-k, --key
		Private key file path
	-t, --topicName
		Use to specify the topic to be used for publishing or subscribing
	-cl, --clientID
		Use to specify the clientID to be used for publishing or subscribing
	-f, --fileName
	-h, --help
		Help information


	"""

    # Read in command-line parameters
    useWebsocket = False
    host = ""
    rootCAPath = ""
    certificatePath = ""
    privateKeyPath = ""
    topicName = ""
    clientID = ""
    fileName = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:t:i:f:", ["help", "endpoint=", "key=","cert=","rootCA=", "topicName=", "clientID=", "fileName=","websocket"])
        if len(opts) == 0:
            raise getopt.GetoptError("No input parameters!")
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(helpInfo)
                exit(0)
            if opt in ("-e", "--endpoint"):
                host = arg
            if opt in ("-r", "--rootCA"):
                rootCAPath = arg
            if opt in ("-c", "--cert"):
                certificatePath = arg
            if opt in ("-k", "--key"):
                privateKeyPath = arg
            if opt in ("-w", "--websocket"):
                useWebsocket = True
            if opt in ("-t", "--topicName"):
                topicName = arg
            if opt in ("-i", "--clientID"):
                clientID = arg
            if opt in ("-f", "--fileName"):
                fileName = arg
                print ("fileName: ", fileName)
    except getopt.GetoptError:
        print(usageInfo)
        exit(1)

    # Missing configuration notification
    missingConfiguration = False
    if not host:
        print("Missing '-e' or '--endpoint'")
        missingConfiguration = True
    if not rootCAPath:
        print("Missing '-r' or '--rootCA'")
        missingConfiguration = True
    if not topicName:
        print("Missing '-t' or '--topicName'")
        missingConfiguration = True
    if not clientID:
        print("Missing '-i' or '--clientID'")
        missingConfiguration = True
    if not fileName:
        print("Missing '-f' or '--fileName'")
        missingConfiguration = True
    if not useWebsocket:
        if not certificatePath:
            print("Missing '-c' or '--cert'")
            missingConfiguration = True
        if not privateKeyPath:
            print("Missing '-k' or '--key'")
            missingConfiguration = True
    if missingConfiguration:
        exit(2)

    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    logger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTClient
    myAWSIoTMQTTClient = None
    if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID, useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, 443)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
    else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient(clientID)
        myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    return myAWSIoTMQTTClient,topicName, fileName, clientID

def transmit(mqttclient,topic, datafile, clientID):
    # Connect and subscribe to AWS IoT
    mqttclient.connect()
    #myAWSIoTMQTTClient.subscribe("energy/SNode1_1", 1, customCallback)
    time.sleep(2)
    # Publish to the same topic in a loop forever
    loopCount = 0
    while loopCount<289:
        mqttclient.publish(topic, getPayload(loopCount, datafile, clientID), 1)
        loopCount += 1
        time.sleep(1)
    #myAWSIoTMQTTClient.unsubscribe("energy/SNode1_1")
    print("published")
    mqttclient.disconnect()


def main():
    mqttclient,topic, datafile, clientID = usageNConfig()
    transmit(mqttclient,topic, datafile, clientID)
if __name__ == "__main__": main()


