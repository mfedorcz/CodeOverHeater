import requests
import json
import os
import sys

def fetch_and_save_json(api_key, bbox, output_file):
    """
    Fetches JSON data from the HERE Traffic API and saves it to a file.

    :param api_key: Your HERE API key.
    :param bbox: Bounding box in the format 'west,south,east,north'.
    :param output_file: Path to the output JSON file.
    """
    base_url = "https://data.traffic.hereapi.com/v7/flow"
    params = {
        "locationReferencing": "shape",
        "in": f"bbox:{bbox}",
        "apiKey": api_key
    }

    try:
        print(f"Sending request to {base_url} with parameters: {params}")
        response = requests.get(base_url, params=params, timeout=30)  # 30 seconds timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        print("Request successful. Parsing JSON data...")
        data = response.json()  # Parse JSON response

        print(f"Saving JSON data to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"JSON data successfully saved to {output_file}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred during the request: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Error decoding JSON: {json_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

def main():
    # Retrieve API key from environment variable
    api_key = "bb5yVD7eybArHJ0xMl0RtzsAwljoX-BrMCp_pDKOAlM"
    if not api_key:
        print("Error: HERE_API_KEY environment variable not set.")
        sys.exit(1)

    # Define the bounding box (west, south, east, north)
    bbox = "19.7587,49.9889,20.0564,50.0945"

    # Define the output file path
    output_file = "traffic_data.json"

    # Fetch and save the JSON data
    fetch_and_save_json(api_key, bbox, output_file)

if __name__ == "__main__":
    main()
