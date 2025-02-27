import os
import json
import logging
from datetime import datetime
from tkinter import Tk, Label, Entry, Button, filedialog, Text, messagebox
import smtplib
from email.message import EmailMessage

# Configuração do log
logging.basicConfig(filename="email_automation.log", level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do arquivo de histórico
HISTORICO_ARQUIVO = "historico_envios.json"

# Função para salvar histórico
def salvar_historico(destinatario, assunto, status):
    historico = []
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r") as f:
            historico = json.load(f)
    historico.append({
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "destinatario": destinatario,
        "assunto": assunto,
        "status": status
    })
    with open(HISTORICO_ARQUIVO, "w") as f:
        json.dump(historico, f, indent=4)

# Função para exibir histórico
def exibir_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        with open(HISTORICO_ARQUIVO, "r") as f:
            historico = json.load(f)
        historico_texto = "\n".join([f"{h['data']} - {h['destinatario']} - {h['assunto']} - {h['status']}" for h in historico])
    else:
        historico_texto = "Nenhum histórico disponível."
    messagebox.showinfo("Histórico de Envios", historico_texto)

# Função para enviar e-mail
def enviar_email():
    try:
        email = entry_email.get()
        senha = entry_senha.get()
        destinatario = entry_destinatario.get()
        assunto = entry_assunto.get()
        mensagem = text_mensagem.get("1.0", "end")
        
        msg = EmailMessage()
        msg["From"] = email
        msg["To"] = destinatario
        msg["Subject"] = assunto
        msg.set_content(mensagem, subtype="html")
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, senha)
            server.send_message(msg)
        
        salvar_historico(destinatario, assunto, "Sucesso")
        messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
    except Exception as e:
        logging.error(f"Erro ao enviar e-mail: {str(e)}")
        salvar_historico(destinatario, assunto, "Falha")
        messagebox.showerror("Erro", f"Falha ao enviar e-mail: {str(e)}")

# Interface Gráfica
root = Tk()
root.title("Automação de E-mails")

Label(root, text="E-mail:").grid(row=0, column=0)
entry_email = Entry(root)
entry_email.grid(row=0, column=1)

Label(root, text="Senha:").grid(row=1, column=0)
entry_senha = Entry(root, show="*")
entry_senha.grid(row=1, column=1)

Label(root, text="Destinatário:").grid(row=2, column=0)
entry_destinatario = Entry(root)
entry_destinatario.grid(row=2, column=1)

Label(root, text="Assunto:").grid(row=3, column=0)
entry_assunto = Entry(root)
entry_assunto.grid(row=3, column=1)

Label(root, text="Mensagem:").grid(row=4, column=0)
text_mensagem = Text(root, height=5, width=40)
text_mensagem.grid(row=4, column=1)

Button(root, text="Enviar", command=enviar_email).grid(row=5, column=1)
Button(root, text="Ver Histórico", command=exibir_historico).grid(row=6, column=1)

root.mainloop()
