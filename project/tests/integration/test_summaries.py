from app import models
import pytest


def add_summary(session, url: str = "www.blabla.org"):
    summary = models.TextSummary(url=url)
    session.add(summary)
    session.commit()


def test_get_summary_returns_existing_summary(client, session):
    add_summary(session)
    response = client.get("/summaries/1")
    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["summary"] is None
    assert body["url"] == "www.blabla.org"


def test_get_summary_returns_404_for_invalid_summary_id(client):
    response = client.get("/summaries/109281")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Summary not found.'}


def test_get_summary_lists_all_existing_summaries(client, session):
    urls = ["www.bla.org", "www.blabla.org"]
    for url in urls:
        add_summary(session, url)

    response = client.get("/summaries/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["id"] == 1
    assert data[0]["url"] == urls[0]
    assert data[0]["summary"] is None
    assert data[1]["id"] == 2
    assert data[1]["url"] == urls[1]
    assert data[1]["summary"] is None


def test_get_summary_returns_empty_list_if_no_entries_available(client, session):
    response = client.get("/summaries/")
    assert response.status_code == 200
    assert response.json() == []


def test_post_summary_creates_entry(client, session):
    add_summary(session)
    response = client.post("/summaries/", json={"url": "https://www.blabla.org"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 2
    assert data["url"] == "https://www.blabla.org"
    assert data["summary"] is None


@pytest.mark.parametrize("data,expected",
                         [(123, "{'detail': [{'loc': ['body', 'url'], 'msg': 'invalid or missing URL scheme', "
                                "'type': 'value_error.url.scheme'}]}"),
                          ("no_url", "{'detail': [{'loc': ['body', 'url'], 'msg': 'invalid or missing URL scheme', "
                                     "'type': 'value_error.url.scheme'}]}"),
                          ("www.blabla.org", "{'detail': [{'loc': ['body', 'url'], 'msg': 'invalid or missing URL "
                                             "scheme', 'type': 'value_error.url.scheme'}]}")
                          ]
                         )
def test_post_summary_throws_error_when_sent_false_data(client, session, data, expected):
    response = client.post("/summaries/", json={"url": data})
    assert response.status_code != 201
    assert str(response.json()) == expected
