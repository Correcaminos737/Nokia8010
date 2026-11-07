import json

with open(r'C:\Users\arran\.gemini\antigravity\brain\b91774bc-257d-43cd-badc-a6ce6977deb2\.system_generated\logs\transcript.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        content = str(data.get('content', ''))
        if 'moneda' in content.lower() or 'coin' in content.lower():
            clean_text = content[:200].encode('ascii', 'ignore').decode()
            print(f"Step {data.get('step_index')}: {clean_text}")
