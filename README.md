# DMVTestReady

A web application that allows users to practice Driver's License knowledge test online.

## Programming & framework:

- Python 3.8
- Flask

## Database:

- sqlite3

## Access our web application online:

https://my-cloud-run-service-ya575o6hjq-uw.a.run.app/

## Run our web application locally

### Setup the virtual environment

#### Using conda (Preferable)

- conda create -n dmvtestready python=3.8
- conda activate dmvtestready

#### Using source

- source activate dmvtestready

### Install flask and other dependencies

```
  pip3 install flask
  pip3 install flask-login
  pip3 install flask-sqlalchemy
  pip3 install pandas
  pip3 install matplotlib
  pip3 install seaborn
```

### Run the application

- python3 app.py

## File Structure

```
.
├── DMV
│ ├── **init**.py
│ ├── **pycache**
│ │ ├── **init**.cpython-312.pyc
│ │ ├── **pycache**
│ │ │ ├── auth.cpython-312.pyc
│ │ │ └── views.cpython-312.pyc
│ │ ├── auth.cpython-312.pyc
│ │ ├── models.cpython-312.pyc
│ │ └── views.cpython-312.pyc
│ ├── controller
│ │ ├── **pycache**
│ │ │ ├── auth.cpython-312.pyc
│ │ │ └── views.cpython-312.pyc
│ │ ├── auth.py
│ │ └── views.py
│ ├── models.py
│ ├── static
│ │ ├── logo3.png
│ │ └── sampleAva.png
│ └── templates
│ ├── index.html
│ ├── login.html
│ ├── practice.html
│ ├── registration.html
│ └── templateMain.html
├── README.md
├── app.py
└── instance
└── databaseDMV.db
```
