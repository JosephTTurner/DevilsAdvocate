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

#
