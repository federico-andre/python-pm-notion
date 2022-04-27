# python-pm-notion
Passwords Manager with Python and Notion API


# Getting started
You can install dependencies with:
> pip install -r requirements.txt

## env file
To work the password manager needs a *.env* file with the following properties:

| **KEY** | **VALUE** |
|---|---|
|INTEGRATION_KEY| Your Notion integration key|
|DATABASE_ID| Your Notion database id|
|NOTION_VERSION| The Notion's API version|
|SECRET_KEY| A Cypher secret key for encrypt and decrypt your passwords|

## Database structure
You Notion database should have the following structure:

| Site | User | Password | Aggiunto |
|---|---|---|---|

# Usage
You can run the script with the command:

`python pass-mngr.py --help`

## newpassword
This function will create a new password and will ask for the site, user and password to be add.

## getpassword
This function will return all your stored passwords. You can pass the site name and retrive only the corrispondent password
