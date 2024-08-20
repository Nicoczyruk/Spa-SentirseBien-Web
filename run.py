from app import create_app
import os
from sqlalchemy import inspect

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)