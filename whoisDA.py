from flask import Flask, request, url_for, redirect
from flask_cors import CORS, cross_origin
import whois
import json

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/getWhoIs", methods=['GET'])
@cross_origin(support_credentials=True)
def get_who_is():
	url = request.args.get('checkURL')
	whoisReturn = whois.whois(url)
	print (whoisReturn)
	return whoisReturn.text


if __name__ == "__main__":
	app.run()