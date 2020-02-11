import os
import re

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText().strip()


def pig_latinize(fact):
    with requests.Session() as session:
        response = session.post("https://hidden-journey-62459.herokuapp.com/piglatinize/",
                                data={"input_text": fact})

    return response


@app.route('/')
def home():
    fact = get_fact()
    pig_latinized = pig_latinize(fact)

    css_sub = ('<head>\n<style type ="text/css" >\n  .footer{\n      '
               'position:fixed;\n      bottom:10px;\n  }\n</style>')
    body_sub = ('<p>URL: <a href={url}>{url}</a>\n\n<p><div class="footer">'
                'riginalOay actfay: {fact}</div></body>'.format(url=pig_latinized.url, fact=fact))
    
    body = re.sub('<head>', css_sub, pig_latinized.text)
    body = re.sub('</body>', body_sub, body)

    return Response(response=body.encode('utf8'), mimetype="text/html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)






