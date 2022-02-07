import requests
import json


class Test:
    def get_teams(self) -> str:
        url = "https://api.pagerduty.com/teams?limit=1000&offset=1&total=false"

        payload = {}
        headers = {
            'Authorization': 'Token token=u+ACyVVGD-_FgpxawvyA',
            'Accept': 'application/vnd.pagerduty+json;version=2',
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.text
        # print(response.text)
