<<<<<<< HEAD
from flasksite import db


db.create_all()
=======
from flasksite import create_app

app = create_app()
app.app_context().push()

from flasksite import db

db.create_all()
>>>>>>> 5df6187... First commit
