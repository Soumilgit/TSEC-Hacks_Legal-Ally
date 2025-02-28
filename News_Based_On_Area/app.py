from flask import Flask, render_template, request, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_news(region):
    search_query = region.replace(" ", "+") + "+law+and+legal+news"
    url = f"https://news.google.com/rss/search?q={search_query}"

    response = requests.get(url)

    if response.status_code != 200:
        return ["Failed to retrieve news"]

    soup = BeautifulSoup(response.content, 'xml')
    items = soup.find_all('item')[:5]

    news_list = []
    for item in items:
        title = item.title.text
        link = item.link.text
        news_list.append({"title": title, "link": link})

    return news_list

@app.route("/", methods=["GET", "POST"])
def home():
    news = []
    if request.method == "POST":
        region = request.form["region"]
        news = fetch_news(region)

    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(host="127.0.0.2", port=5000, debug=True)
