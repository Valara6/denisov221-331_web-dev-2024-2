from flask import Flask
import project.config as config
from project.db.db import MyDb
app = Flask(__name__)
app.config.from_object(config.MainConfig)
db = MyDb(app)
