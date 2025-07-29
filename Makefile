# 🛍️ Pasar ML Agents - Makefile
# Simple helper commands for Docker & development

# Run all services (build if needed)
up:
	docker-compose up --build

# Stop all services
down:
	docker-compose down

# Rebuild all containers without cache
rebuild:
	docker-compose build --no-cache

# View logs (follow mode)
logs:
	docker-compose logs -f

# Stop all services and remove volumes (use with caution!)
reset:
	docker-compose down -v

# Run a single service (example: make xiara)
xiara:
	docker-compose up --build xiara

shogun:
	docker-compose up --build shogun

resolute:
	docker-compose up --build resolute

xena:
	docker-compose up --build xena
