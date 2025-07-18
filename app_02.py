import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

from funcoes_auxiliares import (
    B_operation_known, C_q_operation_known, C_h_operation_known,
    Q_w_operation_known, H_w_operation_known,
    C_eta_operation_known, eta_vis_operation_known,
    potencia_operation_known
)

def salvar_plot(entrada, saida, nome_arquivo="relatorio_plot"):
    # Garante que a pasta plots existe
    pasta_plots = Path("plots")
    pasta_plots.mkdir(exist_ok=True)

    caminho_arquivo = pasta_plots / f"{nome_arquivo}.png"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # remove os eixos

    # Texto formatado
    linhas = ["== Dados de Entrada =="] + entrada + [""] + ["== Resultados da Correção =="] + saida

    for i, linha in enumerate(linhas):
        ax.text(0.05, 1 - i * 0.07, linha, fontsize=11, va='top')

    plt.tight_layout()
    fig.savefig(caminho_arquivo, dpi=300)
    plt.close(fig)
    messagebox.showinfo("Imagem Salva", f"Gráfico salvo como '{caminho_arquivo}'")

def calcular():
    try:
        Q_vis = float(entry_q_vis.get())
        H_vis = float(entry_h_vis.get())
        Visc = float(entry_visc.get())
        s = float(entry_s.get())
        eta_W = float(entry_eta_w.get()) / 100  # converte de % para decimal
    except ValueError:
        messagebox.showerror("Erro", "Digite todos os valores corretamente.")
        return

    B = B_operation_known(V_vis=Visc, Q_vis=Q_vis, H_vis=H_vis)

    if B >= 40:
        messagebox.showwarning("Aviso", f"Parâmetro B fora do intervalo permitido (<40). B = {B:.2f}")
        return

    if not (1 <= Visc <= 4000):
        messagebox.showwarning("Aviso", "Viscosidade fora do intervalo permitido (1 a 4000 cSt)")
        return

    if B <= 1.0:
        C_q = C_h = C_eta = 1.0
    else:
        C_q = C_q_operation_known(B)
        C_h = C_h_operation_known(B)
        C_eta = C_eta_operation_known(B)

    Q_w = Q_w_operation_known(C_q, Q_vis)
    H_w = H_w_operation_known(C_h, H_vis)
    eta_vis = eta_vis_operation_known(C_eta, eta_W)
    P = potencia_operation_known(Q_vis, H_vis_total=H_vis, s=s, eta_vis=eta_vis)

    saida = [
        f"Parâmetro B: {B:.2f}",
        f"Vazão corrigida com água: {Q_w:.2f} m³/h",
        f"Altura corrigida com água: {H_w:.2f} m",
        f"Eficiência com viscosidade: {eta_vis*100:.2f} %",
        f"Potência com viscosidade: {P:.2f} W"
    ]

    entrada = [
        f"Vazão (com viscosidade): {Q_vis} m³/h",
        f"Altura manométrica: {H_vis} m",
        f"Viscosidade: {Visc} cSt",
        f"Peso específico relativo: {s}",
        f"Eficiência com água: {eta_W*100:.2f} %"
    ]

    # Armazena para salvar depois
    calcular.entrada = entrada
    calcular.saida = saida

    messagebox.showinfo("Resultados", '\n'.join(saida))

def salvar_com_nome():
    nome = entry_nome_arquivo.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Digite um nome de arquivo.")
        return

    if not hasattr(calcular, 'entrada') or not hasattr(calcular, 'saida'):
        messagebox.showwarning("Aviso", "Você precisa calcular antes de salvar o plot.")
        return

    salvar_plot(calcular.entrada, calcular.saida, nome)

# GUI
root = tk.Tk()
root.title("Correção a partir de operação com fluido viscoso")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Vazão com viscosidade [m³/h]:").grid(row=0, column=0)
entry_q_vis = ttk.Entry(frame)
entry_q_vis.grid(row=0, column=1)

ttk.Label(frame, text="Altura manométrica [m]:").grid(row=1, column=0)
entry_h_vis = ttk.Entry(frame)
entry_h_vis.grid(row=1, column=1)

ttk.Label(frame, text="Viscosidade [cSt] (1 a 4000):").grid(row=2, column=0)
entry_visc = ttk.Entry(frame)
entry_visc.grid(row=2, column=1)

ttk.Label(frame, text="Peso específico relativo:").grid(row=3, column=0)
entry_s = ttk.Entry(frame)
entry_s.grid(row=3, column=1)

ttk.Label(frame, text="Eficiência com água (%):").grid(row=4, column=0)
entry_eta_w = ttk.Entry(frame)
entry_eta_w.grid(row=4, column=1)

ttk.Label(frame, text="Nome do arquivo de saída (sem extensão):").grid(row=5, column=0)
entry_nome_arquivo = ttk.Entry(frame)
entry_nome_arquivo.grid(row=5, column=1)

ttk.Button(frame, text="Calcular Correção", command=calcular).grid(row=6, columnspan=2, pady=10)
ttk.Button(frame, text="Salvar Plot", command=salvar_com_nome).grid(row=7, columnspan=2, pady=5)

root.mainloop()
