# Database Migration Guide (Alembic)

## Overview

This project uses **Alembic** for database schema migrations. Alembic is a lightweight database migration tool for SQLAlchemy that maintains migration history and allows safe rollbacks.

## Key Differences from Old System

| Feature          | Old System                   | Alembic                   |
| ---------------- | ---------------------------- | ------------------------- |
| Method           | `Base.metadata.create_all()` | Migration files + scripts |
| History Tracking | ❌ No                        | ✅ Yes                    |
| Rollback Support | ❌ No                        | ✅ Yes                    |
| Production-Safe  | ❌ No                        | ✅ Yes                    |
| Control          | Automatic                    | Manual (safer)            |

## Common Commands

### 1. Run All Pending Migrations

```bash
python -m alembic upgrade head
```

Or:

```bash
python app/migrations.py
```

### 2. Create a New Migration (After Changing Models)

```bash
python -m alembic revision --autogenerate -m "Add new column to users"
```

**Example:**

- You add a `phone` column to the User model
- Run the command above
- A new migration file is created automatically
- Run `python -m alembic upgrade head` to apply it

### 3. View Migration History

```bash
python -m alembic history
```

### 4. Rollback (Go Back to Previous Version)

```bash
python -m alembic downgrade -1
```

To go back 2 versions:

```bash
python -m alembic downgrade -2
```

To go back to a specific revision:

```bash
python -m alembic downgrade <revision_id>
```

### 5. Check Current Database Version

```bash
python -m alembic current
```

## Workflow

### Adding a New Model or Column

1. **Update the model** in `app/models/your_model.py`:

   ```python
   class User(Base):
       __tablename__ = "users"

       id = Column(Integer, primary_key=True)
       name = Column(String(100))
       phone = Column(String(20))  # New column
   ```

2. **Generate migration**:

   ```bash
   python -m alembic revision --autogenerate -m "Add phone to users"
   ```

3. **Review the migration file** in `alembic/versions/`:
   - Check that the changes look correct
   - Edit if needed

4. **Apply migration**:
   ```bash
   python -m alembic upgrade head
   ```

### Modifying a Migration (Before Applying)

If you created a migration but haven't applied it yet:

1. Edit the migration file in `alembic/versions/`
2. Run `python -m alembic upgrade head`

### After Applying a Migration

If you already ran a migration and need to modify it:

1. Revert the migration:

   ```bash
   python -m alembic downgrade -1
   ```

2. Edit the migration file

3. Reapply:
   ```bash
   python -m alembic upgrade head
   ```

## Migration File Structure

```python
# alembic/versions/6b58a9246c38_initial_migration.py

def upgrade() -> None:
    # Operations to apply (forward)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
    )

def downgrade() -> None:
    # Operations to undo (rollback)
    op.drop_table('users')
```

## Important Notes

⚠️ **Before Committing to Git:**

- Always review auto-generated migrations
- Test migrations on a test database first
- Commit both the model changes AND the migration file

📌 **Production Safety:**

- Alembic tracks applied migrations in `alembic_version` table
- Never delete migration files (even old ones)
- Always go forward with new migrations

## Troubleshooting

### Migration Failed to Generate

```bash
python -m alembic revision --autogenerate -m "Description"
```

If no changes are detected, ensure:

- You imported the model in `alembic/env.py`
- The model inherits from `Base`
- Changes are actually different from current schema

### Cannot Apply Migration

```bash
python -m alembic upgrade head
```

If you get connection errors:

- Check database is running
- Verify credentials in `app/core/config.py`
- Ensure `alembic_version` table exists

### View Pending Migrations

```bash
python -m alembic current
python -m alembic history
```

## Project Structure

```
camera_backend/
├── alembic/
│   ├── versions/           # Migration files
│   ├── env.py             # Alembic configuration
│   └── script.py.mako     # Migration template
├── alembic.ini            # Alembic settings
├── app/
│   ├── models/            # SQLAlchemy models
│   ├── migrations.py      # Migration runner
│   └── core/
│       └── database.py    # Database setup
└── requirements.txt
```

## Additional Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM Guide](https://docs.sqlalchemy.org/en/20/orm/)
