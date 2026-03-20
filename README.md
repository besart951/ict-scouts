# Dino Runner

Ein sehr kleines Pygame-Projekt fuer den ersten Einstieg in objektorientiertes Programmieren mit Python.
Die Figur laeuft automatisch. Die Kinder muessen nur springen.
Wenn die Figur ein Hindernis beruehrt, ist die Runde vorbei.

Das Projekt ist bewusst einfach gehalten:

- wenige Dateien
- jede Klasse in ihrer eigenen Datei
- klare Aufgaben pro Klasse
- vorhandene Bilder und Sounds aus `assets/` werden direkt genutzt
- nur eine Hauptidee: springen und Hindernissen ausweichen

## Am einfachsten: mit uv starten

Wenn `uv` installiert ist, reicht das:

```powershell
uv run --python 3.12 main.py
```

`uv` laedt bei Bedarf Python 3.12, erstellt die Umgebung und installiert die Abhaengigkeiten automatisch.

Falls Python 3.12 noch nicht vorhanden ist, kann man es auch vorher explizit holen:

```powershell
uv python install 3.12
uv run --python 3.12 main.py
```

## Setup mit uv in 2 Schritten

Wenn ihr lieber zuerst alles vorbereitet und danach startet:

```powershell
uv sync --python 3.12
uv run main.py
```

## Warum Python 3.12?

Empfohlen ist **Python 3.12 oder 3.13**.
Mit Python 3.14 gibt es je nach System noch Probleme beim Installieren von `pygame`.

## Manueller Weg ohne uv

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3.12 -m pip install -r requirements.txt
py -3.12 main.py
```

macOS oder Linux:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python3.12 -m pip install -r requirements.txt
python3.12 main.py
```

## Steuerung

- `Leertaste`, `W` oder `Pfeil hoch`: springen
- `R`: Runde neu starten
- `Esc`: Spiel beenden

## Dateiueberblick

- `main.py`: Startpunkt
- `game.py`: Hauptschleife, Punkte, neue Hindernisse und Game Over
- `player.py`: die Figur springt und zeigt die passende Animation
- `obstacle.py`: ein Hindernis bewegt sich nach links
- `asset_store.py`: laedt Bilder und Sounds aus `assets/`
- `settings.py`: wenige Zahlen fuer das Spiel
- `pyproject.toml`: Projektdatei fuer `uv`
- `uv.lock`: gesperrte Paketversionen fuer `uv`
- `klassendiagramm.puml`: PlantUML-Klassendiagramm

## Warum die Struktur gut fuer Kinder ist

- Man sieht schnell, **welche Klasse wofuer zustaendig ist**.
- Das Spiel zeigt die typische Pygame-Struktur: `Eingaben -> Update -> Zeichnen`.
- Es gibt nur wenige zentrale Ideen: `Game`, `Player`, `Obstacle`, `AssetStore`.
- Die Figur laeuft alleine. Die Kinder konzentrieren sich nur auf das Springen.
- Es gibt keine Levelkarte, keine Gegnerlogik und keine freie Bewegung nach links und rechts.

## Spielidee

- Die Figur laeuft automatisch.
- Von rechts kommen Kakteen und Steine.
- Fuer jedes ueberstandene Hindernis gibt es einen Punkt.
- Bei einer Kollision erscheint `Game Over`.

## PlantUML

Die Datei `klassendiagramm.puml` kann mit PlantUML gerendert werden.

Beispiel:

```bash
plantuml klassendiagramm.puml
```

Dann entsteht daraus zum Beispiel eine PNG-Datei mit dem Klassendiagramm.
