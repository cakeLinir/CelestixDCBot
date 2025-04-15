# 🎯 CelestixDCBot – Valorant Rank Verifier

Ein moderner Discord-Bot zur **automatischen Verifikation von Valorant-Rängen** mithilfe offizieller Riot Games Schnittstellen. Entwickelt für kompetitive Discord-Server, Turniere und Gaming-Communities, die Fairness, Authentizität und sauberes Matchmaking gewährleisten möchten.

---

## 🛠 Features

- ✅ Auswahl-Interface für alle **Valorant Ranks** via Dropdown-Menü
- 🛡 Automatische **Rollenzuweisung** basierend auf gewähltem Rang
- 🔁 **Persistente Views**, auch nach Bot-Restarts
- 📦 Verwendung **benutzerdefinierter Emoji-Badges**
- 🔐 Slash-Command `/privacy` zur DSGVO-konformen Datenschutzerklärung
- 🧠 Riot API-Integration *(in Planung – pending approval)*

---

## 🔧 Voraussetzungen

- Python `3.10+`
- Abhängigkeiten (siehe `requirements.txt`):
  - `nextcord`
  - `python-dotenv`

---

## 🚀 Quickstart

```bash
git clone https://github.com/DEIN-NAME/CelestixDCBot.git
cd CelestixDCBot

# Optional: Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # oder .venv\Scripts\activate (Windows)

# Installieren
pip install -r requirements.txt
