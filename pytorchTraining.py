import mss
import mss.tools
import os
import json
import sys
from pathlib import Path
import time

downloads_path = Path.home() / "Downloads"
caminho_imagens = downloads_path / "caminho_imagens"

numSpawn = sys.argv[1] if len(sys.argv) > 1 else input("Qual spawn voce pegou? ")

imgSave = caminho_imagens / f"spawn{numSpawn}"
os.makedirs(imgSave, exist_ok=True)

json_path = Path("C:/Users/mateu/Downloads/AITraining")
with open(json_path / "spawnCounter.json", "w") as f:
    json.dump({"numSpawn": numSpawn}, f)

with mss.MSS() as sct:
    contador = 0
    while contador < 15:
        contador += 1
        sct.shot(output=str(imgSave / f"{contador}.png"))
        time.sleep(1)

