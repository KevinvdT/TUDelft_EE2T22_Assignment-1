from timer import Timer
from config import TIMEOUT_RECEIVER, VERBOSE


class Receiver:
    def __init__(self):
        self.timer = Timer()
        self.incoming_frames = list()
        self.outgoing_ack = list()
        self.received_data = list()
        self.n_r = 0

    def log(self, *args, **kwargs):
        if VERBOSE:
            print("Receiver:\t", *args, **kwargs)

    def is_corrupted(self, frame):
        return frame[0] == 0

    def tick(self):
        if len(self.incoming_frames) > 0:
            frame = self.incoming_frames.pop(0)
            self.log(f"Incoming frame {frame}")
            if (not self.is_corrupted(frame)) and (frame[1] == self.n_r):
                self.log("\033[92mIncoming frame is valid\033[00m")
                self.receive_frame(frame)
                self.send_ack()
            else:
                self.log(
                    "\033[91mFrame is corrupted or invalid seq. no., passing \033[00m"
                )

        self.timer.tick()
        self.log(f"tick n_r = {self.n_r}")

    def receive_frame(self, frame):
        data = frame[2]
        self.received_data.append(data)
        # Flip n_r (mod 2 artihmetic)
        self.n_r = 1 if self.n_r == 0 else 0
        # self.n_r += 1
        self.log(f"Data ({data}) from frame {frame} added to received data")

    def send_ack(self):
        ack = [1, self.n_r, 0]
        self.outgoing_ack.append(ack)
        self.log(f"Send ACK for n_r = {self.n_r}")
