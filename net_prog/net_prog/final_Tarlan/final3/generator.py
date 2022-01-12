import time
import zmq
import pickle

def generator():
	context = zmq.Context()
	zmq_socket = context.socket(zmq.PUSH)
	zmq_socket.bind("tcp://127.0.0.1:5557")

	part1 = []
	part2 = []
	part3 = []

	with open('BagOfWords.txt', 'r') as reader:
		count = 0
    	line = reader.readline()
    	while line != '':
        	print(line, end='')
        	count += 1
        	line = reader.readline()
        	

    data_to_send = pickle.dump(data)
    context.send(data_to_send)


generator()