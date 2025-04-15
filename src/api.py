from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from os import environ

# from src.resource.branch import branch_ns

# Build database

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
# api.add_namespace(branch_ns)
