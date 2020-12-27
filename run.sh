pip install virtualenv
virtualenv env
./env/Scripts/activate
pip install -r requirements
pip install numpy==1.19.0
cp formats.py "env/Lib/site-packages/tube_dl/formats.py"
cp __main__.py "env/Lib/site-packages/tube_dl/__main__.py"
python script.py

