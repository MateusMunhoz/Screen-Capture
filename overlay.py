import tkinter as tk
import tkinter.font as tkfont
import subprocess
import os
import sys
from pynput import keyboard
from PIL import Image, ImageTk
from tkinter import messagebox

# ---- Paleta ----
BG_MAIN   = "#1e1e2e"
BG_CARD   = "#2a2a3c"
ENTRY_BG  = "#3a3a52"
FG        = "#e8e8f0"
FG_DIM    = "#9a9ab0"
ACCENT    = "#7c6cf5"
ACCENT_HV = "#9184f8"
ERRO_BG   = "#3a1e28"
ERRO_FG   = "#ff5c7a"


def hover(widget, cor_hover, cor_normal):
    widget.bind("<Enter>", lambda e: widget.config(bg=cor_hover))
    widget.bind("<Leave>", lambda e: widget.config(bg=cor_normal))


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Print Timer")
        self.root.geometry("320x130+960+540")
        self.root.wm_attributes('-topmost', True)
        self.root.configure(bg=BG_MAIN)

        fonte_padrao = tkfont.nametofont("TkDefaultFont")
        fonte_padrao.configure(family="JetBrains Mono", size=10)
        self.root.option_add("*Font", fonte_padrao)

        card = tk.Frame(self.root, bg=BG_CARD, padx=16, pady=14)
        card.pack(expand=True, fill="both", padx=10, pady=10)

        self.label = tk.Label(
            card, text="Lembre de tirar  [F8]",
            font=("JetBrains Mono", 13, "bold"), fg=FG, bg=BG_CARD
        )
        self.label.pack(pady=(0, 10))

        self.btn = tk.Button(
            card, text="ATIVAR SCRIPT",
            font=("JetBrains Mono", 10, "bold"),
            bg=ACCENT, fg="#ffffff",
            activebackground=ACCENT_HV, activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            padx=18, pady=6,
            command=self.abrir_popup
        )
        self.btn.pack()
        hover(self.btn, ACCENT_HV, ACCENT)

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
        self.janela_mapa.configure(bg=BG_MAIN)

        for nome in ["EsquerdaSpawns.png", "DireitaSpawns.png"]:
            caminho = os.path.join(script_dir, nome)
            if os.path.exists(caminho):
                img = Image.open(caminho)
                foto = ImageTk.PhotoImage(img)
                lbl = tk.Label(self.janela_mapa, image=foto, bg=BG_MAIN)
                lbl.image = foto
                lbl.pack(side="left", padx=4, pady=4)

    def on_press(self, key):
        if hasattr(key, 'name') and key.name == 'f8':
            self.root.after(0, self.abrir_popup)

    def abrir_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Spawn")
        popup.geometry("280x300+1500+120")
        popup.wm_attributes('-topmost', True)
        popup.configure(bg=BG_MAIN)

        card = tk.Frame(popup, bg=BG_CARD, padx=16, pady=14)
        card.pack(expand=True, fill="both", padx=10, pady=10)

        def so_letras(texto):
            return texto == "" or not texto.isdigit()

        teste = popup.register(so_letras)

        tk.Label(card, text="Qual mapa você está?",
                 fg=FG_DIM, bg=BG_CARD).pack(pady=(4, 4))

        entryMap = tk.Entry(card,
            bg=ENTRY_BG, fg=FG, insertbackground=FG,
            relief="flat", justify="center",
            highlightthickness=1, highlightbackground=ENTRY_BG,
            highlightcolor=ACCENT,
            validate="key", validatecommand=(teste, "%P"))
        entryMap.pack(pady=2, padx=6, fill="x", ipady=4)
        entryMap.focus_set()

        def so_numeros(texto):
            return texto == "" or texto.isdigit()

        vcmd = popup.register(so_numeros)

        tk.Label(card, text="Qual spawn você pegou?",
                 fg=FG_DIM, bg=BG_CARD).pack(pady=(10, 4))

        entrySpawn = tk.Entry(card,
            bg=ENTRY_BG, fg=FG, insertbackground=FG,
            relief="flat", justify="center",
            highlightthickness=1, highlightbackground=ENTRY_BG,
            highlightcolor=ACCENT,
            validate="key", validatecommand=(vcmd, "%P"))
        entrySpawn.pack(pady=2, padx=6, fill="x", ipady=4)

        legenda = tk.Button(card, text="Ver legenda de spawns",
            font=("JetBrains Mono", 9),
            bg=BG_CARD, fg=FG_DIM,
            activebackground=BG_CARD, activeforeground=FG,
            relief="flat", bd=0, cursor="hand2",
            command=self.exibir_mapa)
        legenda.pack(pady=(10, 2))
        hover(legenda, BG_CARD, BG_CARD)

        entryMap.bind("<Return>", lambda e: entrySpawn.focus_set())

        def confirmar():
            mapsInfo = {"CUSTOMS": 24, "SHORELINE": 26, "WOODS": 28}
            spawn_str = entrySpawn.get()
            spawn_int = int(spawn_str)
            mapa = entryMap.get().upper()

            if mapa in mapsInfo and spawn_int <= mapsInfo[mapa]:
                self.rodar_script(spawn_str, mapa)
                tk.Label(popup, text="Tirando prints", fg=FG, bg=BG_MAIN).pack(pady=5)
                popup.destroy()
            else:
                messagebox.showerror("Erro, spawn ou mapa invalido", f"Esse mapa só tem {mapsInfo[mapa]} spawns")

        entrySpawn.bind("<Return>", lambda e: confirmar())

        btn_ok = tk.Button(card, text="CONFIRMAR",
            font=("JetBrains Mono", 10, "bold"),
            bg=ACCENT, fg="#ffffff",
            activebackground=ACCENT_HV, activeforeground="#ffffff",
            relief="flat", bd=0, cursor="hand2",
            padx=18, pady=6,
            command=confirmar)
        btn_ok.pack(pady=(10, 0))
        hover(btn_ok, ACCENT_HV, ACCENT)

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
