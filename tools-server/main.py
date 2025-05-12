from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Tools API",
    version="v1.0.0",
    description="Custom tools for Dify integration",
    servers=[{"url": ""}]
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    # Difyの期待に合わせてバージョンを明示的に指定
    openapi_schema["openapi"] = "3.1.0"
    openapi_schema["servers"] = [{"url": ""}]  # 空のserversがDify互換の鍵
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

class ReadFileRequest(BaseModel):
    path: str

class ReadFileResponse(BaseModel):
    content: str

@app.post("/tools/read_file", response_model=ReadFileResponse)
def read_file(req: ReadFileRequest):
    with open(req.path, "r", encoding="utf-8") as f:
        return {"content": f.read()}
