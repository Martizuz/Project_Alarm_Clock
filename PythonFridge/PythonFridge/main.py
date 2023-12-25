import tkinter as tk
from tkinter import messagebox
from camera import Camera
from temperature import Temperature
from basedata import BaseData
from motor import Motor
import sqlite3

class Main:
    def __init__(self, root):
        self.root = root
        self.root.title("Fridge")
        self.current_temperature = {"Freezer": -10, "Main Compartment": -3}
        self.motor_status = False
        self.door_open = False
        self.conn = sqlite3.connect("fridge_records.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS records (event TEXT, camera TEXT, timestamp TEXT)")
        self.conn.commit()
        self.camera_frame = tk.LabelFrame(root, text="Select Camera:")
        self.temperature_frame = tk.LabelFrame(root, text="Temperature")
        self.motor_frame = tk.LabelFrame(root, text="Motor Status")
        self.database_frame = tk.Frame(root)
        self.camera_frame.pack(padx=10, pady=10)
        self.temperature_frame.pack(padx=10, pady=10)
        self.motor_frame.pack(padx=10, pady=10)
        self.database_frame.pack(pady=10)
        self.camera_var = tk.StringVar()
        self.camera_var.set("Freezer")
        self.camera_radio1 = tk.Radiobutton(self.camera_frame, text="Freezer", variable=self.camera_var, value="Freezer")
        self.camera_radio2 = tk.Radiobutton(self.camera_frame, text="Main Compartment", variable=self.camera_var, value="Main Compartment")
        self.camera_button = tk.Button(self.camera_frame, text="Open Camera", command=self.open_camera)
        self.close_camera_button = tk.Button(self.camera_frame, text="Close Door", command=self.close_door)
        self.camera_radio1.pack()
        self.camera_radio2.pack()
        self.camera_button.pack()
        self.close_camera_button.pack()
        self.temperature_label = tk.Label(self.temperature_frame, text="Current Temperature: {}".format(self.current_temperature[self.camera_var.get()]))
        self.temperature_entry = tk.Entry(self.temperature_frame)
        self.temperature_button = tk.Button(self.temperature_frame, text="Set Temperature", command=self.set_temperature)
        self.temperature_label.pack()
        self.temperature_entry.pack(pady=10)
        self.temperature_button.pack()
        self.motor_label = tk.Label(self.motor_frame, text="Motor Status: OFF")
        self.motor_label.pack()
        self.database_button = tk.Button(self.database_frame, text="Open Database", command=self.open_database)
        self.clear_records_button = tk.Button(self.database_frame, text="Clear Records", command=self.clear_records)
        self.database_button.pack()
        self.clear_records_button.pack()
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(padx=500, side="right")
        self.images = {
            "closefridge": tk.PhotoImage(file="closefridge.png"),
            "closefreeze": tk.PhotoImage(file="closefreeze.png"),
            "closemain": tk.PhotoImage(file="closemain.png"),
        }
        self.image_label = tk.Label(self.image_frame, image=self.images["closefridge"])
        self.image_label.pack()

    def open_camera(self):
        camera = self.camera_var.get()
        if camera == "Freezer":
            self.image_label.config(image=self.images["closefreeze"])
        elif camera == "Main Compartment":
            self.image_label.config(image=self.images["closemain"])
        self.temperature_label.config(text="Current Temperature: {}".format(self.current_temperature[camera]))
        messagebox.showinfo("Camera Opened", "Camera {} is now open".format(camera))
        self.door_open = True
        self.save_record("Camera Opened", camera)
        self.root.after(10000, self.check_door_status)
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
    def set_temperature(self):
        camera = self.camera_var.get()
        new_temperature = int(self.temperature_entry.get())
        if new_temperature < self.current_temperature[camera]:
            self.motor_status = True
            self.motor_label.config(text="Motor Status: ON")
        else:
            self.motor_status = False
            self.motor_label.config(text="Motor Status: OFF")
        self.current_temperature[camera] = new_temperature
        self.temperature_label.config(text="Current Temperature: {}".format(self.current_temperature[camera]))
        self.save_record("Temperature Set", camera)
        messagebox.showinfo("Temperature Updated", "Temperature for {} updated".format(camera))
    def save_record(self, event, camera):
        self.cursor.execute("INSERT INTO records (event, camera, timestamp) VALUES (?, ?, DATETIME('now'))", (event, camera))
        self.conn.commit()
    def open_database(self):
        messagebox.showinfo("Database", "Opening database...")
    def clear_records(self):
        confirmation = messagebox.askyesno("Clear Records", "Are you sure you want to clear all records?")
        if confirmation:
            self.cursor.execute("DELETE FROM records")
            self.conn.commit()
            messagebox.showinfo("Records Cleared", "All records have been cleared")
    def open_database(self):
        db_window = tk.Toplevel(self.root)
        db_window.title("Database Records")
        db_text = tk.Text(db_window)
        db_text.pack()
        self.cursor.execute("SELECT * FROM records")
        records = self.cursor.fetchall()
        for record in records:
            db_text.insert(tk.END, f"Event: {record[0]}, Camera: {record[1]}, Timestamp: {record[2]}\n")
if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    root.mainloop()