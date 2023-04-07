import requests

def get_stop_info(stop_id):
    """Retrieve information about a bus stop using Easy Way Stops API's GetStopInfo method.

    Args:
        stop_id (str): The ID of the bus stop to retrieve information for.

    Returns:
        dict: A dictionary containing information about the bus stop, including its ID, name, latitude,
        longitude, and a list of routes that stop there.
    """
    base_url = 'https://api.easyway.com/stops/GetStopInfo'
    payload = {'stop_id': stop_id}
    response = requests.get(base_url, params=payload)

    if response.status_code == 200:
        stop_info = response.json()['stop_info']
        return stop_info
    else:
        print(f'Request failed with status code {response.status_code}')


stop_id = '4711'
stop_info = get_stop_info(stop_id)
print(stop_info)