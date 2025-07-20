import numpy as np

def reynolds_number(rho, u, D, mu):
    """
    Calculates the Reynolds number for internal flow.

    Parameters:
        rho (float): Fluid density [kg/m³]
        u (float): Mean velocity [m/s]
        D (float): Pipe diameter [m]
        mu (float): Dynamic viscosity [Pa·s]

    Returns:
        float: Reynolds number
    """
    return (rho * u * D) / mu


def friction_factor(Re, D, epsilon, f_init=0.02, tol=1e-6, max_iter=100):
    """
    Solves the implicit Colebrook-White equation for the Darcy-Weisbach friction factor.

    Parameters:
        Re (float): Reynolds number
        D (float): Pipe diameter [m]
        epsilon (float): Absolute roughness [m]
        f_init (float): Initial guess for f
        tol (float): Convergence tolerance
        max_iter (int): Maximum iterations

    Returns:
        float: Darcy-Weisbach friction factor

    Raises:
        RuntimeError: If solution does not converge within max_iter
    """
    if Re > 2300:
        f = f_init
        for _ in range(max_iter):
            lhs = 1.0 / np.sqrt(f)
            rhs = -2.0 * np.log10((epsilon / (3.7 * D)) + (2.51 / (Re * np.sqrt(f))))
            f_new = 1.0 / (rhs ** 2)

            if abs(f - f_new) < tol:
                return f_new
            f = f_new
    else:
        f = 64 / Re
        print(f"Laminar flow friction factor: {f:.5f}")
        return f

    raise RuntimeError("Friction factor did not converge within the maximum number of iterations.")


def pressure_drop(L, D, u, f, rho):
    """
    Calculates pressure drop due to friction in a circular pipe using the Darcy-Weisbach equation.

    Parameters:
        L (float): Pipe length [m]
        D (float): Pipe diameter [m]
        u (float): Mean velocity [m/s]
        f (float): Friction factor (Darcy-Weisbach)
        rho (float): Fluid density [kg/m³]

    Returns:
        float: Pressure drop [Pa]
    """
    return f * (L / D) * (rho * u**2 / 2)
