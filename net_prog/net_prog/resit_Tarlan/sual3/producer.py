import zmq
import json

def producer():
    context  = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5555")
    result_receiver = context.socket(zmq.PULL)
    result_receiver.connect("tcp://127.0.0.1:5557")

    part1 = []
    part2 = []

    with open("BagOfWords.txt", "r") as reader:
        total_lines = len(reader.readlines())

    with open("BagOfWords.txt", "r") as reader:
        line_counter = 0
        #character_count = 0
        line = reader.readline()

        while line != '':
            if line_counter <= total_lines/2:
                part1.append(line)
            else:
                part2.append(line)

            line_counter += 1
            line = reader.readline()

    for part in [part1, part2]:
        work_message = {'part':part}
        zmq_socket.send_json(work_message)

    print("PART 1")
    print(part1)
    print('')
    print("PART 2")
    print(part2)
    print('')

    #receive
    data_received = result_receiver.recv_json()
    print("RESULT: ")
    for item, count in data_received.items():
        print(f"{item} -> {count}")
    

producer()
