# PubMed Evidence Monitor

An automated pipeline that finds new medical research, evaluates its relevance and evidence level, produces concise Russian-language summaries, and delivers selected articles through a scheduled Telegram workflow.

The current monitor focuses on aesthetic medicine, including botulinum toxin, hyaluronic-acid fillers, laser and light treatments, focused ultrasound, and radiofrequency techniques.

## How it works

1. Queries the PubMed E-utilities API for recently published articles
2. Retrieves titles and abstracts for new PubMed IDs
3. Uses GPT-5 to create a structured summary in accessible Russian
4. Scores each article from 0 to 100 for topic relevance and strength of evidence
5. Removes duplicates, maintains a bounded priority queue, and sends the highest-ranked articles first
6. Runs automatically through scheduled GitHub Actions workflows

## Engineering details

- Tracks processed PubMed IDs to prevent duplicate delivery
- Retries transient PubMed requests
- Keeps API credentials in GitHub Actions secrets
- Separates search, summarization, queue, and delivery logic into small modules
- Records automated processing activity in the repository commit history

## Project structure

```text
pubmed_search.py       PubMed search and abstract retrieval
summarizer.py          Structured summarization and evidence scoring
fill_queue.py          Processing and prioritization pipeline
send_next_article.py   Telegram delivery
.github/workflows/     Scheduled automation
```

## Tech stack

Python · NCBI PubMed E-utilities · OpenAI API · Telegram Bot API · GitHub Actions

## Disclaimer

This project is a research-discovery and summarization tool, not a source of medical advice. AI-generated summaries should be checked against the original publication before clinical or academic use.
