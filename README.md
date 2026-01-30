# Myflaskapp

Modern Flask application structure.

## Quick Start

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. **Run Application**
   ```bash
   flask run
   ```

3. **Run Tests**
   ```bash
   pytest
   ```

## Project Structure

- `app/` - Application code
- `app/core/` - Configuration and extensions
- `app/models/` - Database models
- `app/routes/` - Route blueprints
- `app/services/` - Business logic
- `tests/` - Test files
