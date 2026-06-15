import os
from dotenv import load_dotenv

load_dotenv()


class config:
    # Adding string defaults prevents the variables from turning into "None"
    host = os.getenv("db_host", "localhost")
    user = os.getenv("db_user", "root")
    password = os.getenv("db_password", "")
    name = os.getenv("db_name", "library")
    port = os.getenv("db_port", "3306")  # Safe fallback port string

    # Explicitly use standard mysql+pymysql driver
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
