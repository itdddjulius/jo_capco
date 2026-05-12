from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from rag import RAGBot

app = FastAPI()

# Mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")

# RAG Bot
bot = RAGBot()
bot.read_and_embed_data("data/")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/ask", response_class=HTMLResponse)
async def ask(request: Request, question: str = Form(...)):

    answer = bot.ask(question)

    return templates.TemplateResponse(
        request=request,
        name="answer.html",
        context={
            "question": question,
            "answer": answer
        }
    )