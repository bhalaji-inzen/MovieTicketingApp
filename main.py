from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_caching import Cache

from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import *
from application.workers import *


app=None
celery=None
cache=None


def create_app():
  app=Flask(__name__,template_folder="templates")
  print("App has started to run")
  app.config.from_object(LocalDevelopmentConfig)
  db.init_app(app)
  app.app_context().push()
  with app.app_context():
    db.create_all()
  user_datastore=SQLAlchemySessionUserDatastore(db.session, User, Role)
  security= Security(app, user_datastore)

  celery = celery_app
  celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    broker_connection_retry_on_startup=True,
    timezone='Asia/Kolkata'
  )
  celery.Task=AppContextTask
  app.app_context().push()
  cache=Cache(app)
  app.app_context().push()
  return app, user_datastore, celery, cache

app, user_datastore, celery, cache =create_app()

from application.controllers import *

@app.before_request
def create_db():
    if not user_datastore.find_role("admin"):
      user_datastore.create_role(name="admin",description="Admin related work")
      db.session.commit()   
    if not user_datastore.find_user(email="admin@admin.com"):
      user_datastore.create_user(username="Admin",email="admin@admin.com",password="1234")
      admin_user=user_datastore.find_user()
      user_datastore.add_role_to_user(admin_user,'admin')
      db.session.commit()



if __name__ == '__main__' :
  app.run(debug=True, port=8080)