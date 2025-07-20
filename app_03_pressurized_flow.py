import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from flow_resistance import reynolds_number, friction_factor, pressure_drop  # keep original names for imported funcs

def save_plot(input_data, output_data, filename="flow_report"):
    Path("plots").mkdir(exist_ok=True)
    filepath = Path("plots") / f"{filename}.png"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("off")

    lines = ["== Input Data =="] + input_data + [""] + ["== Calculated Results =="] + output_data
    for i, line in enumerate(lines):
        ax.text(0.05, 1 - i * 0.07, line, fontsize=11, va='top')

    plt.tight_layout()
    fig.savefig(filepath, dpi=300)
    plt.close()
    messagebox.showinfo("Success", f"Image saved as {filepath}")

def calculate():
    try:
        g = float(entry_g.get())
        mu = float(entry_mu.get())
        rho = float(entry_rho.get())
        P_nominal = float(entry_P_nominal.get())
        P_min = float(entry_P_min.get())
        divisor = float(entry_divisor.get())
        Q_m3h = float(entry_Q.get())
        D_inch = float(entry_D.get())
        roughness = float(entry_roughness.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter all values correctly.")
        return

    Q_m3s = Q_m3h / 3600
    D_m = D_inch * 2.54 / 100
    A = np.pi * (D_m / 2) ** 2
    velocity = Q_m3s / A
    mass_flow = Q_m3s * rho

    Re = reynolds_number(rho=rho, u=velocity, D=D_m, mu=mu)
    f = friction_factor(Re=Re, D=D_m, epsilon=roughness, f_init=0.02, tol=1e-6, max_iter=100)
    delta_P_max = P_nominal - P_min
    head_loss_per_meter = pressure_drop(L=1, D=D_m, u=velocity, f=f, rho=rho)
    length = (delta_P_max / divisor) / head_loss_per_meter
    manometric_head = (delta_P_max / divisor) / (rho * g)

    input_data = [
        f"Gravity: {g} m/s²",
        f"Dynamic viscosity: {mu} Pa·s",
        f"Density: {rho} kg/m³",
        f"Nominal pressure: {P_nominal/1e5:.2f} bar",
        f"Minimum pressure: {P_min/1e5:.2f} bar",
        f"ΔP divisor coefficient: {divisor}",
        f"Volumetric flow rate: {Q_m3h} m³/h",
        f"Internal diameter: {D_inch} in = {D_m:.4f} m",
        f"Absolute roughness: {roughness} m"
    ]

    output_data = [
        f"Reynolds number: {Re:.2e}",
        f"Friction factor (f): {f:.5f}",
        f"Pressure loss per meter: {head_loss_per_meter:.2f} Pa/m",
        f"Total length (L): {length:.2f} m",
        f"Manometric head (H): {manometric_head:.2f} m",
        f"Mass flow rate: {mass_flow:.2f} kg/s",
        f"Average velocity: {velocity:.2f} m/s"
    ]

    # Save for export
    calculate.input_data = input_data
    calculate.output_data = output_data

    messagebox.showinfo("Results", "\n".join(output_data))

def save_with_name():
    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showerror("Error", "Please enter a filename to save.")
        return
    if not hasattr(calculate, 'input_data') or not hasattr(calculate, 'output_data'):
        messagebox.showwarning("Attention", "Calculate first before saving.")
        return
    save_plot(calculate.input_data, calculate.output_data, filename)

root = tk.Tk()
root.title("Pressurized Pipeline Flow Calculation")

frame = ttk.Frame(root, padding=12)
frame.grid()

labels = [
    ("Gravity [m/s²]:", "9.81"),
    ("Dynamic viscosity μ [Pa·s]:", "0.0945"),
    ("Density ρ [kg/m³]:", "945"),
    ("Nominal pressure [Pa]:", "1000000"),
    ("Minimum pressure [Pa]:", "520000"),
    ("Pressure drop divisor (ΔP/div):", "2"),
    ("Volumetric flow rate [m³/h]:", "2124"),
    ("Internal diameter [inch]:", "24"),
    ("Absolute roughness [m]:", "0.000045"),
]

entries = []
for i, (text, default) in enumerate(labels):
    ttk.Label(frame, text=text).grid(row=i, column=0, sticky="w")
    entry = ttk.Entry(frame)
    entry.insert(0, default)
    entry.grid(row=i, column=1)
    entries.append(entry)

(entry_g, entry_mu, entry_rho, entry_P_nominal, entry_P_min,
 entry_divisor, entry_Q, entry_D, entry_roughness) = entries

ttk.Label(frame, text="Filename (without extension):").grid(row=len(labels), column=0, sticky="w")
entry_filename = ttk.Entry(frame)
entry_filename.grid(row=len(labels), column=1)

ttk.Button(frame, text="Calculate", command=calculate).grid(row=len(labels)+1, columnspan=2, pady=6)
ttk.Button(frame, text="Save Plot", command=save_with_name).grid(row=len(labels)+2, columnspan=2)

root.mainloop()
