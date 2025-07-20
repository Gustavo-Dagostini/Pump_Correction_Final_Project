import tkinter as tk
from tkinter import ttk

# Assuming your apps are in separate modules:
# import app_01
# import app_02
# import pressurized_line

def open_app_01():
    # Import or call the main function of app_01
    import app_01_pump_correction
    app_01_pump_correction.main()  # assuming each app has a main() function

def open_app_02():
    import app_02_pump_correction
    app_02_pump_correction.main()

def open_pressurized_line():
    import app_03_pressurized_flow
    app_03_pressurized_flow.main()

def main_launcher():
    root = tk.Tk()
    root.title("Application Launcher")

    frame = ttk.Frame(root, padding=20)
    frame.grid()

    ttk.Label(frame, text="Select an application:", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Button(frame, text="Pump Correction - Example 1", width=30, command=open_app_01).grid(row=1, column=0, pady=5)
    ttk.Button(frame, text="Pump Correction - Example 2", width=30, command=open_app_02).grid(row=2, column=0, pady=5)
    ttk.Button(frame, text="Pressurized Pipeline", width=30, command=open_pressurized_line).grid(row=3, column=0, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_launcher()
