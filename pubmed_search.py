import requests
import xml.etree.ElementTree as ET
import time

def get_latest_pmids():

    query = '''
(
    "arterial hypertension"[Title/Abstract]
    OR hypertension[Title/Abstract]
    OR perindopril[Title/Abstract]
    OR telmisartan[Title/Abstract]
)
'''

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 7,
        "sort": "pub_date",
        "retmode": "json",
        "datetype": "pdat",
        "reldate": 2
    }

    for attempt in range(3):

        try:
            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["esearchresult"]["idlist"]

        except Exception as e:

            print(f"PubMed error: {e}")

            time.sleep(10)

    return []

def get_abstract(pmid):
    print(f"Получаю PMID {pmid}")

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "xml"
    }

    for attempt in range(3):
        response = requests.get(url, params=params, timeout=30)

        if (
            response.status_code == 200
            and response.headers.get("Content-Type", "").startswith("text/xml")
            and response.text.lstrip().startswith("<?xml")
        ):
            root = ET.fromstring(response.text)

            title = root.find(".//ArticleTitle")
            title_res = title.text if title is not None else ""

            abstract_res = ""
            for section in root.findall(".//AbstractText"):
                if section.text:
                    abstract_res += section.text + "\n"

            return title_res, abstract_res

        print(f"Попытка {attempt + 1}/3 не удалась для PMID {pmid}")
        print("STATUS:", response.status_code)
        print(response.text[:300])

        time.sleep(3)

    raise RuntimeError(f"Не удалось получить PMID {pmid} после 3 попыток")