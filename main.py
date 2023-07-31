import subprocess
import re
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox


def clean_non_ascii(text): # Substitui os caracteres non-ASCII para evitar erros
    return ''.join(char if ord(char) < 128 else 'e' for char in text)

def center_window(window): # Centraliza a janela da UI
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def resultado(media): # Define a conclusão do resultado
    value = int(media[:-2])

    if value <= 5:
        return "Super Rápido"
    elif value < 15:
        return "Rápido"
    elif value < 50:
        return "Médio"
    elif value < 80:
        return "Lento"
    elif value < 100:
        return "Muito Lento"
    elif value > 100:
        return "Inutilizavel"

def ping_ip(): # Testa a conexão entre os PCs
    ip_address = ip_entry.get().strip()
    package_count = package_count_entry.get()
    output_file = "ping_results.txt"

    # Checa se a quantidade de pacotes está vazia
    if not package_count:
        package_count = "4"

    # Coloca uma mensagem the log e a atualiza
    sending_label.config(text=f"Enviando {package_count} pacotes de dados ao \n endereço IP {ip_address}...")
    sending_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    app.update_idletasks()

    # Pattern para identificar a Media
    pattern = r"Media = (\d+ms)"

    try: # Manda os pings e grava o resultado em um arquivo
        result = subprocess.run(["ping", ip_address, "-n", package_count], capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        cleaned_output = clean_non_ascii(result.stdout)
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(cleaned_output)
    except subprocess.CalledProcessError as e: # Tratamento de erro
        messagebox.showerror("Ping Failed", f"Ping failed with error: {e}")
        sending_label.place_forget()  # Remove the sending label
        return

    # Lê e armazena o resultado do ping
    with open(output_file, "r", encoding="utf-8") as file:
        response = file.read()

    # Identifica o valor "Média"
    value = re.search(pattern, response)

    if value:
        media_value = value.group(1)
        sending_label.config(text=f"Ping para {ip_address} concluído! Aguarde o resultado...")
        sending_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Display the label again
        app.update()
        # Mostra um pop-up com o resultado da operação
        app.after(100, lambda: messagebox.showinfo("Resultado do Teste", f"Latência Média do IP [{ip_address}]: {media_value} \n \nConclusão: {resultado(media_value)}"))
    else:
        messagebox.showerror("Error", "Ocorreu um erro, latência média não encontrada.")

    # Remove o texto de log
    sending_label.place_forget()


# Define as propriedades da UI
app = tk.Tk()
app.title("Medidor de Latência")
app.geometry("500x250")
app.resizable(False, False)
app.iconbitmap("MyIcon.ico")
MyFont = font.Font(family='Mona-Sans-Bold', size=14)

center_window(app) # Centraliza a janela

# Input para o endereço IP
ip_label = tk.Label(app, text="Insira o endereço IP:", font=MyFont, relief=tk.GROOVE)
ip_label.pack(pady=8)
ip_entry = tk.Entry(app)
ip_entry.pack()

# Input para a quantidade de pacotes
package_count_label = tk.Label(app, text="Insira a quantidade de pacotes a serem enviados:", font=MyFont)
package_count_label.pack(pady=5)
package_count_entry = tk.Entry(app)
package_count_entry.pack()

# Texto de log
sending_label = tk.Label(app, text="", fg="blue", font=MyFont)

# Botão Iniciar
ping_button = tk.Button(app, text="INICIAR", command=ping_ip, fg='#159703', font=MyFont, padx=4, pady=2, height=1, width=8, borderwidth=3, relief=tk.SOLID)
ping_button.pack(side=tk.BOTTOM, pady=10)  # Add vertical padding of 10 between the button and the elements below it

app.mainloop()
