from app import db
from app.models import Parent, Child, Leave

# Create all tables
db.create_all()

# Optional: Add some initial data
# ... e.g. db.session.add(Parent(...))

db.session.commit()