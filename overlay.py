import tkinter as tk
import subprocess
import os
import sys
from pynput import keyboard
from PIL import Image, ImageTk

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Print Timer")
        self.root.geometry("220x90+1400+20")
        self.root.wm_attributes('-topmost', True)
        self.root.configure(bg='#2b2b2b')

        self.label = tk.Label(
            self.root, text="Proximo: 15:00 | F8",
            font=("Consolas", 14), fg="#ffffff", bg='#2b2b2b'
        )
        self.label.pack(pady=6)

        self.btn = tk.Button(
            self.root, text="ATIVAR SCRIPT",
            font=("Consolas", 11, "bold"),
            bg="#3a3a3a", fg="#ffffff",
            activebackground="#555555", activeforeground="#ffffff",
            relief=tk.FLAT, bd=0,
            command=self.abrir_popup
        )
        self.btn.pack(pady=2)

        self.seconds = 900
        self.alerta_ativo = False

        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()

        self.exibir_mapa()
        self.contagem()
        self.root.mainloop()

    def exibir_mapa(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.janela_mapa = tk.Toplevel(self.root)
        self.janela_mapa.title("Mapa de Spawns")
        self.janela_mapa.wm_attributes('-topmost', True)
        self.janela_mapa.geometry("+20+20")
        self.janela_mapa.configure(bg='#2b2b2b')

        for nome in ["DireitaSpawns.png", "EsquerdaSpawns.png"]:
            caminho = os.path.join(script_dir, nome)
            if os.path.exists(caminho):
                img = Image.open(caminho)
                foto = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.janela_mapa, image=foto, bg='#2b2b2b')
                lbl.image = foto
                lbl.pack(side=tk.LEFT, padx=2)

    def on_press(self, key):
        if hasattr(key, 'name') and key.name == 'f8':
            self.root.after(0, self.abrir_popup)

    def contagem(self):
        mins, secs = divmod(self.seconds, 60)
        self.label.config(text=f"Proximo: {mins}:{secs:02d}")

        if self.seconds <= 0:
            if not self.alerta_ativo:
                self.label.config(text="APERTE AGORA!", fg="#ff4444")
                self.root.configure(bg='#661111')
                self.label.configure(bg='#661111')
                self.btn.configure(bg='#cc3333', text=">>> ATIVAR <<<")
                self.alerta_ativo = True
        else:
            self.seconds -= 1

        self.root.after(1000, self.contagem)

    def abrir_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Spawn")
        popup.geometry("200x90+1500+120")
        popup.wm_attributes('-topmost', True)
        popup.configure(bg='#2b2b2b')

        tk.Label(popup, text="Qual spawn voce pegou?",
                 font=("Consolas", 10), fg="#ffffff", bg='#2b2b2b').pack(pady=5)

        entry = tk.Entry(popup, font=("Consolas", 12),
                         bg="#3a3a3a", fg="#ffffff", insertbackground="#ffffff",
                         relief=tk.FLAT, justify="center")
        entry.pack(pady=2, padx=10, fill="x")
        entry.focus_set()

        def confirmar():
            spawn = entry.get()
            popup.destroy()
            self.rodar_script(spawn)


        entry.bind("<Return>", lambda e: confirmar())

        tk.Button(popup, text="OK", font=("Consolas", 10, "bold"),
                  bg="#4a4a4a", fg="#ffffff",
                  activebackground="#666666", activeforeground="#ffffff",
                  relief=tk.FLAT, command=confirmar).pack(pady=2)

    def rodar_script(self, spawn):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(
            [sys.executable, os.path.join(script_dir, "pytorchTraining.py"), spawn],
            cwd=script_dir
        )
        self.seconds = 900
        self.alerta_ativo = False
        self.label.config(text="Proximo: 5:00", fg="#ffffff")
        self.root.configure(bg='#2b2b2b')
        self.label.configure(bg='#2b2b2b')
        self.btn.configure(bg='#3a3a3a', text="ATIVAR SCRIPT")


if __name__ == "__main__":
    Overlay()
