import requests

url = 'http://127.0.0.1:8686/get_blogs/'

params = {'task_id': "1"}  # To get last 7 days from today's date
params = {'task_id': "2-2023/09/01-2023/09/14"}  # To get data from specific starting date to end date
params = {'task_id': "3"}  # to get the data from last week

# Make a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print("API Response:")
    print(data)
else:
    print(f"Error: {response.status_code}")
