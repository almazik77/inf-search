import os
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import warnings
from vector_search import Vector

templates = Jinja2Templates(directory=os.path.dirname(__file__) + "/templates")

app = FastAPI()
vector = Vector()
warnings.filterwarnings("ignore")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", context={'request': request})


@app.post("/")
async def search(request: Request, query=Form(...)):
    result = vector.search((str(query)))
    return templates.TemplateResponse("index.html", context={'request': request, 'result': result, 'query': query})


if __name__ == '__main__':
    uvicorn.run(app)
