import requests


class Core:
    def get_status_code(self, url):
        response = requests.get(url)
        return response.status_code
