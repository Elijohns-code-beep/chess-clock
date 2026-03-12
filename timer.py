import tkinter as tk
import time

TOTAL_TIME = 600      # 10 minutes
INCREMENT = 5         # seconds added per move
LOW_TIME_WARNING = 30 # seconds


class ChessClock:

    def __init__(self, root):

        self.root = root
        self.root.title("Professional Chess Clock")
        self.root.attributes("-fullscreen", True)

        self.white_time = TOTAL_TIME
        self.grey_time = TOTAL_TIME

        self.turn = None
        self.running = False
        self.last = time.time()

        # Frames
        self.white_frame = tk.Frame(root, bg="white", highlightthickness=8)
        self.white_frame.pack(side="left", fill="both", expand=True)

        self.grey_frame = tk.Frame(root, bg="grey", highlightthickness=8)
        self.grey_frame.pack(side="right", fill="both", expand=True)

        # Timer Labels
        self.white_label = tk.Label(
            self.white_frame,
            text=self.format_time(self.white_time),
            font=("Consolas", 150, "bold"),
            bg="white",
            fg="black"
        )
        self.white_label.pack(expand=True)

        self.grey_label = tk.Label(
            self.grey_frame,
            text=self.format_time(self.grey_time),
            font=("Consolas", 150, "bold"),
            bg="grey",
            fg="white"
        )
        self.grey_label.pack(expand=True)

        # Status label
        self.status = tk.Label(
            root,
            text="Press SPACE or click a side to start",
            font=("Arial", 20),
            bg="black",
            fg="white"
        )
        self.status.place(relx=0.5, rely=0.95, anchor="center")

        # Click bindings
        self.white_frame.bind("<Button-1>", self.white_press)
        self.grey_frame.bind("<Button-1>", self.grey_press)

        # Keyboard bindings
        root.bind("<space>", self.switch)
        root.bind("r", self.reset)
        root.bind("f", self.toggle_fullscreen)
        root.bind("<Escape>", lambda e: root.destroy())

        self.update_clock()

    def format_time(self, seconds):
        seconds = int(seconds)
        m = seconds // 60
        s = seconds % 60
        return f"{m:02}:{s:02}"

    def beep(self):
        self.root.bell()

    def highlight(self):

        if self.turn == "white":
            self.white_frame.config(highlightbackground="green")
            self.grey_frame.config(highlightbackground="black")
        elif self.turn == "grey":
            self.grey_frame.config(highlightbackground="green")
            self.white_frame.config(highlightbackground="black")

    def white_press(self, event=None):

        if not self.running:
            self.running = True
            self.turn = "white"
            self.last = time.time()
            self.status.config(text="White running")
            self.highlight()
            return

        if self.turn == "white":
            self.white_time += INCREMENT
            self.turn = "grey"
            self.last = time.time()
            self.status.config(text="Grey running")
            self.highlight()
            self.beep()

    def grey_press(self, event=None):

        if self.turn == "grey":
            self.grey_time += INCREMENT
            self.turn = "white"
            self.last = time.time()
            self.status.config(text="White running")
            self.highlight()
            self.beep()

    def switch(self, event=None):

        if not self.running:
            self.white_press()
            return

        if self.turn == "white":
            self.white_press()
        else:
            self.grey_press()

    def update_clock(self):

        if self.running:

            now = time.time()
            elapsed = now - self.last
            self.last = now

            if self.turn == "white":
                self.white_time -= elapsed
                if self.white_time <= 0:
                    self.white_time = 0
                    self.game_over("Grey wins on time")

            elif self.turn == "grey":
                self.grey_time -= elapsed
                if self.grey_time <= 0:
                    self.grey_time = 0
                    self.game_over("White wins on time")

        self.update_display()

        self.root.after(200, self.update_clock)

    def update_display(self):

        self.white_label.config(text=self.format_time(self.white_time))
        self.grey_label.config(text=self.format_time(self.grey_time))

        # low time warning
        if self.white_time < LOW_TIME_WARNING:
            self.white_label.config(fg="red")

        if self.grey_time < LOW_TIME_WARNING:
            self.grey_label.config(fg="red")

    def game_over(self, message):

        self.running = False
        self.status.config(text=message)
        self.beep()

    def reset(self, event=None):

        self.white_time = TOTAL_TIME
        self.grey_time = TOTAL_TIME
        self.running = False
        self.turn = None
        self.status.config(text="Game reset - press SPACE")
        self.white_label.config(fg="black")
        self.grey_label.config(fg="white")

    def toggle_fullscreen(self, event=None):

        current = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current)


root = tk.Tk()
ChessClock(root)
root.mainloop()