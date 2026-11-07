import json

path = r'C:\Users\arran\.gemini\antigravity\brain\57eae69b-12c6-48c3-adfb-23ad0560e82e\.system_generated\logs\transcript.jsonl'
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line)
        c = str(d.get('content', ''))
        if 'moneda' in c.lower() or 'coin' in c.lower() or 'select' in c.lower():
            clean = c[:250].encode('ascii', 'ignore').decode()
            print(f"[{d.get('step_index')}]: {clean}")
