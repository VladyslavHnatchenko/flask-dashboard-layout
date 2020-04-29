# Flask Dashboard layout
_______________________________________________________________________
###### How to install repository 
Clone repo: 
```bash
git clone https://github.com/VladyslavHnatchenko/flask-dashboard-layout.git
```
Go to folder: 
```bash
cd flask-dashboard-layout
```
_______________________________________________________________________
###### How run in docker container:
To run on terminal/bash: 
```bash
docker-compose up 
OR 
sudo docker-compose up 
```
To build container: 
```bash
docker-compose up --build 
OR
sudo docker-compose up --build
```
Open [localhost](http://localhost:5000/) in your browser.
_______________________________________________________________________
###### How run to locally:
Go to folder: 
```bash
cd flask-dashboard-layout/app
```
To run on terminal/bash:
```bash
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
```
Install and activate virtualenv:
```bash 
python3 -m venv env
source env/bin/activate
```
Install all libraries: 
```bash 
pip install -r requirements.txt
```
Change app.config in /app/main.py and comment/uncomment according to example in /app/main.py
```bash 
app.config['MYSQL_DATABASE_PASSWORD'] = 'Insert your data'
app.config['MYSQL_DATABASE_HOST'] = 'Insert your data'
```
Run locally:
```bash 
python3 main.py
```
Open [localhost](http://localhost:5000/) in your browser.
_______________________________________________________________________
