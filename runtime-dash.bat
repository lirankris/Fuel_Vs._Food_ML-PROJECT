@ECHO ON
cd..
Script\activate
cd main
pip install  -r requirements.txt  --no-index 
pytthon dash_web_app.py