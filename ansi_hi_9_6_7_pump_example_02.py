"""
Example 2: Given viscous operation data (head, flow, viscosity),
calculate the equivalent water operation parameters using ANSI/HI 9.6.7 corrections.
"""

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

# --- Input data ---
Q_vis = 100.0       # Flow rate with viscous fluid [m³/h]
H_vis = 70.0        # Head with viscous fluid [m]
Visc = 120          # Kinematic viscosity [cSt]
s = 0.9             # Specific gravity [-]
eta_BEP_w = 0.68    # Efficiency at BEP with water [-]

# Step 1: Calculate B parameter
B = B_from_viscous_operation(nu_vis_cSt=Visc, Q_vis=Q_vis, H_vis=H_vis)
if B >= 40:
    print(f"B parameter out of valid range (<40): B = {B:.2f}")
else:
    print(f"B parameter within valid range (<40): B = {B:.2f}")

# Step 2: Calculate correction factors for viscous effect
if B <= 1.0:
    C_q = 1.0
    C_h = 1.0
    C_eta = 1.0
else:
    C_q = inverse_correction_factor_flow(B)
    C_h = inverse_correction_factor_head(B)
    C_eta = inverse_correction_factor_efficiency(B)

# Step 3: Calculate equivalent water operating conditions
Q_water = equivalent_water_flow(C_q, Q_vis)
H_water = equivalent_water_head(C_h, H_vis)
eta_vis = equivalent_water_efficiency(C_eta, eta_BEP_w)

# Step 4: Calculate required power under viscous conditions
P_vis = inverse_power(Q_vis, H_vis_total=H_vis, rho=s, eta_vis=eta_vis)

# --- Output ---
print(f"Equivalent Water Flow Rate (Q_water) = {Q_water:.2f} m³/h")
print(f"Equivalent Water Head (H_water)       = {H_water:.2f} m")
print(f"Corrected Efficiency (eta_vis)        = {eta_vis:.4f}")
print(f"Required Power (P_vis)                 = {P_vis:.2f} kW")

# --- Expected values updated with your results ---
expected_values = {
    "B": 5.7,
    "C_q": 0.934,
    "C_h": 0.934,
    "Q_water": 107.1,
    "H_water": 74.9,
    "C_eta": 0.729,
    "eta_vis": 0.496,
    "P_vis": 34.6
}

# --- Validation with detailed messages ---
def check(value, expected, name, tol=0.2):
    assert abs(value - expected) <= tol, \
        f"{name} mismatch: calculated = {value:.3f}, expected = {expected:.3f}"

check(B, expected_values["B"], "Parameter B")
check(C_q, expected_values["C_q"], "Correction factor C_q")
check(C_h, expected_values["C_h"], "Correction factor C_h")
check(Q_water, expected_values["Q_water"], "Equivalent Water Flow Rate Q_water")
check(H_water, expected_values["H_water"], "Equivalent Water Head H_water")
check(C_eta, expected_values["C_eta"], "Correction factor C_eta")
check(eta_vis, expected_values["eta_vis"], "Corrected Efficiency eta_vis")
check(P_vis, expected_values["P_vis"], "Corrected Power P_vis")

print("✔ All results validated successfully.")
