# hackbright-project

## Generating accompaniment to a given melody


#### Setting it up:

* set up virtual environment
* ``` pip install -r requirements.txt ```
* ``` sudo apt install timidity ```
* add a variable SECRET_KEY to environment
* ``` createdb project ```
* ``` python model.py ```
* ``` python server.py ```
* go to localhost:5000

#### Input:

* note names with octaves - C5, F4 B-4
* space-separated
* - is for flats
