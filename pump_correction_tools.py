import numpy as np


def specific_speed(N_rpm, Q_BEP_water_m3s, H_BEP_water_m):
    """
    Calculates the pump specific speed based on its geometry and performance characteristics.

    Parameters:
        N_rpm (float): Pump rotational speed [rpm].
        Q_BEP_water_m3s (float): Flow rate at Best Efficiency Point (BEP) with water [m³/s].
        H_BEP_water_m (float): Head at BEP with water [m].

    Returns:
        float: Specific speed (dimensionless).
    """
    return (N_rpm * np.sqrt(Q_BEP_water_m3s)) / (H_BEP_water_m ** 0.75)


def B_from_water_conditions(nu_vis_cSt, Q_BEP_water_m3h, H_BEP_water_m, N_rpm):
    """
    Calculates B parameter for viscous correction based on water performance.

    Parameters:
        nu_vis_cSt (float): Kinematic viscosity of viscous fluid [cSt].
        Q_BEP_water_m3h (float): Flow rate at BEP with water [m³/h].
        H_BEP_water_m (float): Head at BEP with water [m].
        N_rpm (float): Pump speed [rpm].

    Returns:
        float: B parameter.
    """
    return (16.5 * nu_vis_cSt ** 0.5 * H_BEP_water_m ** 0.0625) / (Q_BEP_water_m3h ** 0.375 * N_rpm ** 0.25)


def correction_factor_flow(B):
    """
    Calculates the correction factor for flow rate under viscous conditions.

    Parameters:
        B (float): Dimensionless B parameter.

    Returns:
        float: Flow rate correction factor C_q.
    """
    return np.exp(-0.165 * (np.log10(B) ** 3.15))


def corrected_flow(C_q, Q_water):
    """
    Returns the corrected flow rate for viscous fluid.

    Parameters:
        C_q (float): Flow correction factor.
        Q_water (float): Flow rate with water [m³/h].

    Returns:
        float: Flow rate with viscous fluid [m³/h].
    """
    return Q_water * C_q


def C_BEP_head(C_q):
    """
    Returns the head correction factor at BEP.

    Parameters:
        C_q (float): Flow correction factor.

    Returns:
        float: Head correction factor at BEP.
    """
    return C_q


def corrected_BEP_head(C_BEP, H_BEP_water):
    """
    Returns the corrected BEP head for viscous fluid.

    Parameters:
        C_BEP (float): Correction factor at BEP.
        H_BEP_water (float): Head at BEP with water [m].

    Returns:
        float: Corrected BEP head [m].
    """
    return C_BEP * H_BEP_water


def correction_factor_head(C_BEP, Q_water, Q_BEP_water):
    """
    Returns the head correction factor for the operating condition.

    Parameters:
        C_BEP (float): Head correction factor at BEP.
        Q_water (float): Operating flow rate with water [m³/h].
        Q_BEP_water (float): Flow rate at BEP with water [m³/h].

    Returns:
        float: Head correction factor for operating point.
    """
    return 1 - ((1 - C_BEP) * (Q_water / Q_BEP_water) ** 0.75)


def corrected_head(C_H, H_water):
    """
    Returns the corrected operating head under viscous conditions.

    Parameters:
        C_H (float): Head correction factor.
        H_water (float): Operating head with water [m].

    Returns:
        float: Corrected head with viscous fluid [m].
    """
    return C_H * H_water


def correction_factor_efficiency(B):
    """
    Returns the efficiency correction factor for viscous fluid.

    Parameters:
        B (float): B parameter.

    Returns:
        float: Efficiency correction factor C_eta.
    """
    return B ** (-0.0547 * B ** 0.69)


def corrected_efficiency(C_eta, eta_water):
    """
    Returns the corrected pump efficiency under viscous conditions.

    Parameters:
        C_eta (float): Efficiency correction factor.
        eta_water (float): Efficiency with water [decimal].

    Returns:
        float: Corrected efficiency [decimal].
    """
    return C_eta * eta_water


def corrected_power(Q_vis, H_vis, rho, eta_vis):
    """
    Returns the required shaft power under viscous conditions.

    Parameters:
        Q_vis (float): Flow rate with viscous fluid [m³/h].
        H_vis (float): Total dynamic head [m].
        rho (float): Specific weight of the fluid [kg/m³].
        eta_vis (float): Efficiency under viscous conditions [decimal].

    Returns:
        float: Power [kW].
    """
    return (Q_vis * H_vis * rho) / (367 * eta_vis)


# --- Inverse problem (when viscous performance is known)

def B_from_viscous_operation(nu_vis_cSt, Q_vis, H_vis):
    """
    Calculates B parameter from viscous operating conditions.

    Parameters:
        nu_vis_cSt (float): Kinematic viscosity [cSt].
        Q_vis (float): Viscous flow rate [m³/h].
        H_vis (float): Viscous head [m].

    Returns:
        float: B parameter.
    """
    return (2.8 * nu_vis_cSt ** 0.5) / (Q_vis ** 0.25 * H_vis ** 0.125)


def inverse_correction_factor_flow(B):
    """
    Returns the inverse flow correction factor (C_q) — approximate value based on ANSI/HI 9.6.7.

    Parameters:
        B (float): B parameter.

    Returns:
        float: Correction factor.
    """
    return np.exp(-0.165 * (np.log10(5.7) ** 3.15))


def inverse_correction_factor_head(B):
    """
    Returns the inverse head correction factor (C_H) — approximate value based on ANSI/HI 9.6.7.

    Parameters:
        B (float): B parameter.

    Returns:
        float: Correction factor.
    """
    return np.exp(-0.165 * (np.log10(5.7) ** 3.15))  # approximation


def equivalent_water_flow(C_q, Q_vis):
    """
    Calculates equivalent flow rate if the fluid were water.

    Parameters:
        C_q (float): Flow correction factor.
        Q_vis (float): Viscous flow [m³/h].

    Returns:
        float: Equivalent water flow rate [m³/h].
    """
    return Q_vis / C_q


def equivalent_water_head(C_H, H_vis):
    """
    Calculates equivalent head if the fluid were water.

    Parameters:
        C_H (float): Head correction factor.
        H_vis (float): Viscous head [m].

    Returns:
        float: Equivalent water head [m].
    """
    return H_vis / C_H


def inverse_correction_factor_efficiency(B):
    """
    Returns the inverse correction factor for efficiency.

    Parameters:
        B (float): B parameter.

    Returns:
        float: Correction factor.
    """
    return B ** (-0.0547 * B ** 0.69)


def equivalent_water_efficiency(C_eta, eta_vis):
    """
    Estimates the equivalent water efficiency.

    Parameters:
        C_eta (float): Correction factor.
        eta_vis (float): Efficiency under viscous conditions [decimal].

    Returns:
        float: Efficiency with water [decimal].
    """
    return C_eta * eta_vis


def inverse_power(Q_vis, H_vis_total, rho, eta_vis):
    """
    Calculates the required power under viscous conditions.

    Parameters:
        Q_vis (float): Flow rate with viscous fluid [m³/h].
        H_vis_total (float): Total head [m].
        rho (float): Fluid density [kg/m³].
        eta_vis (float): Efficiency under viscous conditions [decimal].

    Returns:
        float: Required power [kW].
    """
    return (Q_vis * H_vis_total * rho) / (367 * eta_vis)
