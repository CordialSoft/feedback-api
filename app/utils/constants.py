import os

import dotenv

dotenv.load_dotenv()

DATABASE_URL = "postgresql://qoomjtow:BCKRSeu2mAAWQKGkNX-klhn99DYgFd0H@kala.db.elephantsql.com/qoomjtow"
SECRET_KEY = "os.getenv(SECRET_KEY)"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
