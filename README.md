# harmonize

### About
Harmonize is a web app that generates an accompaniment to any melody you play. It has a simple, user-friendly interface and displays its results as music notation as well as an audio file you can listen to. Behind the scenes, it is using machine learning to learn and predict the next chord based on the notes you provided!

### Installation

install postgresql
clone the repo
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install timidity
export SECRET_KEY='key'
dropdb project
createdb project
python model.py
python server.py
