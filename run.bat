pip install virtualenv
virtualenv env
cd env/Scripts
activate
cd ../..
copy formats.py env/Lib/site-packages/tube_dl/formats.py
copy __main__.py env/Lib/site-packages/tube_dl/__main__.py
pip install -r requirements
pip install numpy==1.19.0
python script.py
