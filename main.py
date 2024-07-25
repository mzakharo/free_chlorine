import json
import paho.mqtt.client as paho
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import sys
import tflite_runtime.interpreter as tflite
import numpy as np

broker = 'nas.home.arpa'
fmodel = 'model_fc.tflite'


interpreter = tflite.Interpreter(model_path=fmodel)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()
    

def on_connect( client, userdata, flags, rc):
    print("MQTT connected with result code "+str(rc))
    client.subscribe("zigbee2mqtt/Pool")


def on_message(client, userdata, msg):
    print(msg.payload)
    payload = json.loads(msg.payload)
    orp = payload['orp']
    ph = payload['ph']
    input_data = np.array([[orp,ph]], dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    fc = interpreter.get_tensor(output_details[0]['index'])[0][0]
    print(orp, ph, fc)
    client.publish("Pool/free_chlorine", str(fc))


client = paho.Client()
client.connect(broker)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
