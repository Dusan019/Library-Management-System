import os

class Config:
    # Secret key for session management and JWT
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

    # Database connection URI
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://root:root@localhost:3306/library_system'
    )

    # Disable SQLAlchemy track modifications to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False
