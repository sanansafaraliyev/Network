import zmq

def result_collector():
    context = zmq.Context()

    collector_receiver = context.socket(zmq.PULL)
    collector_receiver.connect("tcp://127.0.0.1:5556")


    collector_sender = context.socket(zmq.PUSH)
    collector_sender.bind("tcp://127.0.0.1:5557")

    collector_data = {}

    dict1 = collector_receiver.recv_json()
    dict2 = collector_receiver.recv_json()

    for key in dict1:
        if key in dict2:
            collector_data[key] = dict1[key] + dict2[key]
        else:
            collector_data[key] = dict1[key]   
    for key in dict2:
        if key not in dict1:
            collector_data[key] = dict2[key]

    print(collector_data)

    collector_sender.send_json(collector_data)


result_collector()