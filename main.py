from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

def get_json():
    result = {}
    response = requests.get("https://www.google.com/search?q=Virus+Corona+di+Indonesia&sxsrf=ALeKk02FVIsOvfpzFgjZbj72SxCVWPS73w:1627710455249&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiNrO37zYzyAhVFOSsKHfpSBOIQ_AUoAXoECAEQAw&biw=1920&bih=980")
    bs = BeautifulSoup(response.text, "html.parser")
    titles = bs.find_all("div", {'class':'BNeawe vvjwJb AP7Wnd'})
    descriptions = bs.find_all('div', {'class':"BNeawe s3v9rd AP7Wnd"})
    link_divs = bs.find_all("div", {'class':"kCrYT"})
    counter = 1
    links = []
    for div in link_divs:
        links.append((div.find("a")['href'])[7:-91])
    for title, desc, link in zip(titles, descriptions[::2], links[::2]):
        desc = desc.text.split("·")
        result[counter] = {"title": title.text, "desc": desc[1].strip(), "link": link, "time": desc[0].strip(), 'detail':f"/api/news/{counter}"}
        counter += 1
    return result

def get_json_by_id(data):
    response = requests.get(f"{data['link']}")
    bs = BeautifulSoup(response.text, "html.parser")
    images = bs.find_all("img")
    for image in images:
        if image.get('src') == None:
            continue
        elif ('.jpg' in image.get('src')) or ('.jpeg' in image.get('src')):
            data["image"] = image.get('src')
            break
    return data

@app.get("/")
def index():
    return {"message":"Check me on Github https://github.com/athallahmaajid", "api":"/api", 'docs': '/docs', "source":"Google"}

@app.get("/api")
def get_docs():
    return {"news":"/api/news"}

@app.get("/api/news")
def get_api():
    return get_json()

@app.get('/api/news/{id}')
def get_api_by_id(id):
    all_data = get_json()
    return get_json_by_id(all_data[int(id)])

if __name__ == "__main__":
    uvicorn.run(app)
