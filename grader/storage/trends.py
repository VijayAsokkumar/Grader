from grader.storage.sqlite import connect

def recent_runs(db_path:str,limit=20)->list[dict]:
    with connect(db_path) as db:
        rows=db.execute("SELECT id,source,format,score,signal,created_at FROM runs ORDER BY id DESC LIMIT ?",(max(1,int(limit)),)).fetchall()
    return [dict(zip(("id","source","format","score","signal","created_at"),r)) for r in rows]
