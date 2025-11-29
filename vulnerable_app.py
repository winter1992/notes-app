# vulnerable_app.py
from flask import Flask
import pickle
import subprocess

app = Flask(__name__)

# ����������: Debug mode � production
app.config['DEBUG'] = False

# ����������: ������ ��������� ����
app.config['SECRET_KEY'] = 'simple'

# ����������: ������������ ������� ��������������
def load_data(data):
    return pickle.loads(data)  # ������!

# ����������: ������������� �������� ��������  
def run_command(cmd):
    return subprocess.call(cmd, shell=True)  # ������!

if __name__ == '__main__':
    app.run(debug=False)  # ��� ���� debug=False!
