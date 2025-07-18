import numpy as np
from funcoes_auxiliares import velocidade_especifica, B_water_known, C_q_water_known, C_H_water_known, C_BEp_H_water_known, C_H_water_known, C_eta_water_known, eta_vis_water_known, H_Vis_water_known, potencia_water_known

"""
Para este arquivo será resolvido o exemplo 01 do manual onde as informações da bomba operando com água são conhecidas
"""

Q_BEP_W = 110.0 #[m³/h]
H_total = 77 #[m]
N = 2950 #[RPM]
eta_W = 0.68
Visc = 120 #[cSt]
gravity_specific = 0.9

#1º Passo : Bomba é single ou multi estágio? Single
#2° Passo : Qual a rotação específica da bomba? Em unidades métricas <= 60
n_s = velocidade_especifica(N = N,Q_BEP_W = Q_BEP_W/3600,H_BEP_W = H_total)
if n_s <= 60:
    print("A velocidade específica da bomba está dentro do intervalo válido (<60), n_s =",n_s)
else:
    print("A velocidade específica da bomba fora dentro do intervalo válido (<60), n_s =",n_s)
#3° Passo: O Fluído em comportamento Newtoniano? Sim
#4° Passo: A viscosidade cinemática se encontra entre 1 e 4000 cSt? Sim

##Com os passos aprovados podemos determinar a performance da bomba

#1º Calcular o parâmetro B
B = B_water_known (V_vis=Visc, Q_BEP_W = Q_BEP_W,H_BEP_W=H_total,N=N)
if B >= 40:
    print("B da bomba está fora do intervalo válido (<40), B=",B)
else:
    print("B da bomba está dentro do intervalo válido (<40), B=",B)

#2° Calcular os efeitos de correção para a influência da viscosidade
if B <=1.0:
    C_q = 1.0
    C_h = 1.0
    C_eta = 1.0
else:
    C_q = C_q_water_known(B)
    Q_W = 1 * Q_BEP_W
    Q_Visc = Q_W*C_q
    C_BEP_H = C_BEp_H_water_known(C_q)
    C_h = C_H_water_known(C_BEp_H =C_BEP_H ,Q_W = Q_W,Q_BEP_W = Q_BEP_W)
    H_Visc = H_Vis_water_known(C_H = C_h,H_W = H_total)
    C_eta = C_eta_water_known(B)
    eta_vis = eta_vis_water_known(C_eta, eta_W)
    P = potencia_water_known(Q_vis =Q_Visc ,H_vis_total = H_Visc,s=gravity_specific,eta_vis=eta_vis)

a=2