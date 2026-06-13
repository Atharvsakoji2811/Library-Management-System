from flask import Flask
from flask_restx import Api
import os
from dotenv import load_dotenv

from config import config
from database.db import db


load_dotenv()

app =Flask(__name__)

# Configuration
app.config.from_object(config)

# Database initialization
db.init_app(app)

app.secret_key = os.getenv("secret_key")

# Swagger API
api = Api(
    app,
    title="Library Management API",
    doc="/swagger"
)


# Run Server
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )