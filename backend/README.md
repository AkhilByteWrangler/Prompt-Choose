# Django Backend with MongoDB

## Setup

1. **Install and Start MongoDB**

   Local MongoDB:
   ```bash
   # macOS
   brew tap mongodb/brew
   brew install mongodb-community
   brew services start mongodb-community
   
   # Ubuntu
   sudo apt-get install mongodb
   sudo systemctl start mongodb
   ```

   Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

2. **Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the backend directory:

For local MongoDB:
```
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_NAME=prompt_selector
```

For MongoDB Atlas (Cloud):
```
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_NAME=prompt_selector
```

5. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create a superuser (optional):**
```bash
python manage.py createsuperuser
```

7. **Run the development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

- `POST /api/prompts/generate/` - Generate two responses for a prompt
- `POST /api/prompts/{id}/record_preference/` - Record user preference
- `GET /api/prompts/export_training_data/` - Export training data
- `GET /api/prompts/stats/` - Get statistics
- `GET /api/prompts/` - List all prompts
- `GET /api/prompts/{id}/` - Get a specific prompt

## MongoDB Configuration

The app uses Djongo, a Django adapter for MongoDB. This allows you to use Django's ORM with MongoDB.

**Connection Settings** (in settings.py):
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': MONGODB_NAME,
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': MONGODB_URI,
        }
    }
}
```

## Verifying MongoDB Connection

Check if MongoDB is running:
```bash
mongosh  # Should connect to MongoDB shell
```

View your database:
```bash
mongosh
use prompt_selector
show collections
db.api_prompt.find().pretty()
```
