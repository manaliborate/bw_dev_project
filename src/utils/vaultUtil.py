import requests


vault_url =  "http://127.0.0.1:8200"
role_id =  "b70bb787-62e5-305e-47ef-4c8530647c60"
secret_id =  "2ff7b43a-28d9-9d08-af9d-d396a820c811"
secret_path =  "secret/data/aws"


def authenticate_with_approle():
    auth_url = f"{vault_url}/v1/auth/approle/login"
    auth_data = {
        "role_id": role_id,
        "secret_id": secret_id
    }
    try:
        auth_response = requests.post(auth_url, json=auth_data)
        auth_response.raise_for_status()

        token = auth_response.json()["auth"]["client_token"]
        print("token=======", token)
        return token

    except requests.exceptions.RequestException as e:
        print(f"Authentication error: {e}")
        return None

def get_secret(token):
    headers = {
        "X-Vault-Token": token,
    }

    url = f"{vault_url}/v1/{secret_path}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        secret_data = response.json()["data"]
        return secret_data

    except requests.exceptions.RequestException as e:
        print(f"Error retrieving secret: {e}")
        return None
    
token = authenticate_with_approle()
secret_data = get_secret(token)
print(secret_data)