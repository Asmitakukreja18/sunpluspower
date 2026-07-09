import os
import sys
from alembic.config import Config
from alembic import command

# Add backend dir to system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Temporarily set database URL to sqlite for generation
os.environ["DATABASE_URL"] = "sqlite:///./temp.db"

def main():
    print("Configuring Alembic...")
    alembic_cfg = Config("alembic.ini")
    
    print("Running Alembic revision --autogenerate...")
    command.revision(alembic_cfg, message="Initial migrations", autogenerate=True)
    print("Migrations generated successfully.")
    
    # Cleanup local sqlite db
    if os.path.exists("temp.db"):
        os.remove("temp.db")
        print("Cleaned up temp.db")

if __name__ == "__main__":
    main()
