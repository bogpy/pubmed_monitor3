import json

def load_processed_pmids():
    try:
        with open("processed_pmids.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
def save_processed_pmids(pmids):
    with open("processed_pmids.json", "w") as f:
        json.dump(pmids, f)