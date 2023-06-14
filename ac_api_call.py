import requests

def ygo_ac_call():
    response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    data = response.json()['data']

    db_data = []
    for item in data:
        card_data = {}
        for key in item.keys():
            # Convert 'desc' to 'description'
            if key == 'desc':
                card_data['description'] = item[key]
            elif key in ('id', 'name', 'race', 'level', 'def', 'scale', 'linkmarkers', 
                         'archetype', 'atk', 'linkval', 'attribute', 'frameType', 'type'):
                card_data[key] = item[key]
        db_data.append(card_data)

    return db_data