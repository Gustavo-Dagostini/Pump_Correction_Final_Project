"""
Para esse exemplo são fornecidos a altura manometrica desejada, a vazão e a viscodidade
"""
from funcoes_auxiliares import B_operation_known, C_q_operation_known, C_h_operation_known, Q_w_operation_known, H_w_operation_known, C_eta_operation_known, eta_vis_operation_known, potencia_operation_known

Q_vis = 100.0 #[m³/h]
H_vis = 70.0 #[m]
Visc = 120 #[cSt]
s = 0.9
eta_BEP_w = 0.68

#1º Calcular o parâmetro B
B = B_operation_known(V_vis = Visc, Q_vis = Q_vis, H_vis=H_vis)
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
    C_q = C_q_operation_known(B)
    C_h = C_h_operation_known(B)
Q_W = Q_w_operation_known(C_q, Q_vis)
H_W = H_w_operation_known(C_h, H_vis)
C_eta = C_eta_operation_known(B)
eta_vis = eta_vis_operation_known(C_eta, eta_W=eta_BEP_w)
P = potencia_operation_known(Q_vis, H_vis_total=H_vis, s=s,eta_vis=eta_vis)

a=2