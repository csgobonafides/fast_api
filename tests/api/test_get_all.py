import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all(xclient: AsyncClient):
    response = await xclient.get('/lamps/')
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": "1", "name": "gauss", "price": 134.2, "article": 112233},
        {"id": "2", "name": "sweko", "price": 89.0, "article": 441122},
        {"id": "3", "name": "uniel", "price": 13.2, "article": 379283}
    ]


@pytest.mark.asyncio
async def test_get_all_two(xclient: AsyncClient):
    response = await xclient.get('/lamps/')
    assert response.status_code == 200, response.text
    assert len(response.json()) == 3, response.text
    assert response.json() == [
                {
                    'article': 112233,
                    'id': '1',
                    'name': 'gauss',
                    'price': 134.2,
                },
                {
                    'article': 441122,
                    'id': '2',
                    'name': 'sweko',
                    'price': 89.0,
                },
                {
                    'article': 379283,
                    'id': '3',
                    'name': 'uniel',
                    'price': 13.2,
                },
           ]