#!/bin/bash

set -e

echo "Setting up Prompt Selector..."
echo ""

if ! command -v mongosh &> /dev/null; then
    echo "Warning: MongoDB not found"
    echo "Install: brew install mongodb-community or use MongoDB Atlas"
    read -p "Press Enter to continue..."
fi

if [ ! -f "backend/.env" ]; then
    echo "Creating .env from template..."
    cp backend/.env.example backend/.env
    echo "Edit backend/.env with your OPENAI_API_KEY"
    read -p "Press Enter to continue..."
fi

echo "Backend setup..."
cd backend
[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo "Backend ready"

echo ""
echo "Frontend setup..."
cd ../frontend
npm install
echo "Frontend ready"

echo ""
echo "Setup complete!"
echo "Run ./start.sh to start both servers"
