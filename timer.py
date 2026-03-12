import tkinter as tk
import time

TOTAL_TIME = 600  # 10 minutes


class ChessClock:

    def __init__(self, root):

        self.root = root
        self.root.title("Dual Timer Clock")
        self.root.attributes("-fullscreen", True)

        self.white_time = TOTAL_TIME
        self.black_time = TOTAL_TIME

        self.turn = "white"
        self.running = False
        self.last = time.time()

        # Layout
        self.white_frame = tk.Frame(root, bg="white")
        self.white_frame.pack(side="left", fill="both", expand=True)

        self.black_frame = tk.Frame(root, bg="grey")
        self.black_frame.pack(side="right", fill="both", expand=True)

        self.white_label = tk.Label(
            self.white_frame,
            text=self.format_time(self.white_time),
            font=("Arial", 120),
            bg="white",
            fg="black"
        )
        self.white_label.pack(expand=True)

        self.black_label = tk.Label(
            self.black_frame,
            text=self.format_time(self.black_time),
            font=("Arial", 120),
            bg="grey",
            fg="white"
        )
        self.black_label.pack(expand=True)

        # Click anywhere on panels
        self.white_frame.bind("<Button-1>", self.white_press)
        self.black_frame.bind("<Button-1>", self.black_press)

        # Spacebar switch
        self.root.bind("<space>", self.switch)

        self.update_clock()

    def format_time(self, seconds):
        seconds = int(seconds)
        m = seconds // 60
        s = seconds % 60
        return f"{m:02}:{s:02}"

    def white_press(self, event):
        if not self.running:
            self.running = True
            self.turn = "white"
            self.last = time.time()
        elif self.turn == "white":
            self.turn = "black"
            self.last = time.time()

    def black_press(self, event):
        if self.turn == "black":
            self.turn = "white"
            self.last = time.time()

    def switch(self, event):
        if not self.running:
            self.running = True
            self.turn = "white"
            self.last = time.time()
        else:
            self.turn = "black" if self.turn == "white" else "white"
            self.last = time.time()

    def update_clock(self):

        if self.running:

            now = time.time()
            elapsed = now - self.last
            self.last = now

            if self.turn == "white":
                self.white_time -= elapsed
                if self.white_time <= 0:
                    self.white_time = 0
                    self.running = False

            else:
                self.black_time -= elapsed
                if self.black_time <= 0:
                    self.black_time = 0
                    self.running = False

        self.white_label.config(text=self.format_time(self.white_time))
        self.black_label.config(text=self.format_time(self.black_time))

        self.root.after(1000, self.update_clock)


root = tk.Tk()
app = ChessClock(root)
root.mainloop()