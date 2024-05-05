from celery import Celery 
from flask import current_app as app 

celery_app= Celery("Backend Jobs")

class AppContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)