import tkinter as tk
from tkinter import ttk
import subprocess
import socket
import sys

class App:
    def __init__(self, master):
        self.master = master
        master.title("NetProject Interface")
        master.geometry("400x200")
        master.configure(bg="#FFFFFF")  # Couleur de fond en blanc

        # Configuration du style des widgets
        self.style = ttk.Style()

        # Supprimer les bordures des cadres et des boutons
        self.style.configure('TFrame', background='#FFFFFF', borderwidth=0)
        self.style.configure('TButton', font=('Helvetica', 12), borderwidth=0)
        self.style.configure('TLabel', font=('Helvetica', 12), borderwidth=0)

        self.frame = ttk.Frame(master)
        self.frame.pack(pady=20)

        self.label = ttk.Label(self.frame, text="Bienvenue dans NetProject !")
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.run_button = ttk.Button(self.frame, text="Lancer l'application", command=self.run_flask_app)
        self.run_button.grid(row=1, column=0, pady=10)

        self.ip_label = ttk.Label(self.frame, text="")
        self.ip_label.grid(row=1, column=1, pady=10)

        self.close_button = ttk.Button(self.frame, text="Fermer", command=self.close_application)
        self.close_button.grid(row=2, column=0, columnspan=2, pady=10)

        master.protocol("WM_DELETE_WINDOW", self.close_application)

        self.process = None  # Pour stocker le processus Flask

    def run_flask_app(self):
        self.get_ip_address()

        # Lancer l'application Flask avec les paramètres suivants
        self.process = subprocess.Popen(["flask", "run", "--debug", "--host=0.0.0.0"])

    def get_ip_address(self):
        ip_address = socket.gethostbyname(socket.gethostname())
        self.ip_label.config(text=f"Adresse IP: {ip_address}:5000")

    def close_application(self):
        if self.process:
            self.process.terminate()  # Terminer le processus Flask
        self.master.destroy()  # Fermer la fenêtre principale
        sys.exit()  # Quitter le programme

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
