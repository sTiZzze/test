import datetime

import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from main import app

@pytest.mark.anyio('anyio_backend', ['asyncio'])
async def test_simple_workflow():
    deadline = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)


    test_event = {
        'odds': '1.00',
        'deadline': deadline.isoformat() + 'Z',
        'status': "незавершённое"
    }

    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        # Создание события
        response = await ac.post('http://localhost/api/v1/events', json=test_event)
        data = response.json()
        test_id = data.get("id")
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Body: {response.text}"


    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        response = await ac.get(f'http://localhost/api/v1/events/{test_id}')
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Body: {response.text}"
        response_data = response.json()
        assert response_data['odds'] == test_event[
            'odds'], f"Expected odds {test_event['odds']}, got {response_data['odds']}"
        assert response_data['deadline'] == test_event[
            'deadline'], f"Expected deadline {test_event['deadline']}, got {response_data['deadline']}"
        assert response_data['status'] == test_event[
            'status'], f"Expected status {test_event['status']}, got {response_data['status']}"

    updated_event = test_event.copy()
    updated_event['status'] = "завершено выигрышем первой команды"

    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        # Обновление статуса события
        update_response = await ac.patch(f'http://localhost/api/v1/events/{test_id}/status', json={'status': updated_event['status']})
        assert update_response.status_code == 200, f"Unexpected status code: {update_response.status_code}, Body: {update_response.text}"

    async with AsyncClient(transport=ASGITransport(app=app)) as ac:
        # Получение обновленного события
        response = await ac.get(f'http://localhost/api/v1/events/{test_id}')
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Body: {response.text}"
        response_data = response.json()
        assert response_data['odds'] == updated_event[
            'odds'], f"Expected odds {updated_event['odds']}, got {response_data['odds']}"
        assert response_data['deadline'] == test_event[
            'deadline'], f"Expected deadline {updated_event['deadline']}, got {response_data['deadline']}"
        assert response_data['status'] == updated_event[
            'status'], f"Expected status {updated_event['status']}, got {response_data['status']}"
