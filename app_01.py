import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from funcoes_auxiliares import (
    velocidade_especifica, B_water_known, C_q_water_known, C_H_water_known,
    C_BEp_H_water_known, C_eta_water_known, eta_vis_water_known,
    H_Vis_water_known, potencia_water_known
)

def calcular_e_plotar():
    try:
        nome_bomba = entry_nome_bomba.get().strip()
        if not nome_bomba:
            messagebox.showerror("Erro", "Informe o nome da bomba.")
            return

        Q_BEP_W = float(entry_q.get())
        H_total = float(entry_h.get())
        N = float(entry_n.get())
        eta_W = float(entry_eta.get()) / 100  # de % para decimal
        Visc = float(entry_visc.get())
        s = float(entry_s.get())
    except ValueError:
        messagebox.showerror("Erro", "Digite todos os valores corretamente.")
        return

    # Verificações
    n_s = velocidade_especifica(N=N, Q_BEP_W=Q_BEP_W/3600, H_BEP_W=H_total)
    if n_s > 60:
        messagebox.showwarning("Aviso", f"Velocidade específica fora do intervalo (<60). n_s = {n_s:.2f}")
        return

    if not (1 <= Visc <= 4000):
        messagebox.showwarning("Aviso", "Viscosidade fora do intervalo permitido (1 a 4000 cSt)")
        return

    B = B_water_known(V_vis=Visc, Q_BEP_W=Q_BEP_W, H_BEP_W=H_total, N=N)
    if B > 40:
        messagebox.showwarning("Aviso", f"B fora do intervalo permitido (<40). B = {B:.2f}")
        return

    ratios = np.arange(0.2, 1.6, 0.1)
    Q = ratios * Q_BEP_W

    H_corrigida = []
    eta_corrigida = []
    P_corrigida = []

    H_original = [H_total] * len(Q)
    eta_original = [eta_W] * len(Q)
    P_original = [potencia_water_known(q, H_total, s, eta_W) for q in Q]

    for ratio in ratios:
        Q_W = ratio * Q_BEP_W

        if B <= 1.0:
            C_q = C_h = C_eta = 1.0
        else:
            C_q = C_q_water_known(B)
            C_BEP_H = C_BEp_H_water_known(C_q)
            C_h = C_H_water_known(C_BEP_H, Q_W, Q_BEP_W)
            C_eta = C_eta_water_known(B)

        Q_visc = Q_W * C_q
        H_visc = H_Vis_water_known(C_h, H_total)
        eta_vis = eta_vis_water_known(C_eta, eta_W)
        P = potencia_water_known(Q_visc, H_visc, s, eta_vis)

        H_corrigida.append(H_visc)
        eta_corrigida.append(eta_vis)
        P_corrigida.append(P)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()

    ax1.plot(Q, H_original, '--', label='Altura (Agua)', color='blue')
    ax1.plot(Q, H_corrigida, '-o', label='Altura (Fluido)', color='blue')

    ax1.plot(Q, P_original, '--', label='Potência (Agua)', color='green')
    ax1.plot(Q, P_corrigida, '-o', label='Potência (Fluido)', color='green')

    ax2.plot(Q, np.array(eta_original) * 100, '--', label='Eficiência (Agua)', color='red')
    ax2.plot(Q, np.array(eta_corrigida) * 100, '-o', label='Eficiência (Fluido)', color='red')

    ax1.set_xlabel(r"Vazão $[m^3/h]$")
    ax1.set_ylabel(r"Altura Manométrica [m] ; Potência [kW]")
    ax2.set_ylabel(r"Eficiência $[\%]$")
    ax2.set_ylim(0, 100)

    ax1.grid(True)

    plt.subplots_adjust(right=0.75)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()

    fig.legend(lines1 + lines2, labels1 + labels2,
               loc='lower right', bbox_to_anchor=(0.95, 0.15), fontsize=9)

    textstr = '\n'.join((
        rf"Dados - {nome_bomba}",
        "",
        rf"$Q_{{\mathrm{{BEP}}}} = {Q_BEP_W:.1f}\ m^3/h$",
        rf"$H_{{\mathrm{{BEP}}}} = {H_total:.1f}\ m$",
        rf"$N = {N:.0f}\ RPM$",
        rf"$\eta = {eta_W * 100:.1f}\ \%$",
        rf"$\nu = {Visc:.1f}\ cSt$",
        rf"$s = {s:.2f}$",
        rf"$n_s = {n_s:.2f}$",
        rf"$B = {B:.2f}$"
    ))

    props = dict(boxstyle='round', facecolor='white', alpha=0.9, linewidth=1)
    ax1.text(1.1, 1.0, textstr, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top', bbox=props)

    plt.title("Curvas da Bomba (Original x Corrigida)", fontsize=14)

    output_dir = Path("plots")
    output_dir.mkdir(exist_ok=True)

    nome_limpo = nome_bomba.replace(" ", "_").replace("/", "_")

    nome_arquivo = output_dir / f"curvas_bomba_{nome_limpo}.pdf"
    plt.savefig(nome_arquivo, format='pdf')
    plt.show()

    messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{nome_arquivo.resolve()}")

root = tk.Tk()
root.title("Correção de Curva de Bomba por Viscosidade")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Nome da Bomba:").grid(row=0, column=0)
entry_nome_bomba = ttk.Entry(frame)
entry_nome_bomba.grid(row=0, column=1)

ttk.Label(frame, text="Vazão (Ponto de Melhor Eficiência [m³/h]):").grid(row=1, column=0)
entry_q = ttk.Entry(frame)
entry_q.grid(row=1, column=1)

ttk.Label(frame, text="Altura Manométrica Total [m]:").grid(row=2, column=0)
entry_h = ttk.Entry(frame)
entry_h.grid(row=2, column=1)

ttk.Label(frame, text="Rotação [RPM]:").grid(row=3, column=0)
entry_n = ttk.Entry(frame)
entry_n.grid(row=3, column=1)

ttk.Label(frame, text="Eficiência (%):").grid(row=4, column=0)
entry_eta = ttk.Entry(frame)
entry_eta.grid(row=4, column=1)

ttk.Label(frame, text="Viscosidade Cinemática (1-4000) [cSt]:").grid(row=5, column=0)
entry_visc = ttk.Entry(frame)
entry_visc.grid(row=5, column=1)

ttk.Label(frame, text="Peso Específico Relativo:").grid(row=6, column=0)
entry_s = ttk.Entry(frame)
entry_s.grid(row=6, column=1)

ttk.Button(frame, text="Gerar Gráfico", command=calcular_e_plotar).grid(row=7, columnspan=2, pady=10)

root.mainloop()
