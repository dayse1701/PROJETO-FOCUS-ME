# ============================================
# FocusMe - Ferramenta de Produtividade Pessoal 
# Desenvolvido por: Dayse Gomes
# ============================================

import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

ARQUIVO_TAREFAS = "tarefas.json"

# --------------------------------------------
# Funções de persistência
# --------------------------------------------
def carregar_tarefas():
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(tarefas, f, indent=4, ensure_ascii=False)

# --------------------------------------------
# Funções do sistema
# --------------------------------------------
def atualizar_lista():
    lista_tarefas.delete(0, tk.END)
    for t in tarefas:
        status = "✅" if t["concluida"] else "❌"
        lista_tarefas.insert(tk.END, f"{status} {t['nome']}")

def adicionar_tarefa():
    nome = entrada_tarefa.get().strip()
    if nome:
        tarefas.append({"nome": nome, "concluida": False})
        salvar_tarefas()
        entrada_tarefa.delete(0, tk.END)
        atualizar_lista()
    else:
        messagebox.showwarning("Aviso", "O nome da tarefa não pode estar vazio.")

def concluir_tarefa():
    selecao = lista_tarefas.curselection()
    if not selecao:
        messagebox.showinfo("Info", "Selecione uma tarefa para marcar como concluída.")
        return

    indice = selecao[0]
    tarefas[indice]["concluida"] = True
    salvar_tarefas()
    atualizar_lista()

def excluir_tarefa():
    selecao = lista_tarefas.curselection()
    if not selecao:
        messagebox.showinfo("Info", "Selecione uma tarefa para excluir.")
        return

    indice = selecao[0]
    nome = tarefas[indice]['nome']

    confirmar = messagebox.askyesno("Confirmação", f"Deseja excluir a tarefa '{nome}'?")
    if confirmar:
        tarefas.pop(indice)
        salvar_tarefas()
        atualizar_lista()

def resumo_produtividade():
    total = len(tarefas)
    concluidas = sum(t["concluida"] for t in tarefas)
    if total == 0:
        messagebox.showinfo("Resumo", "Nenhuma tarefa cadastrada ainda.")
    else:
        porcentagem = (concluidas / total) * 100
        messagebox.showinfo(
            "Resumo de Produtividade",
            f"Tarefas totais: {total}\n"
            f"Tarefas concluídas: {concluidas}\n"
            f"Progresso: {porcentagem:.1f}%"
        )

# --------------------------------------------
# Interface Tkinter
# --------------------------------------------
janela = tk.Tk()
janela.title("FocusMe - Gerenciador de Tarefas")
janela.geometry("420x420")
janela.configure(bg="#f0f4f7")

# Campo de entrada
frame_superior = tk.Frame(janela, bg="#f0f4f7")
frame_superior.pack(pady=10)

entrada_tarefa = tk.Entry(frame_superior, width=30, font=("Arial", 12))
entrada_tarefa.pack(side=tk.LEFT, padx=5)

btn_adicionar = tk.Button(frame_superior, text="Adicionar", command=adicionar_tarefa, bg="#4CAF50", fg="white")
btn_adicionar.pack(side=tk.LEFT)

# Lista de tarefas
lista_tarefas = tk.Listbox(janela, width=55, height=15, font=("Arial", 10))
lista_tarefas.pack(pady=10)

# Botões de ação
frame_botoes = tk.Frame(janela, bg="#f0f4f7")
frame_botoes.pack(pady=5)

btn_concluir = tk.Button(frame_botoes, text="Concluir", command=concluir_tarefa, bg="#2196F3", fg="white", width=10)
btn_concluir.pack(side=tk.LEFT, padx=5)

btn_excluir = tk.Button(frame_botoes, text="Excluir", command=excluir_tarefa, bg="#f44336", fg="white", width=10)
btn_excluir.pack(side=tk.LEFT, padx=5)

btn_resumo = tk.Button(frame_botoes, text="Resumo", command=resumo_produtividade, bg="#9C27B0", fg="white", width=10)
btn_resumo.pack(side=tk.LEFT, padx=5)

# --------------------------------------------
# Execução
# --------------------------------------------
tarefas = carregar_tarefas()
atualizar_lista()

janela.mainloop()


