### Install dependencies
python3 install -r requirements.txt

### Run app
python3 app.py

### Auth Endpoints
check app.py

### App Endpoints
check routes.py

### After changes to packages used in project Update dependencies
pipreqs --savepath=requirements.in && pip-compile
