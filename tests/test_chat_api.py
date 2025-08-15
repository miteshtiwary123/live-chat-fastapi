import pytest

@pytest.mark.asyncio
async def test_chat_history_empty(async_client):
    response = await async_client.get("/chat/history")
    assert response.status_code == 200
    assert response.json() == []
    