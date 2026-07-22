import requests, os
from summarizer import summarize_article, evaluate_article
from pubmed_search import get_abstract, get_latest_pmids
from json_operations import load_processed_pmids, save_processed_pmids
from queue_operations import load_queue, save_queue

BOT_TOKEN = os.environ["BOT_TOKEN"]

processed_pmids = load_processed_pmids()
queue = load_queue()
pmids = get_latest_pmids()

if not pmids:
    print("PubMed вернул пустой список")
    exit()

for pmid in pmids:
    if pmid in processed_pmids:
        continue
    
    
    try:
        title, abstract = get_abstract(pmid)
    except Exception as e:
        print(f"Пропускаю PMID {pmid}: {e}")
        continue

    if abstract == "":
        continue

    try:
        summary = summarize_article(title, abstract)
        score = evaluate_article(title, abstract)
    except Exception as e:
        print(f"Ошибка GPT: {e}")
        continue

    pubmed_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

    article = {
        "pmid": pmid,
        "title": title,
        "summary": summary,
        "score": score,
        "link": pubmed_link
    }

    queue.append(article)
    if len(queue) > 24:
        queue = queue[-24:]

    processed_pmids.append(pmid)

queue.sort(key=lambda article: article["score"], reverse=True)

save_queue(queue)
save_processed_pmids(processed_pmids)

print(f"В очереди сейчас: {len(queue)} статей")
print(f"Сейчас обработанных публикаций: {len(processed_pmids)}")