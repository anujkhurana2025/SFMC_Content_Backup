# Salesforce Marketing Cloud Backup Script

This Python script automates the backup of content assets from Salesforce Marketing Cloud (SFMC) to Google Cloud Storage (GCS). It uses the SFMC APIs to fetch updated or new content blocks since the last run and saves them in a structured format on GCS.

## Features

- Securely authenticates with Salesforce Marketing Cloud using OAuth2.
- Fetches only new or updated content assets since the last backup.
- Saves backups in a date-based subfolder in Google Cloud Storage (e.g., `backup_010623`).
- Fully configurable via a JSON configuration file.
- Can be scheduled for automated daily execution.

---

## Prerequisites

1. **Python**:
   - Ensure Python 3.7 is installed
   - Install dependencies using `pip install -r requirements.txt`.

2. **Google Cloud SDK**:
   - Install the Google Cloud SDK: [Google Cloud SDK Installation Guide](https://cloud.google.com/sdk/docs/install).
   - Authenticate with GCP:
     ```bash
     gcloud auth application-default login
     ```

3. **Salesforce Marketing Cloud Credentials**:
   - Obtain your `client_id`, `client_secret`, `auth_url`, and `content_url` from your SFMC account.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo-name/SFMC_Content_Backup.git
   cd SFMC_Content_Backup
