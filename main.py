from sender import Sender
from receiver import Receiver
from timer import Timer
from config import (
    PROPAGATION_TIME,
    VERBOSE,
)
from time import sleep
from random import random, randint
from copy import deepcopy


def log(*args, **kwargs):
    if VERBOSE:
        print("Main:\t\t", *args, **kwargs)


def generate_data(length):
    return [randint(0, 2**8 - 1) for i in range(length)]


def run_experiment(data, p_1, p_2):
    sender_to_receiver_line = list()
    receiver_to_sender_line = list()

    sender = Sender()
    receiver = Receiver()

    data_to_send = deepcopy(data)
    sender.incoming_data = deepcopy(data_to_send)

    iteration = 0

    while receiver.received_data != data_to_send:
        iteration += 1
        # print(f"Iteration {iteration}")
        if VERBOSE:
            print()  # New line
        log(f"Tick, iteration {iteration}\tn_s = {sender.n_s}\t\tn_r = {receiver.n_r}")

        ## Sender -> Receiver ##
        # Update propagation timers
        for index, item in enumerate(sender_to_receiver_line):
            item["timer"].tick()
            if item["timer"].get() >= PROPAGATION_TIME - 1:
                sender_to_receiver_line.pop(index)
                receiver.incoming_frames.append(item["frame"])
                log(
                    f'Moved frame {item["frame"]} from sender_to_receiver_line to receiver.incoming_frames'
                )

        # If there are outgoing frames
        if len(sender.outgoing_frames) > 0:
            frame = deepcopy(sender.outgoing_frames.pop(0))
            if random() <= p_1:
                frame[0] = 0
                log("\033[48:5:208mFrame got corrupted\033[m\n")
            propagaiton_timer = Timer()
            sender_to_receiver_line.append({"timer": propagaiton_timer, "frame": frame})
            propagaiton_timer.start()
            log(f"Added frame {frame} to sender_to_receiver_line")

        ## Receiver -> Sender ##
        # Update propagation timers
        for index, item in enumerate(receiver_to_sender_line):
            item["timer"].tick()
            if item["timer"].get() >= PROPAGATION_TIME - 1:
                receiver_to_sender_line.pop(index)
                sender.incoming_ack.append(item["ack"])
                log(f"Moved ACK from receiver_to_sender_line to sender.incoming_ack")
        # If there are outgoing ACK
        if len(receiver.outgoing_ack) > 0:
            ack = deepcopy(receiver.outgoing_ack.pop(0))
            if random() <= p_2:
                log("\033[48:5:208mACK got corrupted\033[m\n")
                ack[0] = 0
            propagaiton_timer = Timer()
            receiver_to_sender_line.append({"timer": propagaiton_timer, "ack": ack})
            propagaiton_timer.start()
            log(f"Added ACK to receiver_to_sender_line")

        sender.tick()
        receiver.tick()
        if VERBOSE:
            sleep(0.1)

    log(
        f"\033[92mData transfer finished\tno. iterations = {iteration}\t received data = {receiver.received_data}\033[00m"
    )
    return {"iterations": iteration, "received_data": receiver.received_data}


if __name__ == "__main__":
    p_1 = 0
    p_2 = 0.5
    data = [randint(0, 2**8 - 1) for i in range(20)]
    result = run_experiment(data, p_1, p_2)
    print(
        f'Iterations = {result["iterations"]}\t received_data = {result["received_data"]}'
    )
