from app.models import Base
from app.database import engine


# One-time DB table creation (for dev/testing)
Base.metadata.create_all(bind=engine)
