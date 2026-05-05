from httpx import AsyncClient


async def test_admin_can_create_notification(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    resp = await client.post("/api/v1/notifications", json={
        "title": "Admin Notif",
        "message": "From admin",
        "audience_type": "ALL",
        "created_by": seed["alice"].id,
    })
    assert resp.status_code == 201


async def test_non_admin_cannot_create_notification(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    for name in ("bob", "carol", "dave", "eve", "frank"):
        resp = await client.post("/api/v1/notifications", json={
            "title": "Unauthorized",
            "message": "msg",
            "audience_type": "ALL",
            "created_by": seed[name].id,
        })
        assert resp.status_code == 403, f"{name} should be forbidden from creating notifications"


async def test_by_role_requires_role_ids(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    resp = await client.post("/api/v1/notifications", json={
        "title": "Missing roles",
        "message": "msg",
        "audience_type": "BY_ROLE",
        "role_ids": [],
        "created_by": seed["alice"].id,
    })
    assert resp.status_code == 422


async def test_unknown_creator_returns_404(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, _ = seeded_client
    resp = await client.post("/api/v1/notifications", json={
        "title": "Ghost",
        "message": "msg",
        "audience_type": "ALL",
        "created_by": 9999,
    })
    assert resp.status_code == 404


async def test_mark_read_unknown_notification_returns_404(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    resp = await client.patch("/api/v1/notifications/9999/read",
                              json={"user_id": seed["alice"].id, "is_read": True})
    assert resp.status_code == 404
