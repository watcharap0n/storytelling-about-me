"""Simple chat/FAQ service."""

from __future__ import annotations

from typing import List

from app.services.data_service import (
    get_about,
    get_faq_entries,
    get_pillars,
    get_work_items,
    get_skills,
)


def _collect_corpus() -> List[tuple[str, str]]:
    corpus: List[tuple[str, str]] = []
    about = get_about()
    corpus.append(("about", f"Headline: {about['headline']}\nSummary: {about['summary']}"))
    for pillar in get_pillars():
        corpus.append((pillar["id"], f"Pillar {pillar['title']}: {'; '.join(pillar['bullets'])}"))
    for work in get_work_items():
        corpus.append((work["slug"], f"{work['title']} - {work['summary']}"))
    for skill in get_skills():
        corpus.append((skill["id"], f"{skill['title']}: {', '.join(item['name'] for item in skill['items'])}"))
    for faq in get_faq_entries():
        corpus.append((faq["id"], faq["answer"]))
    return corpus


CORPUS = _collect_corpus()


def answer_question(question: str, audience: str) -> tuple[str, List[str], List[str]]:
    question_lower = question.lower()
    matches = [entry for entry in CORPUS if any(word in entry[1].lower() for word in question_lower.split())]
    if not matches:
        matches = CORPUS[:3]
    answer_parts = [entry[1] for entry in matches[:3]]
    answer = "\n\n".join(answer_parts)
    suggestions = ["See availability", "View case studies", "Contact Kane"]
    sources = [entry[0] for entry in matches[:3]]
    events = [
        {
            "type": "chat",
            "audience": audience,
            "intent": "portfolio_query",
            "sources": sources,
        }
    ]
    return answer, sources, suggestions, events
