from httpx import AsyncClient


async def test_create_all_every_user_receives(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    resp = await client.post("/api/v1/notifications", json={
        "title": "Broadcast",
        "message": "Hello everyone",
        "audience_type": "ALL",
        "created_by": seed["alice"].id,
    })
    assert resp.status_code == 201
    notif_id = resp.json()["id"]

    for user in seed.values():
        r = await client.get(f"/api/v1/users/{user.id}/notifications")
        assert r.status_code == 200
        notif_ids = [n["notification_id"] for n in r.json()]
        assert notif_id in notif_ids, f"{user.name} should have received the broadcast"


async def test_create_by_role_only_managers_receive(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client

    roles_resp = await client.get("/api/v1/roles")
    roles = {r["name"]: r["id"] for r in roles_resp.json()}

    resp = await client.post("/api/v1/notifications", json={
        "title": "Manager Only",
        "message": "For managers",
        "audience_type": "BY_ROLE",
        "role_ids": [roles["Manager"]],
        "created_by": seed["alice"].id,
    })
    assert resp.status_code == 201
    notif_id = resp.json()["id"]

    for name in ("bob", "frank"):
        r = await client.get(f"/api/v1/users/{seed[name].id}/notifications")
        notif_ids = [n["notification_id"] for n in r.json()]
        assert notif_id in notif_ids, f"{name} (Manager) should have received the notification"

    for name in ("carol", "dave", "eve"):
        r = await client.get(f"/api/v1/users/{seed[name].id}/notifications")
        notif_ids = [n["notification_id"] for n in r.json()]
        assert notif_id not in notif_ids, f"{name} should NOT have received the notification"


async def test_notifications_reverse_chronological(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id

    for title in ("First", "Second"):
        await client.post("/api/v1/notifications", json={
            "title": title, "message": "msg", "audience_type": "ALL", "created_by": alice_id,
        })

    resp = await client.get(f"/api/v1/users/{seed['bob'].id}/notifications")
    titles = [n["notification"]["title"] for n in resp.json()]
    assert titles.index("Second") < titles.index("First")


async def test_unread_count(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    carol_id = seed["carol"].id

    before = (await client.get(f"/api/v1/users/{carol_id}/notifications/unread-count")).json()["unread_count"]

    await client.post("/api/v1/notifications", json={
        "title": "Count Test", "message": "msg", "audience_type": "ALL",
        "created_by": seed["alice"].id,
    })

    after = (await client.get(f"/api/v1/users/{carol_id}/notifications/unread-count")).json()["unread_count"]
    assert after == before + 1


async def test_mark_as_read(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id
    dave_id = seed["dave"].id

    create_resp = await client.post("/api/v1/notifications", json={
        "title": "Read Test", "message": "msg", "audience_type": "ALL", "created_by": alice_id,
    })
    notif_id = create_resp.json()["id"]

    resp = await client.patch(f"/api/v1/notifications/{notif_id}/read",
                              json={"user_id": dave_id, "is_read": True})
    assert resp.status_code == 200
    assert resp.json()["is_read"] is True
    assert resp.json()["read_at"] is not None

    resp = await client.patch(f"/api/v1/notifications/{notif_id}/read",
                              json={"user_id": dave_id, "is_read": False})
    assert resp.json()["is_read"] is False
    assert resp.json()["read_at"] is None


async def test_filter_by_is_read(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id
    bob_id = seed["bob"].id

    create_resp = await client.post("/api/v1/notifications", json={
        "title": "Filter Test", "message": "msg", "audience_type": "ALL", "created_by": alice_id,
    })
    notif_id = create_resp.json()["id"]

    await client.patch(f"/api/v1/notifications/{notif_id}/read",
                       json={"user_id": bob_id, "is_read": True})

    unread = await client.get(f"/api/v1/users/{bob_id}/notifications?is_read=false")
    assert notif_id not in [n["notification_id"] for n in unread.json()]

    read = await client.get(f"/api/v1/users/{bob_id}/notifications?is_read=true")
    assert notif_id in [n["notification_id"] for n in read.json()]


async def test_search_by_title(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id
    bob_id = seed["bob"].id

    await client.post("/api/v1/notifications", json={
        "title": "Unique XYZ123 Title", "message": "body", "audience_type": "ALL",
        "created_by": alice_id,
    })
    await client.post("/api/v1/notifications", json={
        "title": "Unrelated", "message": "nothing here", "audience_type": "ALL",
        "created_by": alice_id,
    })

    resp = await client.get(f"/api/v1/users/{bob_id}/notifications?search=XYZ123")
    results = resp.json()
    assert len(results) >= 1
    assert all("XYZ123" in n["notification"]["title"] or "XYZ123" in n["notification"]["message"]
               for n in results)


async def test_search_by_message(seeded_client: tuple[AsyncClient, dict]) -> None:
    client, seed = seeded_client
    alice_id = seed["alice"].id

    await client.post("/api/v1/notifications", json={
        "title": "No Match Title", "message": "SearchableABC content", "audience_type": "ALL",
        "created_by": alice_id,
    })

    resp = await client.get(f"/api/v1/users/{seed['carol'].id}/notifications?search=SearchableABC")
    assert len(resp.json()) >= 1
