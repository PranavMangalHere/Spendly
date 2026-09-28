from database.db import get_user_by_email


def register(client, name="Test User", email="testuser1@example.com", password="password123"):
    return client.post(
        "/register",
        data={"name": name, "email": email, "password": password},
        follow_redirects=False,
    )


def test_get_register_renders_form(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"auth-error" not in response.data


def test_valid_registration_creates_user_and_redirects(client):
    response = register(client)
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"

    user = get_user_by_email("testuser1@example.com")
    assert user is not None
    assert user["name"] == "Test User"
    assert user["password_hash"] != "password123"
    assert user["password_hash"].startswith(("pbkdf2:", "scrypt:"))


def test_duplicate_email_shows_error_and_does_not_duplicate(client):
    register(client)
    response = register(client)

    assert response.status_code == 200
    assert b"already exists" in response.data

    conn = get_user_by_email("testuser1@example.com")
    assert conn is not None


def test_missing_name_shows_error(client):
    response = register(client, name="")
    assert response.status_code == 200
    assert b"Full name is required" in response.data
    assert get_user_by_email("testuser1@example.com") is None


def test_invalid_email_format_shows_error(client):
    response = register(client, email="notanemail")
    assert response.status_code == 200
    assert b"valid email address" in response.data


def test_short_password_shows_error(client):
    response = register(client, password="short")
    assert response.status_code == 200
    assert b"at least 8 characters" in response.data
    assert get_user_by_email("testuser1@example.com") is None
