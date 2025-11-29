# vulnerable_app.py
from flask import Flask
import pickle
import subprocess

app = Flask(__name__)

# ”я«¬»ћќ—“№: Debug mode в production
app.config['DEBUG'] = True

# ”я«¬»ћќ—“№: —лабый секретный ключ
app.config['SECRET_KEY'] = 'simple'

# ”я«¬»ћќ—“№: ѕотенциально опасна€ десериализаци€
def load_data(data):
    return pickle.loads(data)  # ќпасно!

# ”я«¬»ћќ—“№: ѕотенциальна€ командна инъекци€  
def run_command(cmd):
    return subprocess.call(cmd, shell=True)  # ќпасно!

if __name__ == '__main__':
    app.run(debug=True)  # ≈ще один debug=True!
