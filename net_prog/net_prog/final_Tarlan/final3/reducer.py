import time
import zmq

def reducer():
	context = zmq.Context()
	reducer_receiver = context.socket(zmq.PULL)
	reducer_receiver.bind("tcp://127.0.0.1:5558")


	reducer_sender = context.socket(zmq.PULL)
	reducer_sender.bind("tcp://127.0.0.1:5557")

	collector_data = {}

	for x in range(1000):
		result = results_receiver.recv_json()
		print(collector_data)

	reducer_sender.send_json()

reducer()	