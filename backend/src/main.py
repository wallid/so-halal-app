from src.util.logging_config import configure_logging
from fastapi import FastAPI
from src.api.v1.barcode import router as barcode_router
from src.util.config import load_configuration
from uvicorn.config import LOGGING_CONFIG
import logging
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

configure_logging()
logger = logging.getLogger(__name__)
logger = logging.getLogger("uvicorn.access")

app = FastAPI(
    title="Halal Verification API",
    description="API for verifying if products are halal by checking against various databases.",
    version="1.0.0",
    docs_url="/docs", 
    redoc_url="/redoc",
)

origins = os.getenv("ORIGINS", "").split(",")
app_insights_connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")
redis_connection_string = os.getenv("REDIS_CONNECTION_STRING")
configuration_file_path = os.getenv("CONFIGURATION_FILE_PATH")



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from your Expo app's URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


# Register the API routes
app.include_router(barcode_router, prefix="/api/v1/barcode")

load_configuration(configuration_file_path)



logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application has started.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI application is shutting down.")

@app.get("/health")
def health_check():
    logger.info("Health check called")
    return {"status": "healthy"}

@app.get("/")
def home():
    logger.info("Home page called")
    return {}