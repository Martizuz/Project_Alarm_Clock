import tkinter as tk
from tkinter import messagebox

class Temperature:
    def __init__(self, root, current_temperature, camera_var, temperature_label, temperature_entry, motor):
        self.temperature_frame = tk.LabelFrame(root, text="Temperature")
        self.temperature_frame.pack(padx=10, pady=10)
        self.camera_var = camera_var
        self.current_temperature = current_temperature
        self.temperature_label = temperature_label
        self.temperature_entry = temperature_entry
        self.temperature_button = tk.Button(self.temperature_frame, text="Set Temperature", command=self.set_temperature)
        self.temperature_label.pack()
        self.temperature_entry.pack(pady=10)
        self.temperature_button.pack()
        self.motor = motor

    def set_temperature(self):
        camera = self.camera_var.get()
        new_temperature = int(self.temperature_entry.get())
        if new_temperature < self.current_temperature[camera]:
            self.motor.motor_status = True
            self.motor.motor_label.config(text="Motor Status: ON")
        else:
            self.motor.motor_status = False
            self.motor.motor_label.config(text="Motor Status: OFF")
        self.current_temperature[camera] = new_temperature
        self.temperature_label.config(text="Current Temperature: {}".format(self.current_temperature[camera]))
        self.save_record("Temperature Set", camera)
        messagebox.showinfo("Temperature Updated", "Temperature for {} updated".format(camera))
