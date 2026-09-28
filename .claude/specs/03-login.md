# Spec: Login and Logout

## Overview
This step implements real authentication for Spendly. The `GET /login` route already
renders `login.html`, but the form posts to `/login` with no `POST` handler and there
is no session mechanism yet — anyone can currently reach any page without signing in.
This step adds `POST /login` to verify credentials and establish a session, and
implements the `GET /logout` route (currently a stub) to clear it. This unlocks the
next roadmap steps (Step 4 — Profile, and the expense CRUD steps), which all require
knowing who the logged-in user is.

## Depends on
- Step 1 (Database setup) — `users` table, `get_db()`, `get_user_by_email()`
- Step 2 (Registration) — users must be able to register before they can log in

## Routes
- `POST /login` — verify email + password, start a session, redirect to profile/dashboard on success, re-render `login.html` with an error on failure — public
- `GET /logout` — clear the session and redirect to `login` — logged-in

`GET /login` already exists and needs no signature change, but should redirect
already-logged-in users away from the form.

## Database changes
No database changes. `users.password_hash` (from `database/db.py`) is sufficient to
verify credentials with `werkzeug.security.check_password_hash`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html` — no structural changes expected; already posts to `/login` and already renders `{{ error }}`
  - `templates/base.html` — nav currently always shows "Sign in" / "Get started"; once sessions exist it should conditionally show "Sign out" (and a profile link) when a user is logged in

## Files to change
- `app.py` — add `POST` handling to `/login`, implement `/logout`, add a `login_required` guard usable by future stub routes, set `app.secret_key` for session support
- `database/db.py` — add `get_user_by_id(user_id)` helper if needed for session-based lookups (verify against existing helpers before adding)
- `templates/base.html` — conditional nav based on session state

## Files to create
None.

## New dependencies
No new dependencies. Flask's built-in `session` and `werkzeug.security.check_password_hash` cover this step.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug (`check_password_hash` against the stored `password_hash`)
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Never use raw string returns for `/logout` once implemented — always redirect or render a template
- Store only `user_id` in the Flask session, never the password hash
- `app.secret_key` must be set for sessions to work — flag if it needs to come from an env var vs. a hardcoded dev default

## Definition of done
- [ ] Visiting `/login` while logged out shows the sign-in form
- [ ] Submitting `/login` with the seeded demo user (`demo@spendly.com` / `demo123`) redirects successfully and starts a session
- [ ] Submitting `/login` with a wrong password re-renders `login.html` with an error and does not start a session
- [ ] Submitting `/login` with an email that doesn't exist re-renders `login.html` with an error
- [ ] Visiting `/logout` while logged in clears the session and redirects to `/login`
- [ ] After logout, the nav bar shows "Sign in" / "Get started" again
- [ ] While logged in, the nav bar reflects the signed-in state (e.g. shows "Sign out")
- [ ] Visiting `/login` while already logged in does not show the form (redirects away)
