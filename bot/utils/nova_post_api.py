import requests

api_key = '19608388e2583ed03a660f65179eb1c3'
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
					"Phone": "380931207723"
				}
			]
		}
	}

	response = requests.get(url, json=data)
	return response.json()['data'][0]['Status']
