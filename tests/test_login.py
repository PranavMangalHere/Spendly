from test_registration import register


def login(client, email="testuser1@example.com", password="password123"):
    return client.post(
        "/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


def test_get_login_renders_form(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"auth-error" not in response.data


def test_valid_login_sets_session_and_redirects(client):
    register(client)
    response = login(client)

    assert response.status_code == 302
    assert response.headers["Location"] == "/"

    with client.session_transaction() as sess:
        assert "user_id" in sess


def test_invalid_password_shows_error(client):
    register(client)
    response = login(client, password="wrongpassword")

    assert response.status_code == 200
    assert b"Invalid email or password." in response.data

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_unknown_email_shows_error(client):
    response = login(client, email="nosuchuser@example.com")

    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_logout_clears_session_and_redirects(client):
    register(client)
    login(client)

    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_get_login_redirects_when_already_logged_in(client):
    register(client)
    login(client)

    response = client.get("/login")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
