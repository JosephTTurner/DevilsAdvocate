from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/hello", methods=['GET', 'POST'])
@cross_origin(support_credentials=True)
def hello():
	
	print (request.data)

	return "Hello, CORS is awful."

if __name__ == "__main__":
    app.run()
