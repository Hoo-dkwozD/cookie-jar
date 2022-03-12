from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'

db = SQLAlchemy(app)

class Cookie(db.Model):
    __tablename__ = 'cookies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(64))
    value = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.key}: {self.value}"

@app.get("/")
def index():
    data = request.cookies

    for key in data:
        cookie = Cookie(key=key, value=data[key])

        db.session.add(cookie)
        db.session.commit()
    
    results = Cookie.query.all()
    
    return escape(results)

if __name__ == "__main__":
    db.create_all()
    app.run()