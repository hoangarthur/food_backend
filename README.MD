
## TasteTeam Project Backend

This project is the backend for the TasteTeam application, designed to manage food-related data (users, items, receipts, and recipes) and provide online connectivity using FastAPI. It features modular repositories, MySQL integration, and AI-powered logging.


### Project Structure

```
food_backend/
├── config.py                # Database configuration
├── core/
│   ├── database.py          # Database connection utilities
│   └── test_database.py     # Script to test DB connection
├── repositories/
│   ├── __init__.py
│   ├── item_repository.py   # Item data access
│   ├── receipt_repository.py# Receipt data access
│   ├── user_repository.py   # User data access
│   └── recipe_repository.py # Recipe data access (planned)
├── Ai_repository/
│   └── AI_generate_log.py   # AI-powered log module (planned)
├── testserver.py            # Standalone DB connection test
├── main.py                  # FastAPI server entry point (planned)
├── README.MD                # Project documentation
└── ...
```


### Features
- User, item, receipt, and recipe management
- MySQL database integration
- Repository pattern for data access
- Context-managed DB connections
- FastAPI for online RESTful API
- AI-powered logging module


### Setup
1. **Install dependencies:**
	- Python 3.x
	- `mysql-connector-python` (install via `pip install mysql-connector-python`)
	- `fastapi` and `uvicorn` (install via `pip install fastapi uvicorn`)

2. **Configure Database:**
	- Edit `config.py` with your MySQL credentials and database name.

3. **Database Tables:**
	- Ensure MySQL database has the following tables: `users`, `items`, `receipts`, `recipes` (with appropriate columns).
4. **Database structure:**
- **user**: Stores user information (userId, username, email, phone, diet, password).
- **receipts**: Each receipt is linked to a user (one-to-many: one user can have many receipts).
- **item**: Each item is linked to a receipt (one-to-many: one receipt can have many items).
- **recipe**: Each recipe is linked to a user (one-to-many: one user can have many recipes).

- **user (1) — (M) receipts**: One user can have multiple receipts.
- **receipts (1) — (M) item**: One receipt can have multiple items.
- **user (1) — (M) recipe**: One receipt can have multiple recipes.

> **Note:**
> - There are no direct many-to-many relationships in this schema. All relationships are one-to-many.
> - The `ingredients` field in `recipe` is stored as JSON for flexibility.

**user**
- userId (INT, PK)
- username (VARCHAR)
- email (VARCHAR)
- phone (VARCHAR)
- diet (VARCHAR)
- password (VARCHAR)

**receipts**
- receiptId (INT, PK)
- userId (INT)
- date (DATE)
- source (VARCHAR)
- status (VARCHAR)

**item**
- iditem (INT, PK)
- recipeId (INT)
- name (VARCHAR)
- price (TINYINT)
- quantity (TINYINT)
- date (DATETIME)
- store (VARCHAR)
- category (VARCHAR)

**recipe**
- recipeId (INT, PK)
- userId (INT)
- source (VARCHAR)
- title (VARCHAR)
- description (VARCHAR)
- ingredients (JSON)
- instructions (TEXT)
- nutrition (INT)
- totalTime (SMALLINT)
- dateSaved (DATETIME)
- servings (TINYINT)


### Usage
- **Start FastAPI Server:**
	```sh
	uvicorn main:app --reload
	```
- **Test DB Connection:**
	```sh
	python testserver.py
	```
- **Run Repository Methods:**
	- Use the repository classes in `repositories/` to interact with the database in your own scripts or applications.
	- Example (from project root):
		```sh
		python -m repositories.receipt_repository
		```


### Notes
- Always run scripts from the project root to ensure imports work correctly.
- Relative imports (e.g., `from .item_repository import ...`) require running as a module.
- FastAPI endpoints are defined in `main.py`.
- AI log generation is handled in `Ai_repository/AI_generate_log.py`.


### License
This project is for TasteTeam backend development.
