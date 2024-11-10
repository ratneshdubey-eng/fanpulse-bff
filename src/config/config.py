import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:test%40123@localhost:5432/fanpulse')
    SQLALCHEMY_TRACK_MODIFICATIONS = False