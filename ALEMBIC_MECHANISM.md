# Cơ Chế Hoạt Động của Alembic Migration

## 1. So Sánh: Cũ vs Mới

### ❌ Cách Cũ (Loại bỏ rồi)

```python
# Không dùng nữa!
Base.metadata.create_all(bind=engine)
```

**Vấn đề:**

- Tự động tạo ALL bảng cùng lúc
- Nếu bảng đã tồn tại → bỏ qua (không update)
- Không theo dõi lịch sử thay đổi
- Không thể rollback

### ✅ Cách Mới (Alembic)

```bash
python -m alembic upgrade head
```

**Ưu điểm:**

- Tạo/cập nhật bảng từng bước (có kiểm soát)
- Theo dõi lịch sử mọi thay đổi
- Có thể rollback về version cũ
- An toàn cho production

---

## 2. Kiến Trúc Alembic

### Cấu Trúc Thư Mục

```
camera_backend/
├── alembic/                          # Thư mục Alembic
│   ├── versions/                     # Chứa các file migration
│   │   ├── 6b58a9246c38_initial_migration.py  # Migration 1
│   │   └── (migration files khác)    # Migration 2, 3, ...
│   ├── env.py                        # Cấu hình Alembic
│   └── script.py.mako                # Template cho migration
├── alembic.ini                       # Tệp cấu hình chính
├── app/
│   ├── models/                       # SQLAlchemy models
│   │   ├── camera.py
│   │   ├── user.py
│   │   └── ...
│   ├── migrations.py                 # Runner (chạy migration)
│   └── core/
│       └── database.py               # Thiết lập database
└── requirements.txt
```

---

## 3. Quy Trình Hoạt Động

### Bước 1: Xác định Thay Đổi

```
Bạn sửa model (thêm cột, xóa cột, v.v)
     ↓
Chạy: python -m alembic revision --autogenerate -m "Description"
     ↓
Alembic so sánh:
  - Mô tả model trong code (app/models/)
  - Cơ sở dữ liệu hiện tại
     ↓
Tạo file migration mới (nếu có khác biệt)
```

**Ví dụ:**

```python
# app/models/user.py (bạn thêm cột phone)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    phone = Column(String(20))  # ← Cột mới
```

Alembic phát hiện và tạo migration:

```python
# alembic/versions/xxxxx_add_phone_to_users.py
def upgrade():
    op.add_column('users',
        sa.Column('phone', sa.String(length=20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

### Bước 2: Áp Dụng Migration

```
Bạn chạy: python app/migrations.py
        hoặc: python -m alembic upgrade head
     ↓
Alembic kiểm tra: Bảng "alembic_version" có revision gì?
     ↓
So sánh với các migration files:
  - Migration nào đã applied? ✓ (skip)
  - Migration nào chưa applied? ✗ (chạy)
     ↓
Chạy từng upgrade() của migration chưa applied
     ↓
Cập nhật "alembic_version" table
```

### Bước 3: Lưu Lịch Sử

```
Database "alembic_version" table:
┌────────────────────┐
│ version_num        │
├────────────────────┤
│ 6b58a9246c38       │ ← Migration 1 đã applied
│ 7c69b3346d49       │ ← Migration 2 đã applied
│ 8d70c4456e50       │ ← Migration 3 đã applied
└────────────────────┘
```

---

## 4. Sơ Đồ Luồng Dữ Liệu

```
┌─────────────────────────────────────────────────────────────┐
│              BẠN THAY ĐỔI MODEL                             │
│              (app/models/camera.py)                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ↓
        ┌────────────────────────────┐
        │ alembic revision            │
        │ --autogenerate -m "..."     │
        └────────────┬─────────────────┘
                     │
        ┌────────────↓──────────────┐
        │ Alembic Autogenerate      │
        │ (So sánh models vs DB)    │
        └────────────┬──────────────┘
                     │
        ┌────────────↓──────────────────────┐
        │ Tạo file migration                │
        │ alembic/versions/xxxxx_...py      │
        │ (Chứa upgrade() + downgrade())    │
        └────────────┬──────────────────────┘
                     │
                     ↓
        ┌────────────────────────────┐
        │ python app/migrations.py   │
        │ (Chạy alembic upgrade)     │
        └────────────┬─────────────────┘
                     │
        ┌────────────↓──────────────────────┐
        │ Alembic Runtime                  │
        │ - Kiểm tra alembic_version table│
        │ - Chạy từng migration chưa apply│
        │ - Cập nhật version tracking      │
        └────────────┬──────────────────────┘
                     │
                     ↓
        ┌────────────────────────────┐
        │ Database được cập nhật     │
        │ (Bảng mới/cột mới được    │
        │  tạo)                      │
        └────────────────────────────┘
```

---

## 5. Chi Tiết Migration File

### Cấu Trúc

```python
# alembic/versions/6b58a9246c38_initial_migration.py

"""Initial migration

Revision ID: 6b58a9246c38          # ID duy nhất cho migration này
Revises:                            # Migration trước (null = first)
Create Date: 2026-04-30 ...
"""

revision = '6b58a9246c38'           # ID này
down_revision = None                # Migration trước
branch_labels = None
depends_on = None

def upgrade() -> None:              # Chạy khi: alembic upgrade
    """Thay đổi để áp dụng (forward)"""
    op.create_table('cameras',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:            # Chạy khi: alembic downgrade
    """Đảo ngược thay đổi (backward)"""
    op.drop_table('cameras')
```

### Ý Nghĩa Revision Chain

```
Revision: 6b58a9246c38  →  7c69b3346d49  →  8d70c4456e50
(Initial)                 (Add phone)      (Remove email)
   ↓                          ↓                  ↓
down_rev: None          down_rev: 6b...  down_rev: 7c...

Khi downgrade -2:
Current 8d... → downgrade() → 7c... → downgrade() → 6b... → None
```

---

## 6. Các Lệnh Thường Dùng

### 1️⃣ Chạy Migration (Áp dụng vào DB)

```bash
python app/migrations.py              # Áp dụng tất cả chưa applied
python -m alembic upgrade head        # Tương tự
python -m alembic upgrade +1          # Áp dụng 1 migration tiếp theo
```

### 2️⃣ Tạo Migration Mới (Từ thay đổi model)

```bash
python -m alembic revision --autogenerate -m "Add phone to users"
# Tạo file: alembic/versions/xxxxx_add_phone_to_users.py
```

### 3️⃣ Quay Lùi (Undo)

```bash
python -m alembic downgrade -1        # Quay lại 1 version
python -m alembic downgrade 6b58a9    # Quay lại version cụ thể
python -m alembic downgrade base      # Quay lại trước tất cả
```

### 4️⃣ Xem Lịch Sử

```bash
python -m alembic history              # Liệt kê tất cả migrations
python -m alembic current              # Version hiện tại trong DB
```

### 5️⃣ Kiểm Tra Thay Đổi

```bash
python -m alembic heads                # Xem tip (mới nhất)
```

---

## 7. Ví Dụ Thực Tế: Thêm Cột Vào User Model

### Step 1: Chỉnh Model

```python
# app/models/user.py
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))  # ← Thêm dòng này
```

### Step 2: Tạo Migration

```bash
$ python -m alembic revision --autogenerate -m "Add phone to users"

INFO  [alembic.autogenerate.compare.tables] Detected added column 'users.phone'
Generating alembic/versions/7c69b3346d49_add_phone_to_users.py ... done
```

### Step 3: Xem File Generated

```python
# alembic/versions/7c69b3346d49_add_phone_to_users.py

def upgrade() -> None:
    op.add_column('users',
        sa.Column('phone', sa.String(length=20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone')
```

### Step 4: Áp Dụng

```bash
$ python app/migrations.py

Running Alembic migrations...
INFO  [alembic.runtime.migration] Running upgrade 6b58a9246c38 -> 7c69b3346d49, Add phone to users
✓ Migration completed successfully!
```

### Step 5: Kiểm Tra

```bash
$ python -m alembic current

7c69b3346d49 (head)

$ python -m alembic history

<base> -> 6b58a9246c38 (initial_migration), 2026-04-30 09:18
6b58a9246c38 -> 7c69b3346d49 (add_phone_to_users), 2026-04-30 10:25
```

---

## 8. Rollback Example

```bash
# Nếu muốn quay lại trước khi thêm phone:
$ python -m alembic downgrade -1

INFO  [alembic.runtime.migration] Running downgrade 7c69b3346d49 -> 6b58a9246c38, Add phone to users
✓ Migration completed successfully!

# Kiểm tra
$ python -m alembic current
6b58a9246c38 (head)
```

---

## 9. Workflow Tóm Tắt

```
┌─────────────────────────────────────────────┐
│  1. Sửa model trong app/models/             │
│  2. python -m alembic revision --autogenerate -m "..."  │
│  3. Review file migration được generate      │
│  4. python app/migrations.py                │
│  5. Kiểm tra: python -m alembic current     │
│  6. Commit to Git (model + migration file)  │
└─────────────────────────────────────────────┘
```

---

## 10. Lợi Ích Của Alembic

| Tính Năng          | Lợi Ích                                   |
| ------------------ | ----------------------------------------- |
| 📜 Version Control | Mỗi thay đổi được ghi lại với ID duy nhất |
| ⏮️ Rollback        | Có thể quay lại version cũ nếu có lỗi     |
| 📊 Tracking        | Biết chính xác DB version hiện tại        |
| 👥 Team Collab     | Dễ share migrations với team              |
| 🛡️ Production Safe | Không tự động tạo/xóa (phải chủ động)     |
| 🔍 Audit Trail     | Lịch sử mọi thay đổi database             |
| 🎯 Controlled      | Bạn kiểm soát khi nào apply migration     |

---

## 11. Best Practices

✅ **LÀM:**

- Luôn xem lại file migration trước khi apply
- Commit cả model changes và migration file
- Đặt tên migration rõ ràng (ví dụ: "Add email verification")
- Thử test migration trên test DB trước
- Giữ các migration file (đừng xóa cũ)

❌ **KHÔNG LÀM:**

- Chỉnh sửa migration file sau khi applied
- Xóa migration file cũ
- Tự viết SQL trong migration (dùng SQLAlchemy operations)
- Skip migration và apply trực tiếp vào DB
- Quên commit migration file

---

**Tóm lại:** Alembic là hệ thống quản lý database schema giống như Git, nhưng cho database! 🚀
