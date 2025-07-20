import numpy as np
from pump_correction_tools import (
    specific_speed,
    B_from_water_conditions,
    correction_factor_flow,
    correction_factor_head,
    C_BEP_head,
    correction_factor_efficiency,
    corrected_efficiency,
    corrected_head,
    corrected_power
)

"""
This script solves Example 01 from the ANSI/HI 9.6.7 standard,
where the pump operating conditions with water are known.
"""

# --- Input parameters ---
Q_BEP_water = 110.0         # Flow at BEP with water [m³/h]
H_total_water = 77.0        # Head at BEP with water [m]
N_rpm = 2950                # Pump speed [rpm]
eta_water = 0.68            # Efficiency with water [-]
kinematic_viscosity = 120.0 # Viscosity [cSt]
specific_gravity = 0.9      # Specific gravity [-]

# Step 1: Calculate specific speed (metric units, ≤ 60)
n_s = specific_speed(N_rpm, Q_BEP_water / 3600, H_total_water)
if n_s <= 60:
    print(f"Specific speed is within valid range (≤ 60): n_s = {n_s:.2f}")
else:
    print(f"Specific speed is out of valid range (> 60): n_s = {n_s:.2f}")

# Step 2: Calculate B parameter for viscosity correction
B = B_from_water_conditions(kinematic_viscosity, Q_BEP_water, H_total_water, N_rpm)
if B >= 40:
    print(f"B parameter is out of valid range (< 40): B = {B:.2f}")
else:
    print(f"B parameter is within valid range (< 40): B = {B:.2f}")

# Step 3: Calculate correction factors and corrected values
if B <= 1.0:
    C_q = 1.0
    C_h = 1.0
    C_eta = 1.0
    Q_vis = Q_BEP_water
    H_vis = H_total_water
    eta_vis = eta_water
else:
    C_q = correction_factor_flow(B)
    Q_vis = Q_BEP_water * C_q

    C_BEP = C_BEP_head(C_q)
    C_h = correction_factor_head(C_BEP, Q_BEP_water, Q_BEP_water)
    H_vis = corrected_head(C_h, H_total_water)

    C_eta = correction_factor_efficiency(B)
    eta_vis = corrected_efficiency(C_eta, eta_water)

# Step 4: Calculate corrected power
P_vis = corrected_power(Q_vis, H_vis, specific_gravity, eta_vis)

# --- Output ---
print(f"Corrected Flow Rate (Q_vis)     = {Q_vis:.2f} m³/h")
print(f"Corrected Head (H_vis)           = {H_vis:.2f} m")
print(f"Corrected Efficiency (eta_vis)   = {eta_vis:.4f}")
print(f"Required Power (P_vis)           = {P_vis:.2f} kW")

# --- Expected results ---
expected_values = {
    "B": 5.52,
    "C_q": 0.938,
    "Q_vis": 103.2,
    "C_BEP": 0.938,
    "H_BEP_Vis": 72.2,
    "C_H": 0.958,
    "H_Vis": 83.9,
    "C_eta": 0.738,
    "eta_Vis": 0.502,
    "Power_Vis": 36.4
}

# --- Validations with detailed error messages ---
def check(value, expected, name, tol=1e-1):
    assert np.isclose(value, expected, atol=tol), \
        f"{name} mismatch: calculated = {value:.3f}, expected = {expected:.3f}"

check(B, expected_values["B"], "Parameter B")
check(C_q, expected_values["C_q"], "Correction factor C_q")
check(Q_vis, expected_values["Q_vis"], "Corrected Flow Rate Q_vis")
check(C_BEP, expected_values["C_BEP"], "Correction factor C_BEP")
check(C_eta, expected_values["C_eta"], "Correction factor C_eta")
check(eta_vis, expected_values["eta_Vis"], "Corrected Efficiency eta_vis")
check(P_vis, expected_values["Power_Vis"], "Corrected Power P_vis")

print("✔ All results validated successfully.")
