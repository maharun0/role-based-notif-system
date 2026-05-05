from httpx import AsyncClient


async def test_list_users_returns_all_six(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    resp = await client.get("/api/v1/users")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 6
    emails = {u["email"] for u in users}
    assert "alice@example.com" in emails
    assert "frank@example.com" in emails


async def test_list_users_includes_role(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, _ = seeded_client
    resp = await client.get("/api/v1/users")
    assert resp.status_code == 200
    for user in resp.json():
        assert "role" in user
        assert "name" in user["role"]


async def test_get_user_by_id(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id
    resp = await client.get(f"/api/v1/users/{alice_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert data["role"]["name"] == "Admin"


async def test_get_user_not_found(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, _ = seeded_client
    resp = await client.get("/api/v1/users/9999")
    assert resp.status_code == 404
