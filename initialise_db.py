from flasksite import create_app

app = create_app()
app.app_context().push()

from flasksite import db

db.create_all()
