# Screen Capture - Ferramenta de reconhecimento de imagens

Ferramenta simples em Python para capturar telas automaticamente e organizar prints por spawn e mapa. Feito para coletar imagens a serem usadas para treinamento de uma IA que identifique aonde o player spawnou.

## Funcionalidades

- Seleção de mapa e spawn via popup.
- Exibição de legendas de spawns por mapa.
- Captura automática de **150 screenshots** ao confirmar.
- Organiza as imagens em pastas por mapa e número do spawn.
- Salva os metadados (`spawn` e `mapa`) em um arquivo JSON.

## Mapas suportados

| Mapa      | Spawns | Legenda                            |
|-----------|--------|------------------------------------|
| CUSTOMS   | 24     | `EsquerdaSpawns.png`, `DireitaSpawns.png` |
| SHORELINE | 26     | `spawns shoreline.png`             |


## Estrutura do projeto

```
Screen-Capture-master/
├── overlay.py           # Interface principal e controle do fluxo
├── pytorchTraining.py   # Script de captura de tela
├── spawnCounter.json    # Último spawn e mapa selecionados
├── EsquerdaSpawns.png   # Legenda de spawns (Customs)
├── DireitaSpawns.png    # Legenda de spawns (Customs)
├── spawns shoreline.png # Legenda de spawns (Shoreline)
├── spawns woods.png     # Legenda de spawns (Woods)
└── .idea/               # Configurações do PyCharm
```

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `pynput`
  - `Pillow`
  - `mss`

Instale as dependências com:

```bash
pip install pynput Pillow mss
```

## Como usar

1. Execute a interface principal:

```bash
python overlay.py
```

2. Pressione `F8` ou clique em **ATIVAR SCRIPT**.
3. Digite o nome do mapa (`CUSTOMS`, `SHORELINE` ou `WOODS`).
4. Digite o número do spawn que você pegou.
5. Clique em **Ver legenda de spawns** para conferir a posição (opcional).
6. Clique em **CONFIRMAR**.

As capturas serão salvas em:

```
Downloads/caminho_imagens/<MAP>/spawn<NUM>/
```



## Avisos

- O caminho de saída das imagens está configurado para a pasta `Downloads/caminho_imagens` do usuário atual.
- O `spawnCounter.json` é salvo em `C:/Users/mateu/Downloads/AITraining/`. Ajuste esse caminho no código se necessário.
- Certifique-se de que as bibliotecas estejam instaladas antes de rodar o projeto.
