from Database.database import db
import os
from dotenv import load_dotenv
load_dotenv()

class config:
    host=os.getenv("db_host")
    user=os.getenv("db_user")
    password=os.getenv("db_password")
    name=os.getenv("db_name")
    port=os.getenv("db_port")

    SQLALCHEMY_DATABASE_URI =(
        f"mysql://{user}:{password}@{host}:{port}/{name}"
    )

SQLALCHEMY_TRACK_MODIFICATIONS = False