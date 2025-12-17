from flask import Flask
from app import create_app, db

app = create_app('DevelopmentConfig')

with app.app_context():
    db.create_all()  # Create all tables
   
if __name__== '__main__':
    app.run(debug=True)