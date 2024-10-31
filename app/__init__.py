'''initialise the app and db, and register routers'''

from flask import Flask
from app import models_orm, db, helper, routers
import config

models_orm.Base.metadata.create_all(bind=db.engine)

app = Flask(__name__, 
    template_folder="../templates", 
    static_url_path="/static", static_folder="../static")

app.secret_key = config.settings.secret_key

app.register_blueprint(routers.public.public_page, url_prefix="/")
app.register_blueprint(routers.staff.staff_page, url_prefix="/staff")
app.register_blueprint(routers.customer.customer_page, url_prefix="/customer")

# initialise db with data
with db.get_db() as db_session:
    helper.initialise_db(db_session)