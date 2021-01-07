import flask
from flask import jsonify, request
from searchDB import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Watch This</h1><p>This is a prototype api for watch this movie app to gt movies details form multiple sources</p>"


@app.route('/api/movies', methods=['GET'])
def api_all():
    query = str(request.args['q'])
    return jsonify(searchTmdb(query))


@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    # if 'id' in request.args:
    #     id = int(request.args['id'])
    # else:
    #     return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    # for book in books:
    #     if book['id'] == id:
    #         results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)


# print(searchTmdb("name"))
app.run(host="0.0.0.0")
