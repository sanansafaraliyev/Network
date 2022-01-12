import time
import zmq
import random

def mapper():
	mapper_id = random.randrange(1, 10005)
	print(f"I am consumer {mapper_id}")

	context = zmq.Context()
	# receive work
	mapper_receiver = context.socket(zmq.PULL)
	mapper_receiver.connect("tcp://127.0.0.1:5557")

	# send work
	mapper_sender = context.socket(zmq.PUSH)
	mapper_sender.connect("tcp://127.0.0.1:5558")

	while True:
		work = mapper_receiver.recv_json()
		result = {"mapper": mapper_id, "data": data}

		mapper_sender.send_json(result)

mapper()