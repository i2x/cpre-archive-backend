# 🔹 Development
dev:
	docker-compose -f docker-compose.dev.yml up --build

# 🔥 Production
prod:
	docker-compose -f docker-compose.prod.yml up --build -d

# ❌ Stop ทั้ง Dev และ Prod
stop:
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.prod.yml down

# 🛠 Migrate สำหรับ Dev & Prod
migrate:
	docker-compose -f docker-compose.dev.yml run backend python manage.py migrate
	docker-compose -f docker-compose.prod.yml run backend python manage.py migrate

# 📂 Load Fixtures (Data) เข้า Database
loaddata:
	docker-compose -f docker-compose.dev.yml run backend python manage.py loaddata data.json
	docker-compose -f docker-compose.prod.yml run backend python manage.py loaddata data.json

# 🧹 Cleanup
clean:
	docker system prune -af
