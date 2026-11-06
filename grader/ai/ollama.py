from __future__ import annotations
import json
from urllib import request,error,parse
from grader.errors import OllamaError

class OllamaClient:
    def __init__(self,base_url="http://127.0.0.1:11434",timeout=8.0):
        parsed=parse.urlsplit(base_url)
        if parsed.hostname not in {"localhost","127.0.0.1","::1"}:
            raise OllamaError("For privacy, Ollama must run on localhost")
        if parsed.scheme != "http": raise OllamaError("Ollama must use local http")
        self.url=base_url.rstrip("/")+"/api/generate"
        self.timeout=timeout

    def generate(self,prompt:str,model="llama3") -> str:
        payload=json.dumps({"model":model,"prompt":prompt,"stream":False}).encode()
        req=request.Request(self.url,payload,headers={"Content-Type":"application/json"},method="POST")
        try:
            with request.urlopen(req,timeout=self.timeout) as response:
                result=json.load(response)
            return str(result.get("response","")).strip()
        except (error.URLError,TimeoutError,ValueError,OSError) as exc:
            raise OllamaError(f"Local Ollama unavailable: {exc}") from exc
