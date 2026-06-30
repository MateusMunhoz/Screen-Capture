import mss
import mss.tools
import os
import json
from pathlib import Path
import time

downloads_path = Path.home() / "Downloads"
caminho_imagens = downloads_path / "caminho_imagens"
json_path = Path("C:/Users/mateu/Downloads/AITraining")
try:
    with open(json_path / "spawnCounter.json", "r") as f:
        numSpawn = json.load(f)["numSpawn"]
except FileNotFoundError:
    numSpawn = 1

total_spawns = 31
os.makedirs(caminho_imagens, exist_ok=True)



with mss.MSS() as sct:
    contador = 0
    while contador < 15:
        contador += 1
        sct.shot(output=str(caminho_imagens / f"print_spawn{numSpawn}_N{contador}.png"))
        time.sleep(1)
    spawn_atual = input("Qual spawn você pegou? ")
    with open(json_path / "spawnCounter.json", "w") as f:
        json.dump({"numSpawn": spawn_atual}, f)

