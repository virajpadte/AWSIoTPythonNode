This is a simple python node which connects to AWS IoT broker and sends data to on a specified topic.
The data source is a simple json file which is supplied as a command line argument.

The program is also specified with a transmit duration which is used to simulate real-time behavior.

This program will be hosted on a EC2 instance and the json data file will be stored on the same instance.