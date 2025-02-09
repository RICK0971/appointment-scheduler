import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime, timedelta

class AppointmentScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Appointment Scheduler")

        self.fcfs_queue = []  # Queue for FCFS scheduling
        self.priority_queue = []  # Queue for priority-based scheduling
        self.appointment_duration = timedelta(minutes=30)
        self.next_available_time = datetime.now()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Appointment Scheduler", font=('Helvetica', 16, 'bold')).pack(pady=20)

        tk.Label(self.root, text="Enter Your Name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        # Dropdown menu for preferred appointment time
        self.time_var = tk.StringVar(self.root)
        self.time_var.set(self.next_available_time.strftime("%H:%M:%S"))
        tk.Label(self.root, text="Select Preferred Time:").pack()
        self.time_dropdown = tk.OptionMenu(self.root, self.time_var, *self.get_available_times())
        self.time_dropdown.pack(pady=10)

        tk.Button(self.root, text="Book Appointment (FCFS)", command=self.book_appointment_fcfs).pack(pady=10)
        tk.Button(self.root, text="Book Appointment (Priority)", command=self.book_appointment_priority).pack(pady=10)
        tk.Button(self.root, text="Next Appointment", command=self.next_appointment).pack(pady=10)
        tk.Button(self.root, text="Show Appointments (FCFS)", command=self.show_appointments_fcfs).pack(pady=10)
        tk.Button(self.root, text="Show Appointments (Priority)", command=self.show_appointments_priority).pack(pady=10)

    def book_appointment_fcfs(self):
        name = self.name_entry.get()
        if name:
            preferred_time = self.time_var.get()

            # Check if the time slot is available
            if not self.is_time_slot_taken(preferred_time, self.fcfs_queue + self.priority_queue):
                self.fcfs_queue.append((name, preferred_time))
                messagebox.showinfo("Appointment Booked (FCFS)", f"Appointment booked for {name} at {preferred_time}.")
                self.clear_entry()
            else:
                messagebox.showwarning("Time Slot Taken", f"The selected time slot at {preferred_time} is already booked. Please choose another time.")
        else:
            messagebox.showwarning("Empty Name", "Please enter your name.")

    def book_appointment_priority(self):
        name = self.name_entry.get()
        if name:
            priority = self.get_priority()
            preferred_time = self.time_var.get()

            # Check if the time slot is available
            if not self.is_time_slot_taken(preferred_time, self.fcfs_queue + self.priority_queue):
                self.priority_queue.append((name, priority, preferred_time))
                self.priority_queue.sort(key=lambda x: x[1], reverse=True)  # Sort by priority
                messagebox.showinfo("Appointment Booked (Priority)", f"Appointment booked for {name} at {preferred_time}.")
                self.clear_entry()
            else:
                messagebox.showwarning("Time Slot Taken", f"The selected time slot at {preferred_time} is already booked. Please choose another time.")
        else:
            messagebox.showwarning("Empty Name", "Please enter your name.")

    def is_time_slot_taken(self, time_slot, appointments):
        for appointment in appointments:
            # Check if the time slot matches any existing appointment
            if len(appointment) == 3:  # Handle both 2-value and 3-value tuples
                _, _, time = appointment
            else:
                _, time = appointment
            if time == time_slot:
                return True
        return False

    def next_appointment(self):
        if self.fcfs_queue:
            next_patient_fcfs = self.fcfs_queue.pop(0)
            messagebox.showinfo("Next Appointment (FCFS)", f"Next appointment is for {next_patient_fcfs[0]} at {next_patient_fcfs[1]}.")
        else:
            messagebox.showinfo("No Appointments (FCFS)", "There are no appointments in the FCFS queue.")

        if self.priority_queue:
            next_patient_priority = self.priority_queue.pop(0)
            messagebox.showinfo("Next Appointment (Priority)", f"Next appointment is for {next_patient_priority[0]} at {next_patient_priority[2]}.")
        else:
            messagebox.showinfo("No Appointments (Priority)", "There are no appointments in the priority queue.")

    def show_appointments_fcfs(self):
        if self.fcfs_queue:
            appointments_info_fcfs = "\n".join([f"{name} at {preferred_time}" for name, preferred_time in self.fcfs_queue])
            messagebox.showinfo("Appointments (FCFS)", f"Current Appointments (FCFS):\n{appointments_info_fcfs}")
        else:
            messagebox.showinfo("No Appointments (FCFS)", "There are no appointments in the FCFS queue.")

    def show_appointments_priority(self):
        if self.priority_queue:
            appointments_info_priority = "\n".join([f"{name} (Priority: {priority}) at {preferred_time}" for name, priority, preferred_time in self.priority_queue])
            messagebox.showinfo("Appointments (Priority)", f"Current Appointments (Priority):\n{appointments_info_priority}")
        else:
            messagebox.showinfo("No Appointments (Priority)", "There are no appointments in the priority queue.")

    def get_available_times(self):
        # Generate a list of available times based on the current time
        available_times = []
        current_time = datetime.now()
        for _ in range(5):  # Provide options for the next 5 time slots
            available_times.append(current_time.strftime("%H:%M:%S"))
            current_time += self.appointment_duration
        return available_times

    def get_priority(self):
        try:
            priority = int(simpledialog.askstring("Priority", "Enter priority (1 being the highest):"))
            return priority
        except ValueError:
            messagebox.showwarning("Invalid Priority", "Priority must be a number.")
            return 0

    def clear_entry(self):
        self.name_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    scheduler = AppointmentScheduler(root)
    root.mainloop()
