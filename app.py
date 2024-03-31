from DMV import *

app = create_app()

if __name__ == '__main__': #app will run only if we run this file, it will not run when imported
    app.run(debug = True)