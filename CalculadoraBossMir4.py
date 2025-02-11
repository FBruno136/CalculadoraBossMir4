import tkinter as tk
from tkinter import ttk
import os


def calcular_bosses(pedras):
    resultados = {
        "1f": min(pedras['Amarela']['Incomum'] // 20, pedras['Vermelha']['Incomum'] // 20),
        "2f": min(pedras['Amarela']['Incomum'] // 25, pedras['Vermelha']['Incomum'] // 25),
        "3f": min(pedras['Amarela']['Rara'] // 7, pedras['Vermelha']['Rara'] // 7),
        "4f": min(pedras['Amarela']['Rara'] // 8, pedras['Vermelha']['Rara'] // 8),
        "5f": min(pedras['Amarela']['Epica'] // 4, pedras['Vermelha']['Epica'] // 4),
        "6f": min(pedras['Amarela']['Epica'] // 5, pedras['Vermelha']['Epica'] // 5),
        "7f": min(pedras['Amarela']['Epica'] // 6, pedras['Vermelha']['Epica'] // 5),
        "8f": min(pedras['Amarela']['Epica'] // 7, pedras['Vermelha']['Epica'] // 5),
        "9f": min(pedras['Amarela']['Epica'] // 9, pedras['Vermelha']['Epica'] // 9),
        "10f": min(pedras['Amarela']['Epica'] // 11, pedras['Vermelha']['Epica'] // 11),
    }
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
    
    for andar, quantidade in resultados.items():
        if check_vars[andar].get():  # Exibir apenas se o checkbox estiver marcado
            output_text.insert(tk.END, f"Andar {andar}: {quantidade} Boss(es)\n")

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
            entry = tk.Entry(root, width=5, bg=raridade_cores[raridade])  # Alterado para tk.Entry
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

    root.mainloop()


if __name__ == "__main__":
    main()
