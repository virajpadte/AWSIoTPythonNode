This is a simple python node which connects to AWS IoT broker and sends data to on a specified topic.
The data source is a simple json file which is supplied as a command line argument.

The program is also specified with a transmit duration which is used to simulate real-time behavior.

This program will be hosted on a EC2 instance and the json data file will be stored on the same instance.

Note: This is an acknowledgement that the following code is a modification the basicPubSub sample available for testing
aws-iot-python sdk.</br>
The original version can be obtained at https://github.com/aws/aws-iot-device-sdk-python.</br>
changes made:</br>
1] Added command line options to specify clientID,topicName.
(this is just to make the code more generic)</br>
2] The subscribe function is not called as I just need to publish data at specific time intervals to
   simulate a real device transmitting data.


Notice: This repo is a part of a bigger project which also involves an IoT dashboard app created for iPhones. 
Need access to the app source code?</br>
https://github.com/virajpadte/awsIoTAppDashBoard

If you are   interested in knowing more about the entire project archicture, visit this link:</br>
page is under-construction
