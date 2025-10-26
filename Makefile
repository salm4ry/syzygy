# for sourcing scripts
SHELL := /bin/bash

.PHONY: dev-backend dev-frontend

# run Flask backend in dev mode
dev-backend:
	source .venv/bin/activate && python3 app.py

# run SvelteKit frontend in dev mode
dev-frontend:
	cd frontend && npm run dev
