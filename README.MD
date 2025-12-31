
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
    ```mermaid
erDiagram
    USER ||--o{ RECEIPTS : "creates"
    USER ||--o{ RECIPE : "saves/creates"
    ITEM ||--o{ RECEIPTS : "is purchased in"
    ITEM ||--o{ RECIPE : "is used in"

    USER {
        int userId PK
        varchar(100) username
        varchar(100) email
        varchar(45) phone
        varchar(45) diet
        varchar(100) password
    }

    RECEIPTS {
        int receiptId PK
        int dateId
        date date
        varchar(100) source
        varchar(45) status
    }

    RECIPE {
        int recipeId PK
        varchar(255) source
        varchar(500) title
        varchar(2500) description
        json ingredients
        text instructions
        int nutrition
        int totalTime
        smallint total SMALLINT
        datetime dateSaved
        tinyint servings
    }

    ITEM {
        int iditem PK
        varchar(100) name
        tinyint price
        tinyint quantity
        datetime date
        varchar(500) store
        varchar(100) category
    }

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
