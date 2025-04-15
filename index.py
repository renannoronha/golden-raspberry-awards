from os import environ

environ["ENV"] = "local"

from src.api import app

if __name__ == "__main__":
    app.run(debug=True)
