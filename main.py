import os
import json
import requests
from datetime import datetime
from google.cloud import storage

# Configuration file path
CONFIG_FILE = "config.json"
LAST_RUN_FILE = "last_run_timestamp.txt"  # Stores the last run timestamp

# Load configuration from JSON file
def load_config():
    with open(CONFIG_FILE, "r") as config_file:
        return json.load(config_file)

# Authenticate with Salesforce Marketing Cloud
def authenticate_sfmc(client_id, client_secret, auth_url):
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(auth_url, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]

# Fetch updated content assets from Salesforce Marketing Cloud
def fetch_content_assets(access_token, content_url, last_run):
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"$filter": f"modifiedDate ge {last_run}"}
    response = requests.get(content_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["items"]

# Backup content assets to Google Cloud Storage
def backup_to_gcs(content_assets, bucket_name, backup_prefix):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    backup_folder = f"{backup_prefix}{datetime.now().strftime('%d%m%y')}/"
    
    for asset in content_assets:
        file_path = f"{backup_folder}{asset['id']}.json"
        blob = bucket.blob(file_path)
        blob.upload_from_string(json.dumps(asset, indent=2))
        print(f"Uploaded: {file_path}")

# Check if the script has already run today
def has_run_today():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            last_run = datetime.fromisoformat(f.read().strip())
            # Compare dates (ignore time)
            if last_run.date() == datetime.utcnow().date():
                return True
    return False

# Update the last run timestamp
def update_last_run_timestamp():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(datetime.utcnow().isoformat())

# Main function
def main():
    # Ensure the script runs only once per day
    if has_run_today():
        print("Script has already run today. Exiting.")
        return

    # Load configuration
    config = load_config()

    # Extract settings
    client_id = config["salesforce"]["client_id"]
    client_secret = config["salesforce"]["client_secret"]
    auth_url = config["salesforce"]["auth_url"]
    content_url = config["salesforce"]["content_url"]
    bucket_name = config["google_cloud"]["bucket_name"]
    backup_prefix = config["settings"]["backup_prefix"]

    # Get last run timestamp
    last_run = None
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, "r") as f:
            last_run = f.read().strip()
    else:
        last_run = datetime.utcnow().isoformat()  # Default to now if no last run

    # Authenticate with Salesforce
    access_token = authenticate_sfmc(client_id, client_secret, auth_url)

    # Fetch content assets
    content_assets = fetch_content_assets(access_token, content_url, last_run)

    # Backup to Google Cloud Storage if there are new/updated assets
    if content_assets:
        backup_to_gcs(content_assets, bucket_name, backup_prefix)
    else:
        print("No new or updated content assets found.")

    # Update the last run timestamp
    update_last_run_timestamp()

# Run script
if __name__ == "__main__":
    main()
