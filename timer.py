class Timer:
    def __init__(self):
        self.timestamp = 0
        self.timer_on = False

    def start(self):
        self.timestamp = 0
        self.timer_on = True

    def stop(self):
        self.timestamp = 0
        self.timer_on = False

    def get(self):
        return self.timestamp

    def tick(self):
        if self.timer_on:
            self.timestamp += 1
