# DevilsAdvocate
Fact Checking Chrome Extension: implements social media API's (Twitter) and HTML parsing

HTML5 and my-chrome-extension starter is borrowed code from existing github projects

They can be used as starter code / examples / tools for our project 

https://github.com/aredridel/html5

https://github.com/salsita/chrome-extension-skeleton

# server.py
This is the flask based python server which serves the endpoints for the LinkAnalyzer and Whois endpoints.
This is run with the command "python server.py" which will open the server on your localhost:8080. At that point any requests to either http://localhost:8080/analyze_links, or http://localhost:8080/get_who_is will attempt to query the server.

server.py requires flask, BeautifulSoup, whois, and flask_cors to be installed.

Analyze Links will need a json list of the hrefs in the parent page, this can be obtained automatically if you run the Chrome extension.

get_who_is requires a query parameter that is the url of the page you want whois information on. This is formatted as http://localhost:8080/get_who_is?checkURL=[your website here]


# Classifier.py
Classifier runs and then tests the accuracy of a classifier created using ScikitLearn and NLTK. It is currently using the Bernoulli Naive Bayesian Network, and is 60.48% accurate on our data.
Classifier is run with the command "python classifier.py"
It requires NLTK and ScikitLearn to be installed.
It also requires the Fake_News.csv and Real_News.csv to be present in the same directory as classifier.py.

# Chrome Extension Installation
The chrome extension requires that the manifest.json, link_analyzer.js, and jquery-3.2.1.min.js files are present in the folder you use to install as the extension.
The manifest file should automatically pull the appropriate js files into the extension.

# Demo
The Classifier can be tested by running the command "python classifier.py" on a python capable command prompt.
The Chrome Extension once installed will attempt to query the python server.py with API calls. For this to work the command "python server.py" must be run in a python capable command prompt. After this you should see a message saying that the server is running on localhost:8080. From there the Chrome extension should work when installed.
The Whois endpoint must currently be tested by actually calling it yourself. Its format is http://localhost:8080/get_who_is?checkURL=redcountry.us This for example pulls the whois information for redcountry.us, a conservative fake news site.
