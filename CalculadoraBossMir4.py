import tkinter as tk
from tkinter import ttk
import os


def calcular_bosses(pedras):
    resultados = {}
    for andar, (req_grande, req_medio) in {
        "1f": ((40, 40), (20, 20)),
        "2f": ((50, 50), (25, 25)),
        "3f": ((12, 12), (7, 7)),
        "4f": ((15, 15), (8, 8)),
        "5f": ((8, 8), (4, 4)),
        "6f": ((10, 10), (5, 5)),
        "7f": ((12, 12), (6, 6)),
        "8f": ((14, 14), (7, 7)),
        "9f": ((17, 17), (9, 9)),
        "10f": ((20, 20), (11, 11)),
    }.items():
        if andar in ["1f", "2f"]:
            boss_grande = min(pedras['Azul']['Incomum'] // req_grande[0], pedras['Verde']['Incomum'] // req_grande[1])
            boss_medio = min(pedras['Amarela']['Incomum'] // req_medio[0], pedras['Vermelha']['Incomum'] // req_medio[1])
        elif andar in ["3f", "4f"]:
            boss_grande = min(pedras['Azul']['Rara'] // req_grande[0], pedras['Verde']['Rara'] // req_grande[1])
            boss_medio = min(pedras['Amarela']['Rara'] // req_medio[0], pedras['Vermelha']['Rara'] // req_medio[1])
        else:
            boss_grande = min(pedras['Azul']['Epica'] // req_grande[0], pedras['Verde']['Epica'] // req_grande[1])
            boss_medio = min(pedras['Amarela']['Epica'] // req_medio[0], pedras['Vermelha']['Epica'] // req_medio[1])

        resultados[andar] = (boss_grande, boss_medio)
    return resultados


def obter_dados_pedras(entries):
    cores = ['Amarela', 'Vermelha', 'Azul', 'Verde']
    raridades = ['Incomum', 'Rara', 'Epica']
    pedras = {cor: {raridade: 0 for raridade in raridades} for cor in cores}

    for cor in cores:
        for raridade in raridades:
            try:
                quantidade = int(entries[f"{cor}_{raridade}"].get())
                pedras[cor][raridade] = quantidade
            except ValueError:
                pedras[cor][raridade] = 0

    return pedras


def exibir_resultados(resultados, output_text, check_vars):
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Resultado:\n")
    output_text.insert(tk.END, "=" * 30 + "\n")

    for andar, (boss_grande, boss_medio) in resultados.items():
        if check_vars[andar].get():  # Exibir apenas se o checkbox estiver marcado
            output_text.insert(tk.END, f"{andar}: {boss_grande} Boss Grande, {boss_medio} Boss Médio\n")

    output_text.insert(tk.END, "=" * 30 + "\n")


def salvar_valores(entries):
    caminho_arquivo = os.path.abspath("valores_pedras.txt")
    with open(caminho_arquivo, "w") as file:
        for key, entry in entries.items():
            file.write(f"{key}:{entry.get()}\n")


def carregar_valores(entries):
    if os.path.exists("valores_pedras.txt"):
        with open("valores_pedras.txt", "r") as file:
            for line in file:
                key, value = line.strip().split(":")
                if key in entries:
                    entries[key].delete(0, tk.END)
                    entries[key].insert(0, value)


def main():
    root = tk.Tk()
    root.title("Calculadora de Bosses")

    def on_close():
        salvar_valores(entries)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Arquivo", menu=file_menu)
    file_menu.add_command(label="Salvar", command=lambda: salvar_valores(entries))
    file_menu.add_separator()
    file_menu.add_command(label="Sair", command=on_close)

    cores = ['Amarela', 'Vermelha', 'Azul', 'Verde']
    raridades = ['Incomum', 'Rara', 'Epica']
    raridade_cores = {"Incomum": "#5aab8f", "Rara": "#2f5586", "Epica": "#a62623"}
    entries = {}

    for i, cor in enumerate(cores):
        ttk.Label(root, text=cor).grid(row=i+1, column=0, padx=5, pady=5)
        for j, raridade in enumerate(raridades):
            ttk.Label(root, text=raridade).grid(row=0, column=j+1, padx=5, pady=5)
            entry = tk.Entry(root, width=5, bg=raridade_cores[raridade])  
            entry.grid(row=i+1, column=j+1, padx=5, pady=5)
            entries[f"{cor}_{raridade}"] = entry

    output_text = tk.Text(root, height=10, width=40)
    output_text.grid(row=6, column=0, columnspan=4, padx=5, pady=5)

    check_vars = {f"{i}f": tk.BooleanVar() for i in range(1, 11)}
    for idx, (andar, var) in enumerate(check_vars.items()):
        chk = ttk.Checkbutton(root, text=andar, variable=var)
        chk.grid(row=7 + idx // 4, column=idx % 4, padx=5, pady=2)

    def calcular():
        pedras = obter_dados_pedras(entries)
        resultados = calcular_bosses(pedras)
        exibir_resultados(resultados, output_text, check_vars)

    calcular_btn = ttk.Button(root, text="Calcular Bosses", command=calcular)
    calcular_btn.grid(row=5, column=0, columnspan=4, pady=10)

    carregar_valores(entries)

    selo_copyright = tk.Label(root, text="© 2025 Bruno - Todos os direitos reservados", font=("Arial", 8), fg="gray", cursor="hand2")
    selo_copyright.grid(row=11, column=0, columnspan=4, pady=(10, 5))
    selo_copyright.bind("<Button-1>", lambda e: os.system("start https://github.com/FBruno136"))

    root.mainloop()


if __name__ == "__main__":
    main()
