from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from src.resource.awards import awards_ns

from src.utils.set_database import SetDatabase

# Declare APP
app = Flask(__name__)

api = Api(
    app,
    doc="/doc/",
    version="1.0",
    title="Golden Raspberry Awards",
    description="Documentação para consulta da API do Golden Raspberry Awards",
)

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/*": {"origins": "*"}})

# Namespaces
api.add_namespace(awards_ns)

# Build database
SetDatabase().set_database()
