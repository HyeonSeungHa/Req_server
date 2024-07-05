from fastapi import FastAPI
from domain.req import req_server

app = FastAPI(docs_url="/docs", redoc_url=None)

app.mount('/', req_server.reqApp)

@app.get('/hello')
def hello():
    return 'hello'



