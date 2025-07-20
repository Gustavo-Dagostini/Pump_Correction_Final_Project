import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from pump_correction_tools import (
    specific_speed, B_from_water_conditions, correction_factor_flow, correction_factor_head,
    C_BEP_head, correction_factor_efficiency, corrected_efficiency,
    corrected_head, corrected_power  # Or rename potencia_water_known to corrected_power if you prefer
)

def calculate_and_plot():
    try:
        pump_name = entry_pump_name.get().strip()
        if not pump_name:
            messagebox.showerror("Error", "Please enter the pump name.")
            return

        Q_BEP_water = float(entry_q.get())
        H_total = float(entry_h.get())
        N = float(entry_n.get())
        eta_water = float(entry_eta.get()) / 100  # Convert percent to decimal
        viscosity = float(entry_visc.get())
        specific_gravity = float(entry_s.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")
        return

    # Validations
    n_s = specific_speed(N_rpm=N, Q_BEP_water_m3s=Q_BEP_water / 3600, H_BEP_water_m=H_total)
    if n_s > 60:
        messagebox.showwarning("Warning", f"Specific speed is out of valid range (<60). n_s = {n_s:.2f}")
        return

    if not (1 <= viscosity <= 4000):
        messagebox.showwarning("Warning", "Viscosity is out of valid range (1 to 4000 cSt).")
        return

    B = B_from_water_conditions(nu_vis_cSt=viscosity, Q_BEP_water_m3h=Q_BEP_water, H_BEP_water_m=H_total, N_rpm=N)
    if B > 40:
        messagebox.showwarning("Warning", f"B parameter is out of valid range (<40). B = {B:.2f}")
        return

    ratios = np.arange(0.2, 1.6, 0.1)
    Q = ratios * Q_BEP_water

    corrected_head_vals = []
    corrected_eta_vals = []
    corrected_power_vals = []

    original_head = [H_total] * len(Q)
    original_eta = [eta_water] * len(Q)
    original_power = [corrected_power(q, H_total, specific_gravity, eta_water) for q in Q]

    for ratio in ratios:
        Q_water = ratio * Q_BEP_water

        if B <= 1.0:
            C_q = C_h = C_eta = 1.0
        else:
            C_q = correction_factor_flow(B)
            C_BEP_H = C_BEP_head(C_q)
            C_h = correction_factor_head(C_BEP_H, Q_water, Q_BEP_water)
            C_eta = correction_factor_efficiency(B)

        Q_visc = Q_water * C_q
        H_visc = corrected_head(C_h, H_total)
        eta_visc = corrected_efficiency(C_eta, eta_water)
        P = corrected_power(Q_visc, H_visc, specific_gravity, eta_visc)

        corrected_head_vals.append(H_visc)
        corrected_eta_vals.append(eta_visc)
        corrected_power_vals.append(P)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(Q, original_head, '--', label='Head (Water)', color='blue')
    ax1.plot(Q, corrected_head_vals, '-o', label='Head (Viscous Fluid)', color='blue')

    ax1.plot(Q, original_power, '--', label='Power (Water)', color='green')
    ax1.plot(Q, corrected_power_vals, '-o', label='Power (Viscous Fluid)', color='green')

    ax2.plot(Q, np.array(original_eta) * 100, '--', label='Efficiency (Water)', color='red')
    ax2.plot(Q, np.array(corrected_eta_vals) * 100, '-o', label='Efficiency (Viscous Fluid)', color='red')

    ax1.set_xlabel(r"Flow Rate $[m^3/h]$")
    ax1.set_ylabel(r"Head [m]; Power [kW]")
    ax2.set_ylabel(r"Efficiency $[\%]$")
    ax2.set_ylim(0, 100)

    ax1.grid(True)

    plt.subplots_adjust(right=0.75)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    fig.legend(lines1 + lines2, labels1 + labels2,
               loc='lower right', bbox_to_anchor=(0.95, 0.15), fontsize=9)

    info_text = '\n'.join((
        f"Pump Data - {pump_name}",
        "",
        rf"$Q_{{\mathrm{{BEP}}}} = {Q_BEP_water:.1f}\ m^3/h$",
        rf"$H_{{\mathrm{{BEP}}}} = {H_total:.1f}\ m$",
        rf"$N = {N:.0f}\ RPM$",
        rf"$\eta = {eta_water * 100:.1f}\ \%$",
        rf"$\nu = {viscosity:.1f}\ cSt$",
        rf"$s = {specific_gravity:.2f}$",
        rf"$n_s = {n_s:.2f}$",
        rf"$B = {B:.2f}$"
    ))

    props = dict(boxstyle='round', facecolor='white', alpha=0.9, linewidth=1)
    ax1.text(1.1, 1.0, info_text, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top', bbox=props)

    plt.title("Pump Curves (Original vs Corrected)", fontsize=14)

    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)

    clean_name = pump_name.replace(" ", "_").replace("/", "_")

    file_name = output_dir / f"pump_curves_{clean_name}.pdf"
    plt.savefig(file_name, format='pdf')
    plt.show()

    messagebox.showinfo("Success", f"Chart saved at:\n{file_name.resolve()}")

root = tk.Tk()
root.title("Pump Curve Viscosity Correction")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Pump Name:").grid(row=0, column=0)
entry_pump_name = ttk.Entry(frame)
entry_pump_name.grid(row=0, column=1)

ttk.Label(frame, text="Flow Rate (Best Efficiency Point) [m³/h]:").grid(row=1, column=0)
entry_q = ttk.Entry(frame)
entry_q.grid(row=1, column=1)

ttk.Label(frame, text="Total Head [m]:").grid(row=2, column=0)
entry_h = ttk.Entry(frame)
entry_h.grid(row=2, column=1)

ttk.Label(frame, text="Rotational Speed [RPM]:").grid(row=3, column=0)
entry_n = ttk.Entry(frame)
entry_n.grid(row=3, column=1)

ttk.Label(frame, text="Efficiency [%]:").grid(row=4, column=0)
entry_eta = ttk.Entry(frame)
entry_eta.grid(row=4, column=1)

ttk.Label(frame, text="Kinematic Viscosity (1-4000) [cSt]:").grid(row=5, column=0)
entry_visc = ttk.Entry(frame)
entry_visc.grid(row=5, column=1)

ttk.Label(frame, text="Specific Gravity:").grid(row=6, column=0)
entry_s = ttk.Entry(frame)
entry_s.grid(row=6, column=1)

ttk.Button(frame, text="Generate Chart", command=calculate_and_plot).grid(row=7, columnspan=2, pady=10)

root.mainloop()
