from typing import Optional, List

from app.adapters.repository import AbstractSummaryRepository, TextSummary


def get_summary(id_: int, repository: AbstractSummaryRepository) -> Optional[TextSummary]:
    item = repository.get(id_)
    return item


def add_summary(item: TextSummary, repository: AbstractSummaryRepository) -> TextSummary:
    added_item = repository.add(item)
    return added_item


def get_all_summaries(repository: AbstractSummaryRepository) -> List[Optional[TextSummary]]:
    items = repository.list()
    return items


def delete_summary(id_: int, repository: AbstractSummaryRepository) -> None:
    repository.delete(id_)
