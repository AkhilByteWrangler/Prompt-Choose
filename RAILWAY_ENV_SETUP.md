# Railway Deployment Environment Variables

Add the following environment variables in your Railway project settings:

## Required Variables

1. **MONGODB_URI** (Already added ✓)
   ```
   mongodb+srv://your-username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```

2. **MONGODB_NAME** (Already added ✓)
   ```
   prompt_selector
   ```

3. **OPENAI_API_KEY** (Already added ✓)
   ```
   sk-proj-...
   ```

## Additional Recommended Variables

4. **SECRET_KEY** (⚠️ Required for Django security)
   ```
   Generate a secure random string (50+ characters)
   Example: Use this Python command to generate:
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **DEBUG** (Optional, defaults to False)
   ```
   False
   ```

6. **ALLOWED_HOSTS** (Optional, recommended)
   ```
   prompt-choose-production.up.railway.app,*.railway.app
   ```

## Verification

After adding environment variables:
1. Redeploy your Railway service
2. Visit: `https://your-app.railway.app/health/` to verify all variables are loaded
3. Check Railway logs for the "Environment Variables Check" output

## Notes
- Railway automatically sets the `PORT` variable
- Do NOT commit `.env` files to git (already in .gitignore)
- Environment variables are injected at container runtime
