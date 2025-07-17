import numpy as np


def velocidade_especifica(N,Q_BEP_W,H_BEP_W):
    """
    Compara o tipo de bomba de acordo com sua geometria e desempenho (centrífuga, axial, mista etc.), independentemente do tamanho
    :param N: Rotação da bomba [rad/s]
    :param Q_BEP_W: Vazão no ponto de melhor eficiência sendo água o fluido [m³/s]
    :param H_BEP_W: Altura de coluna de fluido no ponto de melhor eficiencia sendo água o fluido [m]
    :return: Velocidade especifica
    """
    return (N * (Q_BEP_W**0.5)) / (H_BEP_W**0.75)

def B_water_known (V_vis,Q_BEP_W,H_BEP_W,N):
    """
    O parâmetro B é utilizado como uma forma normalizada do número de Reynolds da bomba para corrigir a influência da viscosidade
    :param V_vis: Viscosidade cinemática [cSt] do fluid viscoso
    :param Q_BEP_W: Q_BEP_W: Vazão no ponto de melhor eficiência sendo água o fluido [m³/h]
    :param H_BEP_W: Altura de coluna de fluido no ponto de melhor eficiencia sendo água o fluido [m]
    :param N: Rotação [rpm]
    :return: B
    """
    return (16.5 * V_vis**0.5 * H_BEP_W**0.0625)/(Q_BEP_W**0.375 * N**0.25)

def C_q_water_known(B):
    """
    Fator de correção para a vazão
    :param B: Parametro adimensional previamente calculado
    :return: C_q
    """
    return  2.71**((-0.165*np.log10(B))**3.15)

def Q_vis_water_known(C_q,Q_w):
    """
    Essa função retorna a vazão corrigida para o fluido viscoso
    :param C_q:
    :param Q_w:
    :return:
    """
    return Q_w * C_q

def C_BEp_H_water_known(C_q):
    """
    Nesse caso o fator de correção para o ponto de melhor eficiência é o próprio C_q
    :param C_q: Adimensional previamente calculado
    :return: C_BEp_H
    """
    return C_q

def H_BEp_H_water_known(C_BEp_H,H_BEP_W):
    return C_BEp_H*H_BEP_W

def C_H_water_known(C_BEp_H,Q_W,Q_BEP_W):
    """
    Calcular o fator de correção para a altura de liquido
    :param C_BEp_H:
    :param Q_W:
    :param Q_BEP_W:
    :return:
    """
    return 1 - ((1-C_BEp_H)*(Q_W/Q_BEP_W)**0.75)

def H_Vis_water_known(C_H,H_W):
    """
    Calcula a altura manométrica corrigida para a bomba
    :param C_H: Parametro adimensional previamente calculado
    :param H_W: Altura Manométrica para operação com água
    :return: altura manométrica corrigida para a bomba
    """
    return C_H*H_W

def C_eta_water_known(B):
    """
    Fator de correção para a eficiêcia
    :param B: Adimensional previamente calculado
    :return: Fator de correção para a eficiência com o liquido viscoso
    """
    return B**(-0.0547*B**0.69)

def eta_vis_water_known(C_eta, eta_W):
    """

    :param C_eta:
    :param eta_W:
    :return:
    """

    return C_eta*eta_W

def potencia_water_known(Q_vis,H_vis_total,s,eta_vis):
    """

    :param Q_vis:
    :param H_vis_total:
    :param s:
    :param eta_vis:
    :return:
    """
    return (Q_vis*H_vis_total*s)/(367*eta_vis)


def B_operation_known(V_vis, Q_vis, H_vis):
    """

    :param V_vis:
    :param Q_vis:
    :param H_vis:
    :return:

    """
    return (2.8 * V_vis ** 0.5) / (Q_vis ** 0.25 * H_vis ** 0.125)


def C_q_operation_known(B):
    """
    Fator de correção para a vazão
    :param B: Parametro adimensional previamente calculado
    :return: C_q
    """
    return 2.71 ** ((-0.165 * np.log10(B)) ** 3.15)

def C_h_operation_known(B):
    """
    Fator de correção para a vazão
    :param B: Parametro adimensional previamente calculado
    :return: C_q
    """
    return 2.71 ** ((-0.165 * np.log10(B)) ** 3.15)


def Q_w_operation_known(C_q, Q_vis):
    """
    Essa função retorna a vazão corrigida para o fluido viscoso
    :param C_q:
    :param Q_w:
    :return:
    """
    return Q_vis / C_q

def Q_H_operation_known(C_H, H_vis):
    """
    Essa função retorna a vazão corrigida para o fluido viscoso
    :param C_q:
    :param Q_w:
    :return:
    """
    return H_vis/ C_H

def C_eta_operation_known(B):
    """
    Fator de correção para a eficiêcia
    :param B: Adimensional previamente calculado
    :return: Fator de correção para a eficiência com o liquido viscoso
    """
    return B ** (-0.0547 * B ** 0.69)


def eta_vis_operation_known(C_eta, eta_W):
    """

    :param C_eta:
    :param eta_W:
    :return:
    """

    return C_eta * eta_W


def potencia_operation_known(Q_vis, H_vis_total, s, eta_vis):
    """

    :param Q_vis:
    :param H_vis_total:
    :param s:
    :param eta_vis:
    :return:
    """
    return (Q_vis * H_vis_total * s) / (367 * eta_vis)

def C_NPSH