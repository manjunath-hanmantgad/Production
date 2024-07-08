# config_test.py

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'postgresql://sa_user:postgres@localhost:5432/sentiment_analysis_db_test'  # Use a separate test database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
