import tkinter as tk
from tkinter import messagebox

class Camera:
    def __init__(self, root, current_temperature, camera_var, temperature_label, motor):
        self.camera_frame = tk.LabelFrame(root, text="Select Camera:")
        self.camera_frame.pack(padx=10, pady=10)
        self.current_temperature = current_temperature
        self.camera_var = camera_var
        self.temperature_label = temperature_label
        self.camera_radio1 = tk.Radiobutton(self.camera_frame, text="Freezer", variable=self.camera_var, value="Freezer")
        self.camera_radio2 = tk.Radiobutton(self.camera_frame, text="Main Compartment", variable=self.camera_var, value="Main Compartment")
        self.camera_button = tk.Button(self.camera_frame, text="Open Camera", command=self.open_camera)
        self.close_camera_button = tk.Button(self.camera_frame, text="Close Door", command=self.close_door)
        self.camera_radio1.pack()
        self.camera_radio2.pack()
        self.camera_button.pack()
        self.close_camera_button.pack()
        self.motor = motor

    def open_camera(self):
        camera = self.camera_var.get()
        if camera == "Freezer":
            self.image_label.config(image=self.images["closefreeze"])
        elif camera == "Main Compartment":
            self.image_label.config(image=self.images["closemain"])
        self.temperature_label.config(text="Current Temperature: {}".format(self.current_temperature[camera]))
        messagebox.showinfo("Camera Opened", "Camera {} is now open".format(camera))
        self.door_open = True
        self.base_data.save_record("Camera Opened", camera)
        root.after(10000, self.check_door_status)

    def check_door_status(self):
        if self.door_open:
            door_status = messagebox.askyesno("BEEEEEEEEP!!!!!!!!", "Door is still open! Would you like to close it?")
            if door_status:
                self.close_door()
            else:
                self.root.after(10000, self.check_door_status)
    def close_door(self):
        self.image_label.config(image=self.images["closefridge"])
        self.door_open = False
        door_status = messagebox.askyesno("Door Alert", "Are you sure you want to close the door?")
        if door_status:
            self.save_record("Camera Closed", self.camera_var.get())
            messagebox.showinfo("Door Closed", "Door is now closed")
