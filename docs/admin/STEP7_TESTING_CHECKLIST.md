# Step 7 Admin Dashboard Testing Checklist

## Local backend test

Start backend:

```bash
cd backend
uvicorn main:app --reload
```

Check:

```bash
curl http://localhost:8000/health
```

## Admin key test

```bash
curl -H "x-admin-key: YOUR_ADMIN_API_KEY" "http://localhost:8000/admin/leads?limit=10"
```

Expected: JSON with `count` and `leads`.

## Dashboard test

1. Run admin dashboard.
2. Enter backend URL.
3. Enter admin key.
4. Dashboard should show metrics and lead table.
5. Search by parent name or phone.
6. Filter by priority.
7. Open a lead details modal.
8. Export leads CSV.
9. Export chat logs CSV.

## Responsive test

Check dashboard on:

- Desktop
- Tablet width
- Mobile width

## Production test

1. Deploy backend.
2. Deploy admin dashboard.
3. Add admin dashboard URL to backend CORS.
4. Open deployed dashboard.
5. Connect using production backend URL and admin key.
6. Confirm leads load.
7. Confirm CSV export works.
