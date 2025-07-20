import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt

from pump_correction_tools import (
    B_from_viscous_operation,
    inverse_correction_factor_flow,
    inverse_correction_factor_head,
    equivalent_water_flow,
    equivalent_water_head,
    inverse_correction_factor_efficiency,
    equivalent_water_efficiency,
    inverse_power
)

def save_plot(input_data, output_data, filename="report_plot"):
    # Ensure the 'plots' folder exists
    plots_folder = Path("plots")
    plots_folder.mkdir(exist_ok=True)

    file_path = plots_folder / f"{filename}.png"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # hide axes

    # Formatted text
    lines = ["== Input Data =="] + input_data + [""] + ["== Correction Results =="] + output_data

    for i, line in enumerate(lines):
        ax.text(0.05, 1 - i * 0.07, line, fontsize=11, va='top')

    plt.tight_layout()
    fig.savefig(file_path, dpi=300)
    plt.close(fig)
    messagebox.showinfo("Image Saved", f"Plot saved as '{file_path}'")

def calculate():
    try:
        Q_visc = float(entry_q_visc.get())
        H_visc = float(entry_h_visc.get())
        viscosity = float(entry_viscosity.get())
        specific_gravity = float(entry_specific_gravity.get())
        eta_water = float(entry_eta_water.get()) / 100  # convert % to decimal
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")
        return

    B = B_from_viscous_operation(nu_vis_cSt=viscosity, Q_vis=Q_visc, H_vis=H_visc)

    if B >= 40:
        messagebox.showwarning("Warning", f"Parameter B out of valid range (<40). B = {B:.2f}")
        return

    if not (1 <= viscosity <= 4000):
        messagebox.showwarning("Warning", "Viscosity out of allowed range (1 to 4000 cSt).")
        return

    if B <= 1.0:
        C_q = C_h = C_eta = 1.0
    else:
        C_q = inverse_correction_factor_flow(B)
        C_h = inverse_correction_factor_head(B)
        C_eta = inverse_correction_factor_efficiency(B)

    # Step 3: Calculate equivalent water operating conditions
    Q_water = equivalent_water_flow(C_q, Q_visc)
    H_water = equivalent_water_head(C_h, H_visc)
    eta_vis = equivalent_water_efficiency(C_eta, eta_water)

    # Step 4: Calculate required power under viscous conditions
    P_vis = inverse_power(Q_visc, H_vis_total=H_visc, rho=specific_gravity, eta_vis=eta_vis)

    output_data = [
        f"Parameter B: {B:.2f}",
        f"Corrected flow (water equivalent): {Q_water:.2f} m³/h",
        f"Corrected head (water equivalent): {H_water:.2f} m",
        f"Efficiency with viscosity: {eta_vis*100:.2f} %",
        f"Power with viscosity: {P_vis:.2f} kW"
    ]

    input_data = [
        f"Flow with viscosity: {Q_visc} m³/h",
        f"Manometric head: {H_visc} m",
        f"Viscosity: {viscosity} cSt",
        f"Specific gravity: {specific_gravity}",
        f"Efficiency with water: {eta_water*100:.2f} %"
    ]

    # Store for later saving
    calculate.input_data = input_data
    calculate.output_data = output_data

    messagebox.showinfo("Results", '\n'.join(output_data))

def save_with_name():
    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showerror("Error", "Please enter a filename.")
        return

    if not hasattr(calculate, 'input_data') or not hasattr(calculate, 'output_data'):
        messagebox.showwarning("Warning", "You need to calculate before saving the plot.")
        return

    save_plot(calculate.input_data, calculate.output_data, filename)

# GUI setup
root = tk.Tk()
root.title("Viscous Fluid Operation Correction")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Flow with viscosity [m³/h]:").grid(row=0, column=0, sticky='w')
entry_q_visc = ttk.Entry(frame)
entry_q_visc.grid(row=0, column=1)

ttk.Label(frame, text="Manometric head [m]:").grid(row=1, column=0, sticky='w')
entry_h_visc = ttk.Entry(frame)
entry_h_visc.grid(row=1, column=1)

ttk.Label(frame, text="Viscosity [cSt] (1 to 4000):").grid(row=2, column=0, sticky='w')
entry_viscosity = ttk.Entry(frame)
entry_viscosity.grid(row=2, column=1)

ttk.Label(frame, text="Specific gravity:").grid(row=3, column=0, sticky='w')
entry_specific_gravity = ttk.Entry(frame)
entry_specific_gravity.grid(row=3, column=1)

ttk.Label(frame, text="Efficiency with water (%):").grid(row=4, column=0, sticky='w')
entry_eta_water = ttk.Entry(frame)
entry_eta_water.grid(row=4, column=1)

ttk.Label(frame, text="Output filename (without extension):").grid(row=5, column=0, sticky='w')
entry_filename = ttk.Entry(frame)
entry_filename.grid(row=5, column=1)

ttk.Button(frame, text="Calculate Correction", command=calculate).grid(row=6, columnspan=2, pady=10)
ttk.Button(frame, text="Save Plot", command=save_with_name).grid(row=7, columnspan=2, pady=5)

root.mainloop()
