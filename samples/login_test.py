from sqlalchemy import create_engine, text
from pip._vendor import tomli

import bcrypt

# user-provided password that is to be verified during login time...
user_password = 'root'

with open("../.streamlit/secrets.toml", "rb") as f:
    data = tomli.load(f)
    base_obj = data['connections']['mysql']

    host = base_obj['host']
    port = base_obj['port']
    db = base_obj['database']
    username = base_obj['username']
    password = base_obj['password']

connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{db}"
engine = create_engine(connection_string, echo=False)

with engine.connect() as connection:
    result = connection.execute(text("SELECT password from users WHERE email='parvd01@pfw.edu'")).one()

    stored_hash = result[0]
    stored_hash = bytes(stored_hash)

    # Checking Password
    check = bcrypt.checkpw(
        password=bytes(user_password, encoding='utf-8'),
        hashed_password=stored_hash
    )

    print(check)
