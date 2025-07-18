import numpy as np
from CoolProp.CoolProp import PropsSI

def Reynolds (rho, u, D, mu):
    return (rho * u * D) / mu


def f_atrito(Re, D, epsilon, f_init=0.02, tol=1e-6, max_iter=100):
    """
    Resolve a equação implícita de Colebrook-White para fator de atrito f.

    Parâmetros:
    Re : float - número de Reynolds
    D : float - diâmetro do tubo (m)
    epsilon : float - rugosidade absoluta (m)
    f_init : float - chute inicial para f
    tol : float - tolerância para convergência
    max_iter : int - número máximo de iterações

    Retorna:
    f : float - fator de atrito
    """
    # Colebrook White funciona bem para Re>4000, entre 2300 e 4000 é uma zona de instabilidade
    # Mas pode ser utilizado com o devido cuidado
    if Re > 2300:
        f = f_init
        for i in range(max_iter):
            lhs = 1.0 / np.sqrt(f)
            rhs = -2.0 * np.log10((epsilon / (3.7 * D)) + (2.51 / (Re * np.sqrt(f))))
            f_new = 1.0 / (rhs ** 2)

            if abs(f - f_new) < tol:
                return f_new
            f = f_new
    else:
        f = 64 / Re
        print(f"Fator de atrito (Laminar): {f:.5f}")

    raise RuntimeError("Não convergiu dentro do número máximo de iterações")

def perda_de_carga(L, D, u, f, rho):
    """
    Calcula a perda de carga em um tubo circular.

    Parâmetros:
    L : float - comprimento do tubo [m]
    D : float - diâmetro interno do tubo [m]
    u : float - velocidade média [m/s]
    f_atrito : float - fator de atrito
    rho : float - densidade [m]
    Retorno:
    delta_p : float - perda de carga [Pa]
    """
    # Cálculo da perda de carga (Pa)
    return f * (L / D) * (rho * u**2 / 2)

densidade = 925 # kg/m³
mu = 0.0945 # Pa.s
D_int_pol = 24 #poleg
D_int_m = 24*2.54/100 #poleg

vazao_volumetrica = 0.59 # m³/s
vazao_massica = vazao_volumetrica*densidade  # kg/s

# Área da seção transversal
A = np.pi * (D_int_m / 2)**2

# Velocidade média do fluido no tubo (m/s)
velocidade = vazao_volumetrica / A

Re = Reynolds(rho=densidade,u=velocidade,D=D_int_m,mu=mu)
c = f_atrito(Re, D=D_int_m, epsilon = 45e-6, f_init=0.02, tol=1e-6, max_iter=100)


d = perda_de_carga(L=1, D = D_int_m , u=velocidade, f=c, rho=densidade)



a=2




