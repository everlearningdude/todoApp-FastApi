import requests

def login(username: str, password: str):
    url = f"http://localhost:8001/apilogin/?username={username}&password={password}"  # Adjust the URL as needed

    # Prepare the data to send in the request body
    data = {
        "username": username,
        "password": password
    }

# try:
    # Make the POST request with data in the request body
    response = requests.post(url, json=data)
    # response.raise_for_status()  # Raise an exception for HTTP errors

    # Print the response message
    print(response.json(), response.status_code)

# except requests.RequestException as e:
#     print(f"Error occurred while making the request: {e}")

# Example usage:
username = "admin"
password = "pass"
login(username, password)
