from timer import Timer
from config import TIMEOUT_SENDER, VERBOSE
from copy import deepcopy


class Sender:
    def __init__(self):
        self.timer = Timer()
        self.can_send = True
        self.n_s = 0
        self.incoming_data = list()
        self.incoming_ack = list()
        self.outgoing_frames = list()
        self.stored_frames = dict()

    def log(self, *args, **kwargs):
        if VERBOSE:
            print("Sender:\t\t", *args, **kwargs)

    def flip(self, n):
        return 0 if n == 1 else 1

    def make_frame(self, data):
        frame = [1, self.n_s, data]
        return frame

    def store_frame(self, frame):
        self.stored_frames[self.n_s] = frame

    def purge_frame(self, index):
        self.stored_frames.pop(index)

    def is_corrupted(self, frame):
        return frame[0] == 0

    def tick(self):
        self.log(f"tick n_s = {self.n_s}")
        # Sending frame
        if self.can_send == True:
            if len(self.incoming_data) > 0:
                self.log("Going to send")
                data = self.incoming_data.pop(0)
                self.log("Read incoming data item")
                self.send_frame(data)
                self.log("Send frame with data")
            else:
                self.log("\033[96mALL DATA SENT\033[00m")

        # Receiving ACK
        elif len(self.incoming_ack) > 0:
            self.log("Received ACK")
            ack = self.incoming_ack.pop(0)
            self.receive_ack(ack)

        # Expired timer
        elif self.timer.get() >= TIMEOUT_SENDER:
            self.log("Timer expired, going to resend frame")
            self.resend_frame()

        # Updating timer
        self.timer.tick()

    def send_frame(self, data):
        frame = self.make_frame(data)
        self.store_frame(deepcopy(frame))
        self.outgoing_frames.append(frame)
        self.timer.start()
        self.can_send = False

    def resend_frame(self):
        self.timer.stop()
        frame = deepcopy(self.stored_frames[self.n_s])
        self.outgoing_frames.append(frame)
        self.timer.start()

    def receive_ack(self, ack):
        if (ack[1] == self.flip(self.n_s)) and (not self.is_corrupted(ack)):
            self.log("\033[92mReceived ACK is valid\033[00m")
            self.timer.stop()
            self.purge_frame(index=self.n_s)
            self.n_s = self.flip(self.n_s)
            self.can_send = True
        else:
            self.log(
                f"\033[91mReceived ACK invalid (n_s = {self.n_s}; n_r = {ack[1]}) \033[00m"
            )
