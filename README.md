# 🏦 Mini Bank App

Një aplikacion bankar i thjeshtuar i ndërtuar me Python dhe Streamlit, që simulon funksionalitetet bazë të një banke: regjistrim, login, depozita, tërheqje dhe transferta mes përdoruesve.

## ✨ Funksionalitete

- 🔐 Regjistrim dhe login i sigurt (password hashing me bcrypt)
- 💰 Depozitim dhe tërheqje fondesh
- 🔁 Transfertë parash mes përdoruesve
- 📊 Historia e transaksioneve
- 📈 Grafik interaktiv i ndryshimit të bilancit nëpër kohë
- 🎨 Ndërfaqe moderne me temë të errët

## 🛠️ Teknologjitë e përdorura

- **Python 3.13**
- **Streamlit** – ndërfaqja web
- **SQLite** – baza e të dhënave
- **bcrypt** – enkriptimi i password-ave
- **Pandas** & **Plotly** – analizë dhe vizualizim i të dhënave

## 🚀 Si të nisësh projektin lokalisht

1. Klono repository-n:
```bash
git clone https://github.com/Emiljano01/mini-bank-app.git
cd mini-bank-app
```

2. Krijo virtual environment dhe aktivizoje:
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

3. Instalo librarite:
```bash
pip install -r requirements.txt
```

4. Nise aplikacionin:
```bash
streamlit run app.py
```

## 📸 Screenshots

*(Shto këtu 1-2 foto ekrani të app-it kur ta ngarkosh)*

## 📁 Struktura e projektit