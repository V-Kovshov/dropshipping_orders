import requests
from bot.config import settings

api_key = settings.post.api
url = 'https://api.novaposhta.ua/v2.0/json/'


def get_status_parcel(parcel_number):
	data = {
		"apiKey": api_key,
		"modelName": "TrackingDocument",
		"calledMethod": "getStatusDocuments",
		"methodProperties": {
			"Documents": [
				{
					"DocumentNumber": f"{parcel_number}",
					"Phone": settings.post.phone
				}
			]
		}
	}

	response = requests.get(url, json=data)
	return response.json()['data'][0]['Status']
