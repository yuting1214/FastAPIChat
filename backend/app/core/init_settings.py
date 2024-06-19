import argparse
import os
from backend.app.core.config import get_settings

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Run the FastAPI application.")
parser.add_argument("--mode", choices=["dev", "prod"], default="dev", help="Run mode: 'dev' or 'prod'")
parser.add_argument("--host", default="127.0.0.1", help="Host IP address")
args = parser.parse_args()

# Initialize and update settings
settings = get_settings(args.mode)

# Save updated settings for import in other modules
global_settings = settings
