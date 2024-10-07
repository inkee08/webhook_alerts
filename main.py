import requests, json
from decouple import config
from datetime import datetime

NOTION_KEY = config('NOTION_KEY')
NOTION_DATABASE_ID = config('NOTION_DATABASE_ID')


headers = {
    "Authorization": "Bearer " + NOTION_KEY,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):

    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]

    return results

def send_msg(alerts):
    print(alerts)

if __name__ == "__main__":
    pages = get_pages()
    now = datetime.now().strftime('%Y-%m-%d')
    alerts = []

    for page in pages:
        try:
            prop = page['properties']
            bean = prop['Name']['title'][0]['plain_text']
            roaster = prop['Roaster']['rich_text'][0]['plain_text']
            status = prop['Status']['status']['name']
            rest_date = prop['Rested date']['formula']['date']['start'] # 2024-09-24
        except:
            continue

        if status == 'Resting' and rest_date <= now:
            alerts.append(f'{roaster} {bean}')
        
    if alerts:
        send_msg(alerts)