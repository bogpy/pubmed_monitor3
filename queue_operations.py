import json

def load_queue():
    try:
        with open("article_queue.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_queue(queue):
    with open("article_queue.json", "w") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)