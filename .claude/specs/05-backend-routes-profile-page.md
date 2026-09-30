# Spec: Backend Routes for Profile Page

## Overview
This step wires the `/profile` route to real database data, replacing every hardcoded dict and list in `app.py` with live queries against the `expenses` and `users` tables. New query helpers are added to `database/db.py` — a total-spent sum, a transaction count, a top-category look-up, a list of recent transactions, and a per-category breakdown. The `profile()` view in `app.py` is updated to fetch the real logged-in user and pass live data to the already-finished `profile.html` template. No template changes are required: the template is already data-driven from Step 4. The currency symbol is also corrected from `$` to `₹` to match the app's "Track every rupee" tagline.

## Depends on
- Step 1: Database setup (`users` and `expenses` tables must exist)
- Step 2: Registration (users must be creatable and stored)
- Step 3: Login + Logout (session must carry a real `user_id`)
- Step 4: Profile page UI (the template must already be in place)

## Routes
No new routes. The existing `GET /profile` route is updated to return real data.

## Database changes
No schema changes. The existing `users` and `expenses` tables are sufficient.

New helper functions to add to `database/db.py`:

| Function | Returns |
|---|---|
| `get_expenses_by_user(user_id)` | All expense rows for the user, ordered by date DESC |
| `get_expense_stats(user_id)` | Dict with `total_spent` (REAL), `transaction_count` (INT), `top_category` (TEXT) |
| `get_category_breakdown(user_id)` | List of dicts: `{name, amount, percent}`, ordered by amount DESC |

## Templates
- **Modify:** `templates/profile.html` — replace the hardcoded `$` currency symbol with `₹`. No structural changes.

## Files to change
- `database/db.py` — add `get_expenses_by_user`, `get_expense_stats`, and `get_category_breakdown`
- `app.py`:
  - Update imports to include the three new helpers
  - Replace the hardcoded dicts in `profile()` with real DB calls
  - Build the `user` dict from `get_user_by_id(session["user_id"])`
  - Format `member_since` from the user's `created_at` field (e.g. `"Sep 2026"`)
  - Pass real `stats`, `transactions` (most-recent 5), and `categories` to the template
- `templates/profile.html` — change `$` to `₹`

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()` only
- Parameterised queries only — never f-strings or `%` formatting in SQL
- Passwords hashed with werkzeug — no auth changes in this step
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- All DB logic must live in `database/db.py` — zero SQL in `app.py`
- `get_expense_stats` must compute `top_category` in SQL using `GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1` — do not compute it in Python
- `get_category_breakdown` must compute each category's percentage relative to the user's own total — not a fixed denominator
- If the user has no expenses, stats should return `{"total_spent": 0.0, "transaction_count": 0, "top_category": "—"}` and breakdown/transactions should return empty lists — the template must not crash on empty data
- `member_since` must be derived from `users.created_at` using Python's `datetime.strptime`, formatted as `"%b %Y"` (e.g. `"Sep 2026"`)
- Authentication guard stays: check `session.get("user_id")`; if absent, `redirect(url_for("login"))`. Also handle the case where `get_user_by_id` returns `None` (stale session) — clear the session and redirect to login
- Show only the 5 most-recent transactions on the profile page

## Definition of done
- [ ] Visiting `/profile` while logged in shows the real logged-in user's name and email, not "Demo User"
- [ ] `member_since` reflects the real `created_at` date from the database
- [ ] Total spent, transaction count, and top category all reflect the user's real expense data
- [ ] The 5 most-recent transactions shown match the user's actual DB rows (date, description, category, amount)
- [ ] The category breakdown percentages sum to 100% (or 0% if no expenses) and reflect the user's real data
- [ ] A brand-new user with no expenses sees the profile page without errors (empty-state handled)
- [ ] Currency symbol on the profile page is `₹`, not `$`
- [ ] No SQL appears in `app.py` — all queries are in `database/db.py`
- [ ] All new queries use `?` placeholders — no f-strings in SQL
- [ ] Logging in with a stale/deleted session redirects to `/login` rather than crashing
