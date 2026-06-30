import tkinter as tk
import subprocess
import os
import sys

class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Print Timer")
        self.root.geometry("220x90+1400+20")
        self.root.wm_attributes('-topmost', True)
        self.root.configure(bg='#2b2b2b')

        self.label = tk.Label(
            self.root, text="Proximo: 5:00",
            font=("Consolas", 14), fg="#ffffff", bg='#2b2b2b'
        )
        self.label.pack(pady=6)

        self.btn = tk.Button(
            self.root, text="ATIVAR SCRIPT",
            font=("Consolas", 11, "bold"),
            bg="#3a3a3a", fg="#ffffff",
            activebackground="#555555", activeforeground="#ffffff",
            relief=tk.FLAT, bd=0,
            command=self.ativar_script
        )
        self.btn.pack(pady=2)

        self.seconds = 300
        self.alerta_ativo = False
        self.contagem()
        self.root.mainloop()

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

    def ativar_script(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(
            [sys.executable, os.path.join(script_dir, "pytorchTraining.py")],
            cwd=script_dir
        )
        self.seconds = 300
        self.alerta_ativo = False
        self.label.config(text="Proximo: 5:00", fg="#ffffff")
        self.root.configure(bg='#2b2b2b')
        self.label.configure(bg='#2b2b2b')
        self.btn.configure(bg='#3a3a3a', text="ATIVAR SCRIPT")


if __name__ == "__main__":
    Overlay()
