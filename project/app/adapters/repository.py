from typing import Optional, List, Union
import abc
from sqlmodel import select

from app.models import TextSummary, TextSummaryPayload


class AbstractSummaryRepository(abc.ABC):

    @abc.abstractmethod
    def get(self, id_: int) -> Optional[TextSummary]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[Optional[TextSummary]]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item: TextSummary) -> TextSummary:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, id_):
        raise NotImplementedError


class SQLModelSummaryRepository(AbstractSummaryRepository):

    def __init__(self, session):
        self.session = session

    def get(self, id_: int) -> Optional[TextSummary]:
        result = self.session.exec(select(TextSummary).where(TextSummary.id == id_)).first()
        return result

    def list(self) -> List[Optional[TextSummary]]:
        result = self.session.exec(select(TextSummary)).all()
        return result

    def add(self, item: Union[TextSummary, TextSummaryPayload]) -> TextSummary:
        if isinstance(item, TextSummaryPayload):
            item = TextSummary(**item.dict())
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete(self, id_: int) -> None:
        item = self.session.exec(select(TextSummary).where(TextSummary.id == id_)).one()
        self.session.delete(item)
