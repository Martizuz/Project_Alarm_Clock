import tkinter as tk

class Motor:
    def __init__(self, root):
        self.motor_frame = tk.LabelFrame(root, text="Motor Status")
        self.motor_frame.pack(padx=10, pady=10)
        self.motor_status = False
        self.motor_label = tk.Label(self.motor_frame, text="Motor Status: OFF")
        self.motor_label.pack()