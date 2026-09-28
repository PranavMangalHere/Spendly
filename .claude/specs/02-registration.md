# Spec: Registration

## Overview
This step implements account creation for Spendly. `GET /register` already
renders `register.html`, but submitting the form does nothing yet — there is
no `POST /register` handler and no logic to validate input, hash passwords,
or persist new users. This step wires up that logic on top of the data layer
built in Step 1, so a visitor can create an account and land on the login
page to sign in. Session handling and actually logging a user in are out of
scope here — they belong to the login/logout step.

## Depends on
- Step 1 — Database Setup (`database/db.py` schema, `get_db()`, `users` table)

## Routes
- `POST /register` — validate submitted name/email/password, create the user, redirect to `/login` on success or re-render `register.html` with an error on failure — public

## Database changes
No database changes. The `users` table (id, name, email, password_hash,
created_at) already supports this feature as defined in
`database/db.py`.

New functions needed in `database/db.py` (logic only, no schema change):
- `get_user_by_email(email)` — returns a user row or `None`
- `create_user(name, email, password_hash)` — inserts a new user, returns the new `id`

## Templates
- **Create:** none
- **Modify:** `templates/register.html` — change the form's hardcoded `action="/register"` to `action="{{ url_for('register') }}"` per the no-hardcoded-URLs rule; the existing `{% if error %}` block is reused to surface validation errors

## Files to change
- `app.py` — replace the `register` route with a function handling both `GET` and `POST`, calling into `database/db.py` for lookups/inserts
- `database/db.py` — add `get_user_by_email()` and `create_user()`
- `templates/register.html` — fix hardcoded form action

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security` (already used in `db.py`) provides `generate_password_hash`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`generate_password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- No inline DB logic in `app.py` — all queries live in `database/db.py`
- Validate on the server even though the form has `required`/`type=email` attributes client-side
- Duplicate email must re-render `register.html` with a clear error, not raise an unhandled exception
- Do not implement session/login logic — that belongs to a later step

## Definition of done
- [ ] Submitting the register form with valid, unique details creates a row in `users` with a hashed password and redirects to `/login`
- [ ] Submitting with an email that already exists re-renders `register.html` showing an error, and does not create a duplicate row
- [ ] Submitting with a missing name, invalid email format, or password under 8 characters re-renders `register.html` with an error and does not create a row
- [ ] No plaintext password is ever written to the database or logged
- [ ] `GET /register` still renders the form as before
- [ ] All new queries in `database/db.py` use `?` placeholders, none use f-strings/string formatting
- [ ] App starts and runs without errors on `python app.py`
