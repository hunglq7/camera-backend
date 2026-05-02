#!/bin/bash
# Script helper để tạo migration file nhanh

if [ -z "$1" ]; then
    echo "Usage: ./create_migration.sh 'migration_name'"
    echo "Example: ./create_migration.sh 'add_danh_muc_table'"
    exit 1
fi

docker-compose exec app python -m alembic revision --autogenerate -m "$1"
echo "✅ Migration file created!"
echo "🔄 Restarting containers to apply migration..."
docker-compose restart app
