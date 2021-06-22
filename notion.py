import requests
import secrets
import json
from datetime import date

URL = "https://api.notion.com/v1"

HEADERS = {
    "Authorization": secrets.INTEGRATION_KEY,
    "Notion-Version": secrets.NOTION_VERSION,
    "Content-Type": "application/json"
}

def getPasswords(sito = None):
    query = {
        "sorts": [
            {
            "timestamp": "created_time",
            "direction": "ascending"
            }
        ]
    }

    if sito is not None:
        query["filter"] = {
            "property": "Site",
            "title": {
                "equals": sito
            }
        }

    query = json.dumps(query)

    resp = requests.post(url = f"{URL}/databases/{secrets.DATABASE_ID}/query", headers = HEADERS, data = query)
    data = resp.json()

    return data["results"]

def aggiungiPagina(sito, user, password):

    passForSite = getPasswords(sito)

    if passForSite:
        return f"Esistono già credenziali per il sito: {sito}"

    to_add = {
        "parent": { "database_id": secrets.DATABASE_ID },
        "properties": {
            "Site": {
                "title": [
                    {
                        "text": {
                            "content": sito
                        }
                    }
                ]
            },
            "User": {
                "rich_text": [
                    {
                        "text": {
                            "content": user
                        }
                    }
                ]
            },
            "Password": {
                "rich_text": [
                    {
                        "text": {
                            "content": password.decode()
                        }
                    }
                ]
            },
            "Aggiunto": {
                "date": {
                    "start": date.today().isoformat()
                }
            }
        },
        "children": []
    }

    to_add = json.dumps(to_add)

    # print(to_add)
    try:
        response = requests.post(url = f"{URL}/pages", headers = HEADERS, data = to_add)
        response = response.json()
        # print(response)

        if response["object"] == "error":
            raise Exception(response['status'], response['code'], response['message'])
        else:
            return f"Credenziali correttamente salvate per il sito: {sito}"
        
    except Exception as e:
        return f"Errore durante il salvataggio delle credenziali su notion! {e.args}"

if __name__ == '__main__':
    aggiungiPagina("prova", "prova", "prova")
    getPasswords()