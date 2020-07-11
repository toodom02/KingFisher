<<<<<<< HEAD
from flasksite import app

if __name__ == '__main__':
    app.run(debug=False)
=======
from flasksite import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 5df6187... First commit
