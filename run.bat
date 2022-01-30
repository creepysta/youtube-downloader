pip install virtualenv
virtualenv venv
call venv\Scripts\activate
pip install -r requirements
pip install numpy==1.19.0
copy formats.py "venv/Lib/site-packages/tube_dl/formats.py" /y
copy __main__.py "venv/Lib/site-packages/tube_dl/__main__.py" /y
python script.py
explorer audios
