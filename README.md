# DMVTestReady

A web application that allows users to practice Driver's License knowledge test online.

### Virtual Environment: Conda

### Dependencies:

- Python 3.8
- Flask
- sqlite3

### Setup the virtual environment for project

- conda create -n dmvtestready python=3.8
- conda activate dmvtestready

### Install flask and other dependencies

- dependencies:
	pip3 install flask
	pip3 install flask-login
	pip3 install flask-sqlachemy

### Run the application

- python3 app.py
### File Structure
.
├── DMV
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── __pycache__
│   │   │   ├── auth.cpython-312.pyc
│   │   │   └── views.cpython-312.pyc
│   │   ├── auth.cpython-312.pyc
│   │   ├── models.cpython-312.pyc
│   │   └── views.cpython-312.pyc
│   ├── controller
│   │   ├── __pycache__
│   │   │   ├── auth.cpython-312.pyc
│   │   │   └── views.cpython-312.pyc
│   │   ├── auth.py
│   │   └── views.py
│   ├── models.py
│   ├── static
│   │   ├── logo3.png
│   │   └── sampleAva.png
│   └── templates
│       ├── index.html
│       ├── login.html
│       ├── practice.html
│       ├── registration.html
│       └── templateMain.html
├── README.md
├── app.py
└── instance
    └── databaseDMV.db
