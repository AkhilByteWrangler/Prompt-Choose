#!/bin/bash

set -e

echo "Starting Prompt Selector..."

if [ ! -d "backend/venv" ] || [ ! -d "frontend/node_modules" ]; then
    echo "Running setup first..."
    ./setup.sh
fi

if [ ! -f "backend/.env" ]; then
    echo "Error: backend/.env not found"
    exit 1
fi

echo "Starting backend..."
cd backend
source venv/bin/activate
python manage.py runserver &
BACKEND_PID=$!
cd ..

echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
