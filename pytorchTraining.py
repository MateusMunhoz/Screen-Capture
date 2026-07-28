from multiprocessing import process

import mss
import mss.tools
import os
import json
import sys
from pathlib import Path

downloads_path = Path.home() / "Downloads"
caminho_imagens = downloads_path / "caminho_imagens"


numSpawn = sys.argv[1] if len(sys.argv) > 1 else input("Qual spawn voce pegou? ")
mapName = sys.argv[2]


imgsaveMapSel = caminho_imagens / f"{mapName}" / f"spawn{numSpawn}"
os.makedirs(imgsaveMapSel, exist_ok=True)

json_path = Path("C:/Users/mateu/Downloads/AITraining")
with open(json_path / "spawnCounter.json", "w") as f:
    json.dump({"numSpawn": numSpawn, "mapName": mapName}, f)


with mss.MSS() as sct:
    contador = 0
    while contador < 150:
        contador += 1
        sct.shot(output=str(imgsaveMapSel / f"{contador}.png"))


