from fastapi import FastAPI,UploadFile,File,HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from tempfile import TemporaryDirectory
from grader.pipeline import analyze
from grader.errors import GraderError

app=FastAPI(title="Grader",version="0.1.0")

@app.get("/health")
def health(): return {"status":"ok","service":"grader"}

@app.post("/api/v1/analyze")
async def analyze_upload(file: UploadFile=File(...),format: str|None=None,ai:bool=False,threshold:float=80):
    filename=Path(file.filename or "report.json").name
    with TemporaryDirectory(prefix="grader-") as tmp:
        target=Path(tmp)/filename
        # Strict size limit for the single-file HTTP endpoint (directory formats use CLI).
        size=0
        with target.open("wb") as output:
            while data:=await file.read(1024*1024):
                size+=len(data)
                if size>20*1024*1024: raise HTTPException(413,"Max upload size is 20MB")
                output.write(data)
        try: return analyze(str(target),format=format,threshold=threshold,ai=ai).to_dict()
        except (GraderError,ValueError) as exc: raise HTTPException(422,str(exc)) from exc

@app.post("/api/v1/ingest/atomic")
def atomic_placeholder():
    return JSONResponse(status_code=501,content={"detail":"Advanced idempotent ingestion not yet implemented; see challenge/AGENT_TASK.md"})
