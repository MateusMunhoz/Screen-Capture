import tkinter as tk
import tkinter.font as tkfont
import subprocess
import os
import sys
from pynput import keyboard
from PIL import Image, ImageTk
from tkinter import messagebox
import time

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Print Timer")
        self.root.geometry("400x140+960+540")
        self.root.wm_attributes('-topmost', True)
        self.root.configure(bg='#2b2b2b')

        fonte_padrao = tkfont.nametofont("TkDefaultFont")
        fonte_padrao.configure(family="JetBrains Mono", size=10)
        self.root.option_add("*Font", fonte_padrao)

        self.label = tk.Label(
            self.root, text="Lembra de tirar| F8",
            font=("JetBrains Mono", 14), fg="#ffffff", bg='#2b2b2b'
        )
        self.label.pack(pady=6)

        self.btn = tk.Button(
            self.root, text="ATIVAR SCRIPT",
            bg="#3a3a3a", fg="#ffffff",
            activebackground="#555555", activeforeground="#ffffff",
            relief="flat", bd=0,
            command=self.abrir_popup
        )
        self.btn.pack(pady=2)


        self.seconds = 900
        self.alerta_ativo = False

        listener = keyboard.Listener(on_press=self.on_press)
        listener.daemon = True
        listener.start()

        self.root.mainloop()

    def exibir_mapa(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.janela_mapa = tk.Toplevel(self.root)
        self.janela_mapa.title("Mapa de Spawns")
        self.janela_mapa.wm_attributes('-topmost', True)
        self.janela_mapa.geometry("+20+20")
        self.janela_mapa.configure(bg='#2b2b2b')

        for nome in ["EsquerdaSpawns.png", "DireitaSpawns.png"]:
            caminho = os.path.join(script_dir, nome)
            if os.path.exists(caminho):
                img = Image.open(caminho)
                foto = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.janela_mapa, image=foto, bg='#2b2b2b')
                lbl.image = foto
                lbl.pack(side="left", padx=2)

    def on_press(self, key):
        if hasattr(key, 'name') and key.name == 'f8':
            self.root.after(0, self.abrir_popup)



    def abrir_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Spawn")
        popup.geometry("250x250+1500+120")
        popup.wm_attributes('-topmost', True)
        popup.configure(bg='#2b2b2b')

        def so_letras(texto):
            return texto =="" or not texto.isdigit()


        tk.Label(popup, text="Qual mapa voce está ?",
                 fg="#ffffff", bg='#2b2b2b').pack(pady=5)

        teste = popup.register(so_letras)
        entryMap = tk.Entry(popup,
            bg="#3a3a3a", fg="#ffffff", insertbackground="#ffffff",
            relief="flat",
            justify="center",
            validate = "key",
            validatecommand=(teste, "%P"))
        entryMap.pack(pady=2, padx=10, fill="x")
        entryMap.focus_set()

        def so_numeros(texto):
            return texto == "" or texto.isdigit()

        vcmd = popup.register(so_numeros)

        tk.Label(popup, text="Qual spawn voce pegou ?",
            fg="#ffffff", bg='#2b2b2b').pack(pady=5)

        entrySpawn = tk.Entry(popup,
            bg="#3a3a3a", fg="#ffffff", insertbackground="#ffffff",
            relief="flat", justify="center",
            validate="key", validatecommand=(vcmd, "%P"))
        entrySpawn.pack(pady=2, padx=10, fill="x")

        tk.Label(popup, text="Legenda de spawns",
            fg="#ffffff", bg='#2b2b2b').pack(pady=5)
        legenda = tk.Button(popup, text="Legenda", command=self.exibir_mapa, fg="#ffffff", bg='#2b2b2b')
        legenda.pack(pady=2)

        entryMap.bind("<Return>", lambda e: entrySpawn.focus_set())



        def confirmar():
            mapsInfo = {"CUSTOMS": 24, "SHORELINE":26, "WOODS": 28}
            spawn_str = entrySpawn.get()
            spawn_int = int(spawn_str)
            mapa = entryMap.get().upper()


            if mapa in mapsInfo and spawn_int <= mapsInfo[mapa]:
                self.rodar_script(spawn_str, mapa)
                tk.Label(popup, text="Tirando prints",fg="#ffffff", bg='#2b2b2b').pack(pady=5)
                popup.destroy()
            else:
                messagebox.showerror("Erro, spawn ou mapa invalido", f"Esse mapa só tem {mapsInfo[mapa]} spawns")


        entrySpawn.bind("<Return>", lambda e: confirmar())

        tk.Button(popup, text="OK",
            bg="#4a4a4a", fg="#ffffff",
            activebackground="#666666", activeforeground="#ffffff",
            relief="flat", command=confirmar).pack(pady=2)

    def rodar_script(self, spawn, mapa):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.root.withdraw()
        self.processo = subprocess.Popen(
            [sys.executable, os.path.join(script_dir, "pytorchTraining.py"), spawn, mapa],
            cwd=script_dir
        ) 
        self.root.after(500, self.verificar_processo)

    def verificar_processo(self):
        if self.processo.poll() is not None:
            self.root.destroy()
        else:
            self.root.after(500, self.verificar_processo)


if __name__ == "__main__":
    Overlay()
