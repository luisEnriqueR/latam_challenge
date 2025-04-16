import os

from dotenv import load_dotenv
from google.cloud import secretmanager
from sqlmodel import Session, create_engine

load_dotenv()


def get_secret(project_id, secret_id, version_id="latest"):
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(
            request={"name": name}
        )
        return response.payload.data.decode("UTF-8")
    except Exception:
        return None


GCP_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DB_PASSWORD_SECRET_ID = os.getenv("DB_PASSWORD_SECRET_ID")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = get_secret(GCP_PROJECT_ID, DB_PASSWORD_SECRET_ID)

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@/"
    f"?host={DB_HOST}"
    f"&database={DB_NAME}"
)

if DB_USER and DB_PASSWORD and DB_HOST and DB_NAME:
    engine = create_engine(DATABASE_URL)
else:
    raise Exception("Unable to init database engine")


def get_session():
    with Session(engine) as session:
        yield session
