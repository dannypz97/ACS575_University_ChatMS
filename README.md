# ACS575_University_ChatMS
## University Chatbot Data Management System

### Setup instructions: -

1. Setup your python interpreter and virtual environment.

2. Install dependencies: 
``
pip install -r requirements.txt
``
3. In the `.streamlit` folder, create a `secrets.toml`. You many rename the existing `secrets.sample.toml` to `secrets.toml` to get started quickly.
4. Make sure to configure the settings in `secrets.toml`.
5. Run the db.sql file under the resources folder. **NOTE:** Initial queries attempt to DROP relevant tables. If you already have the tables setup, you will lose your data!