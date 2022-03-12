from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)

@app.get("/")
def index():
    data = request.cookies

    with open("store.txt") as file:
        for key in data:
            file.write(data[key] + "\n")
    
    with open("store.txt") as file:
        results = file.read()
    
    return "<head></head><body>" + escape(results) + "</body></html>"

if __name__ == "__main__":
    app.run()