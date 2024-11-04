# Define directories
BACKEND_DIR=backend
MOBILE_DIR=mobile
DEVELOP_DIR=develop
VENV=.venv

# Docker Compose file path
DOCKER_COMPOSE=$(DEVELOP_DIR)/docker-compose.yml

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make install        Create venv and install dependencies for backend and mobile"
	@echo "  make up             Start the entire application (backend, mobile, Docker Compose)"
	@echo "  make down           Stop the entire application (backend, mobile, Docker Compose)"
	@echo "  make backend        Run the FastAPI backend locally (with venv)"
	@echo "  make mobile         Run the mobile app (Expo)"
	@echo "  make develop        Provision Docker Compose services"
	@echo "  make logs           View Docker Compose logs"
	@echo "  make lint-backend   Run linter for backend"
	@echo "  make lint-mobile    Run linter for mobile app"
	@echo "  make clean          Clean up containers, images, and volumes"

# Create virtual environment and install dependencies for backend and mobile
.PHONY: install
install:
	@echo "Creating Python virtual environment for backend..."
	cd $(BACKEND_DIR) && python3 -m venv .venv
	@echo "Installing backend dependencies (with venv)..."
	cd $(BACKEND_DIR) && source $(VENV)/bin/activate && pip install -r requirements.txt
	@echo "Installing mobile dependencies..."
	cd $(MOBILE_DIR) && npm install

# Start the entire application (backend, mobile, Docker Compose services)
.PHONY: up
up:
	@echo "Starting the entire application..."
	docker-compose -f $(DOCKER_COMPOSE) up -d
	@echo "Starting FastAPI backend..."
	cd $(BACKEND_DIR) && source $(VENV)/bin/activate && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 &
	@echo "Starting the Expo mobile app..."
	cd $(MOBILE_DIR) && npm start &

# Stop the entire application (backend, mobile, Docker Compose services)
.PHONY: down
down:
	@echo "Stopping the entire application..."
	docker-compose -f $(DOCKER_COMPOSE) down
	@echo "Stopping backend and mobile processes..."
	# Killing background processes (backend and mobile)
	@pkill -f "uvicorn src.main:app" || true
	@pkill -f "npm start" || true

# Run FastAPI backend (with venv)
.PHONY: backend
backend:
	@echo "Running FastAPI backend (with venv)..."
	cd $(BACKEND_DIR) && source $(VENV)/bin/activate && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run the Expo mobile app
.PHONY: mobile
mobile:
	@echo "Running the Expo mobile app..."
	cd $(MOBILE_DIR) && npm run start 

# Provision Docker Compose services (e.g., setting up databases, Redis)
.PHONY: develop
develop:
	@echo "Provisioning Docker Compose services..."
	docker-compose -f $(DOCKER_COMPOSE) up -d --build

# View logs for Docker Compose services
.PHONY: logs
logs:
	@echo "Viewing logs for Docker Compose services..."
	docker-compose -f $(DOCKER_COMPOSE) logs -f

# Lint the backend Python code (with venv)
.PHONY: lint-backend
lint-backend:
	@echo "Linting the backend code (with venv)..."
	cd $(BACKEND_DIR) && source $(VENV)/bin/activate && flake8 .

# Lint the mobile app code
.PHONY: lint-mobile
lint-mobile:
	@echo "Linting the mobile app code..."
	cd $(MOBILE_DIR) && npm run lint

# Clean up Docker containers, images, and volumes
.PHONY: clean
clean:
	@echo "Cleaning up Docker containers, images, and volumes..."
	docker-compose -f $(DOCKER_COMPOSE) down -v --rmi all
