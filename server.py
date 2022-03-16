import datetime
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
from typing import Dict, List

### Prepare `app`, CORS policy and database configs
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

### Prepare database
db = SQLAlchemy(app)


class Cookie(db.Model):
    """
    @param str key -> The key of the cookie 
    @param str value -> The value of the cookie 
    @param str time -> The time of the request that the cookie came from

    Class to capture a row in the Cookie table, 
    with the key and value of the cookie, 
    as well as, the time it was called. 
    """

    __tablename__ = 'cookies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(64))
    value = db.Column(db.String(255))
    timestamp = db.Column(db.String(255))

    def __repr__(self) -> str:
        return f"{self.key}: {self.value} - `{self.timestamp}`"

    def get_dict(self) -> Dict:
        return {
            "key": self.key,
            "value": self.value, 
            "timestamp": self.timestamp
        }


try: 
    db.create_all() # Initialise database
except: 
    print("Database already initialized. ")

### Helper functions for data storage and retrieval
def store_cookies(request, db: SQLAlchemy) -> None:
    """
    @param Request request -> The request object that Flask creates
    @param SQLAlchemy db -> The database ORM

    @return None

    Stores the key, value and time of request of 
    all the cookies from the current request. 
    """
    
    data = request.cookies
    timestamp = datetime.datetime.now().strftime("%a, %d %b %Y, %Z %H:%M:%S")

    for key in data:
        cookie = Cookie(
            key = key, 
            value = data[key], 
            timestamp = timestamp
        )

        db.session.add(cookie)
        db.session.commit()

def clear_cookies(request, db: SQLAlchemy) -> None:
    """
    @param Request request -> The request object that Flask creates
    @param SQLAlchemy db -> The database ORM

    @return None

    Deletes the key, value and time of request of 
    all the cookies stored so far. 
    """

    db.session.query(Cookie).delete()
    db.session.commit()

def process_results(results: Dict) -> Dict:
    """
    @param Dict results -> The dictionary containing data to be cleaned

    Processes the key and value of the dictionary passed in, 
    using the `escape()` function from markupsafe. 
    """
    
    cleaned_results = dict()

    for key in results:
        cleaned_results[escape(key)] = escape(results[key])
    
    return cleaned_results

def get_results(results: List) -> List[Dict]:
    """
    @param List results -> A list of SQLAlchemy query objects to be processed

    Processes a list of SQLAlchemy objects into dicts 
    and clean them with `process_results()`.  
    """
    
    cleaned_results = []

    for cookie in results: 
        cleaned_cookie = process_results(cookie.get_dict())
        cleaned_results.append(cleaned_cookie)
    
    return cleaned_results

@app.get("/")
def index():
    """
    Returns the landing page. 
    """

    store_cookies(request, db)
    
    return render_template("index.html")

@app.get("/cookies")
def get_cookies():
    """
    RESTful JSON API that returns the 
    details of all cookies received so far. 
    """
    
    store_cookies(request, db)
    
    results = Cookie.query.all()
    results = get_results(results)
    
    return jsonify(code = 200, data = results)

@app.delete("/cookies")
def delete_cookies():
    """
    RESTful JSON API that deletes the 
    records of all cookies received so far. 
    """
    
    clear_cookies(request, db)
    
    return jsonify(code = 200, data = "All cookies' details have been deleted. ")

@app.get("/cookies/<key>")
def get_cookies_by_key(key: str):
    """
    @param str key -> The key name to search for
    
    RESTful JSON API that returns the 
    details of cookies received so far 
    that have their key as `<key>`. 
    """
    
    store_cookies(request, db)
    
    results = Cookie.query.filter(Cookie.key.like(key + "%")).all()
    results = get_results(results)

    return jsonify(code = 200, data = results)

@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 page for not existent paths. 
    """
    
    store_cookies(request, db)
    
    return render_template("error.html"), 404

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True)