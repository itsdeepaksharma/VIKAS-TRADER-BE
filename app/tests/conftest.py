import os

os.environ.setdefault("APP_SECRET_KEY", "test-secret-key-that-is-long-enough-for-tests")
os.environ.setdefault("APP_DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")
os.environ.setdefault("APP_BACKEND_CORS_ORIGINS", '["http://localhost:5173"]')
