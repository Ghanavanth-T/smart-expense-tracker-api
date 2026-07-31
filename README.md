# smart-expense-tracker-api
REST API for tracking personal expenses — add, filter by category, aggregate totals, delete. FastAPI with JSON file persistence, validated with Pydantic, tested with pytest.


## API Contract

| Method | Endpoint            | Behaviour                                      |
|--------|---------------------|------------------------------------------------|
| POST   | `/expenses`         | Creates an expense. Returns 201 + full object. |
| GET    | `/expenses`         | Lists all. Optional `?category=` filter.       |
| GET    | `/expenses/summary` | Overall total + per-category breakdown.        |
| DELETE | `/expenses/{id}`    | Deletes by id. 404 if not found.               |

### Expense fields

| Field      | Type   | Rules                                          |
|------------|--------|------------------------------------------------|
| `id`       | string | UUID4, server-generated. Never client-supplied. |
| `title`    | string | Required, min length 1.                        |
| `amount`   | float  | Must be > 0.                                   |
| `category` | string | Free text, lowercased on input.                |
| `date`     | date   | ISO format `YYYY-MM-DD`.                       |

### Design notes

- `amount` is a `float` for scope reasons. Production code should use
  `Decimal` to avoid floating-point rounding on currency.
- `amount > 0` means refunds and negative adjustments are out of scope.
- Data persists to `data/expenses.json`, created on first write. A missing
  or unreadable file is treated as an empty expense list.