from grader.models import Assessment

def slack_blocks(result: Assessment) -> dict:
    items=[{"type":"section","text":{"type":"mrkdwn","text":f"*Grader:* {result.score}/100 · *{result.signal}*"}}]
    if result.findings:
        items.append({"type":"section","text":{"type":"mrkdwn","text":"\n".join(f"• {x.severity}: {x.title} ({x.count})" for x in result.findings[:8])}})
    return {"blocks":items}
