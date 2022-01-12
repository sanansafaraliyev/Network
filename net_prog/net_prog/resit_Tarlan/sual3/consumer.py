import zmq
import random
import json

def consumer():
    consumer_id = random.randrange(1,4)
    print(f"I am consumer {consumer_id}")

    context = zmq.Context()

    #recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5555")

    #send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.bind("tcp://127.0.0.1:5556")

    while True:
        result = {}

        work = consumer_receiver.recv_json()
        data = work['part']
        for item in data:
            result[item] = data.count(item)
        
        #print(result)
        consumer_sender.send_json(result)

consumer()
