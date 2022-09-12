import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.db import get_session
from app.adapters.repository import SQLModelSummaryRepository
from app import models

router = APIRouter()
log = logging.getLogger("summary routes")


@router.get("/{id_}", response_model=models.TextSummary, status_code=200)
def get_summary_by_id_route(id_: int, session=Depends(get_session)):
    repo = SQLModelSummaryRepository(session)
    summary = repo.get(id_)
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found.")
    return summary


@router.get("/", response_model=List[models.TextSummary], status_code=200)
def get_summaries_route(session=Depends(get_session)):
    repo = SQLModelSummaryRepository(session)
    result = repo.list()
    return result


@router.post("/", response_model=models.TextSummary, status_code=201)
def post_summary_route(summary: models.TextSummaryPayload, session=Depends(get_session)):
    repo = SQLModelSummaryRepository(session)
    try:
        result = repo.add(summary)
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=500, detail="An error occurred during saving data to database.")
    return result
