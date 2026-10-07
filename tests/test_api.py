HEADERS = {"X-Agent-Token": "test-token"}


def report(client, status, message="", check="disk:/"):
    return client.post(
        "/api/v1/reports",
        headers=HEADERS,
        json={"hostname": "pc-01", "os": "Linux", "checks": [
            {"name": check, "status": status, "message": message}
        ]},
    )


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_rejects_bad_token(client):
    r = client.post("/api/v1/reports", headers={"X-Agent-Token": "wrong"},
                    json={"hostname": "x", "checks": []})
    assert r.status_code == 401


def test_problem_opens_one_ticket_then_auto_resolves(client):
    r1 = report(client, "warn", "85% used")
    assert len(r1.json()["opened"]) == 1

    # Same problem again: no duplicate ticket
    r2 = report(client, "warn", "86% used")
    assert r2.json()["opened"] == []
    assert len(client.get("/api/v1/tickets?state=open").json()) == 1

    # Problem clears: ticket auto-resolves
    r3 = report(client, "ok", "40% used")
    assert r3.json()["resolved"] == r1.json()["opened"]
    assert client.get("/api/v1/tickets?state=open").json() == []


def test_severity_escalates(client):
    report(client, "warn", "85% used")
    report(client, "crit", "97% used")
    [ticket] = client.get("/api/v1/tickets?state=open").json()
    assert ticket["severity"] == "crit"
    assert ticket["details"] == "97% used"


def test_host_registered(client):
    report(client, "ok")
    hosts = client.get("/api/v1/hosts").json()
    assert [h["hostname"] for h in hosts] == ["pc-01"]
