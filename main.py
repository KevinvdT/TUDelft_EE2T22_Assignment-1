from sender import Sender
from receiver import Receiver
from timer import Timer
from config import PROPAGATION_TIME, VERBOSE
from time import sleep


def log(*args, **kwargs):
    print("Main:\t\t", *args, **kwargs)


def get_data():
    return [1, 2, 3, 4, 5]


sender_to_receiver_line = list()
receiver_to_sender_line = list()


def main():
    sender = Sender()
    receiver = Receiver()

    sender = Sender(verbose=True)
    sender.incoming_data = get_data()

    iteration = 1

    while True:
        if VERBOSE:
            print()  # New line
        log(f"tick, iteration {iteration}\tn_s = {sender.n_s}\t\tn_r = {receiver.n_r}")

        ## Sender -> Receiver ##
        # Update propagation timers
        for index, item in enumerate(sender_to_receiver_line):
            item["timer"].tick()
            if item["timer"].get() >= PROPAGATION_TIME:
                sender_to_receiver_line.pop(index)
                receiver.incoming_frames.append(item["frame"])
                log(
                    f'Moved frame {item["frame"]} from sender_to_receiver_line to receiver.incoming_frames'
                )

        # If there are outgoing frames
        if len(sender.outgoing_frames) > 0:
            frame = sender.outgoing_frames.pop(0)
            propagaiton_timer = Timer()
            sender_to_receiver_line.append({"timer": propagaiton_timer, "frame": frame})
            propagaiton_timer.start()
            log(f"Added frame {frame} to sender_to_receiver_line")

        ## Receiver -> Sender ##
        # Update propagation timers
        for index, item in enumerate(receiver_to_sender_line):
            item["timer"].tick()
            if item["timer"].get() >= PROPAGATION_TIME:
                receiver_to_sender_line.pop(index)
                sender.incoming_ack.append(item["frame"])
                log(f"Moved ACK from receiver_to_sender_line to sender.incoming_ack")
        # If there are outgoing ACK
        if len(receiver.outgoing_ack) > 0:
            ack = receiver.outgoing_ack.pop(0)
            propagaiton_timer = Timer()
            receiver_to_sender_line.append({"timer": propagaiton_timer, "frame": frame})
            propagaiton_timer.start()
            log(f"Added ACK to receiver_to_sender_line")

        sender.tick()
        receiver.tick()
        iteration += 1
        if VERBOSE:
            sleep(0.5)


if __name__ == "__main__":
    main()
