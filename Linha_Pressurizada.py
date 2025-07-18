import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from perda_de_carga import Reynolds, f_atrito, perda_de_carga

def salvar_plot(entrada, saida, nome_arquivo="relatorio_escoamento"):
    Path("plots").mkdir(exist_ok=True)
    caminho = Path("plots") / f"{nome_arquivo}.png"

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis("off")

    linhas = ["== Dados de Entrada =="] + entrada + [""] + ["== Resultados Calculados =="] + saida
    for i, linha in enumerate(linhas):
        ax.text(0.05, 1 - i * 0.07, linha, fontsize=11, va='top')

    plt.tight_layout()
    fig.savefig(caminho, dpi=300)
    plt.close()
    messagebox.showinfo("Sucesso", f"Imagem salva em {caminho}")

def calcular():
    try:
        g = float(entry_g.get())
        mu = float(entry_mu.get())
        rho = float(entry_rho.get())
        P_nominal = float(entry_P_nominal.get())
        P_minima = float(entry_P_minima.get())
        divisor = float(entry_divisor.get())
        Q_m3h = float(entry_Q.get())
        D_polegadas = float(entry_D.get())
        rugosidade = float(entry_eps.get())
    except ValueError:
        messagebox.showerror("Erro", "Insira todos os valores corretamente.")
        return

    Q_m3s = Q_m3h / 3600
    D_m = D_polegadas * 2.54 / 100
    A = np.pi * (D_m / 2) ** 2
    u = Q_m3s / A
    vazao_massica = Q_m3s * rho

    Re = Reynolds(rho=rho, u=u, D=D_m, mu=mu)
    f = f_atrito(Re=Re, D=D_m, epsilon=rugosidade, f_init=0.02, tol=1e-6, max_iter=100)
    delta_P_max = P_nominal - P_minima
    perda_por_metro = perda_de_carga(L=1, D=D_m, u=u, f=f, rho=rho)
    L = (delta_P_max / divisor) / perda_por_metro
    H = (delta_P_max / divisor) / (rho * g)

    entrada = [
        f"Gravidade: {g} m/s²",
        f"Viscosidade dinâmica: {mu} Pa·s",
        f"Densidade: {rho} kg/m³",
        f"P_nominal: {P_nominal/1e5:.2f} bar",
        f"P_minima: {P_minima/1e5:.2f} bar",
        f"ΔP/divisor: {divisor}",
        f"Vazão volumétrica: {Q_m3h} m³/h",
        f"Diâmetro interno: {D_polegadas} pol = {D_m:.4f} m",
        f"Rugosidade: {rugosidade} m"
    ]

    saida = [
        f"Reynolds: {Re:.2e}",
        f"Fator de atrito (f): {f:.5f}",
        f"Perda por metro: {perda_por_metro:.2f} Pa/m",
        f"Comprimento total (L): {L:.2f} m",
        f"Altura manométrica (H): {H:.2f} m",
        f"Vazão mássica: {vazao_massica:.2f} kg/s",
        f"Velocidade média: {u:.2f} m/s"
    ]

    # Salvar os dados para exportação
    calcular.entrada = entrada
    calcular.saida = saida

    messagebox.showinfo("Resultados", "\n".join(saida))

def salvar_com_nome():
    nome = entry_nome_arquivo.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Digite um nome de arquivo para salvar.")
        return
    if not hasattr(calcular, 'entrada') or not hasattr(calcular, 'saida'):
        messagebox.showwarning("Atenção", "Calcule primeiro antes de salvar.")
        return
    salvar_plot(calcular.entrada, calcular.saida, nome)

root = tk.Tk()
root.title("Cálculo de Escoamento em Tubulação")

frame = ttk.Frame(root, padding=12)
frame.grid()

labels = [
    ("Gravidade [m/s²]:", "9.81"),
    ("Viscosidade dinâmica μ [Pa·s]:", "0.0945"),
    ("Densidade ρ [kg/m³]:", "945"),
    ("Pressão nominal [Pa]:", "1000000"),
    ("Pressão mínima [Pa]:", "520000"),
    ("Coeficiente divisor (ΔP/div):", "2"),
    ("Vazão volumétrica [m³/h]:", "2124"),
    ("Diâmetro interno [pol]:", "24"),
    ("Rugosidade absoluta [m]:", "0.000045"),
]

entries = []
for i, (text, default) in enumerate(labels):
    ttk.Label(frame, text=text).grid(row=i, column=0, sticky="w")
    entry = ttk.Entry(frame)
    entry.insert(0, default)
    entry.grid(row=i, column=1)
    entries.append(entry)

(entry_g, entry_mu, entry_rho, entry_P_nominal, entry_P_minima,
 entry_divisor, entry_Q, entry_D, entry_eps) = entries

ttk.Label(frame, text="Nome do arquivo (sem extensão):").grid(row=len(labels), column=0, sticky="w")
entry_nome_arquivo = ttk.Entry(frame)
entry_nome_arquivo.grid(row=len(labels), column=1)

ttk.Button(frame, text="Calcular", command=calcular).grid(row=len(labels)+1, columnspan=2, pady=6)
ttk.Button(frame, text="Salvar Plot", command=salvar_com_nome).grid(row=len(labels)+2, columnspan=2)

root.mainloop()