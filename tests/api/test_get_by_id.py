import pytest
from httpx import AsyncClient
from schemas.lamps import LampDtlInfo


@pytest.mark.asyncio
@pytest.mark.parametrize("lamp_id, expected", [
    ("1", {"id": "1", "name": "gauss", "price": 134.2, "shape": "R50", "base": "E14", "temperature": "cw"}),
    ("2", {"id": "2", "name": "sweko", "price": 89.0, "shape": "A60", "base": "E27", "temperature": "nw"}),
    ("3", {"id": "3", "name": "uniel", "price": 13.2, "shape": "A60", "base": "E27", "temperature": "nw"})
    ])
async def test_get_by_id_200(xclient: AsyncClient, lamp_id, expected: LampDtlInfo):
    response = await xclient.get(f"/lamps/{lamp_id}")
    assert response.status_code == 200, response.text
    assert response.json() == expected


@pytest.mark.asyncio
async def test_get_by_id_404(xclient: AsyncClient):
    response = await xclient.get("/lamps/999")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Такого ключа не найдено."}