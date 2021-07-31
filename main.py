from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

result = {}
response = requests.get("https://www.google.com/search?sxsrf=ALeKk0080IOuOpd2qDWpi9hmmU61T5CaFg:1627650354668&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiq_NSJ7oryAhXKV30KHaZ6DuwQ_AUoAXoECAEQAw&q=Virus%20Corona%20di%20Indonesia&biw=1920&bih=980")
bs = BeautifulSoup(response.text, "html.parser")
titles = bs.find_all("div", {'class':'BNeawe vvjwJb AP7Wnd'})
descriptions = bs.find_all('div', {'class':"BNeawe s3v9rd AP7Wnd"})
link_divs = bs.find_all("div", {'class':"kCrYT"})
counter = 1
links = []
for div in link_divs:
    links.append((div.find("a")['href'])[7:-91])
for title, desc, link in zip(titles, descriptions, links):
    result[counter] = {"title": title.text, "desc": desc.text, "link": link}
    counter += 1

@app.get("/")
def index():
    return {"message":"Check me on Github https://github.com/athallahmaajid", "api":"/api", "source":"Google"}

@app.get("/api")
def get_docs():
    return {"message":"get the api docs at /docs", "news":"/api/news"}

@app.get("/api/news")
def get_api():
    return result

@app.get('/api/news/{id}')
def get_json_by_id(id):
    return result[int(id)]
