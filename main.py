import argparse
import sys
import requests
from bs4 import BeautifulSoup

# 1. Setup Argument Parser
parser = argparse.ArgumentParser(description="Bundy.PH CLI Clock-in/out Tool")

# Required positional argument
parser.add_argument("action", choices=["timein", "timeout"], help="Action to perform")

# Optional positional arguments (default values provided if omitted)
parser.add_argument("--code", default="Paramount", help="Account Code")
parser.add_argument("--user", default="000003277", help="Username")
parser.add_argument("--passw", default="19940709", help="Password")
parser.add_argument("lat", nargs="?", default="14.78116", help="Latitude")
parser.add_argument("long", nargs="?", default="121.047987", help="Longitude")
parser.add_argument("location", nargs="?", default="Barangay 176-D, Zone 15, Bagong Silang, District 1, Caloocan, Northern Manila District, Metro Manila, 1428, Philippines", help="Full address string")

args = parser.parse_args()

# 2. Map Action to API Type
# Based on your logs: 1 = In, 2 = Out
if args.action == "timein":
    type_id = "1"
elif args.action == "timeout":
    type_id = "2"
else:
    # This part is a safety net: if it's not one of the two, exit immediately
    print(f"Error: Invalid action '{args.action}'. Use 'timein' or 'timeout'.")
    sys.exit(1)
    
LOGIN_PAGE_URL = "https://bundy.ph/login/Paramount"
AUTH_URL = "https://bundy.ph/login/authenticate"

ACCOUNT_CODE = args.code
USERNAME = args.user
PASSWORD = args.passw

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": LOGIN_PAGE_URL,
    "Origin": "https://bundy.ph",
}

# 1. Get login page first
response = session.get(LOGIN_PAGE_URL, headers=headers)
response.raise_for_status()

# 2. Extract CSRF token
soup = BeautifulSoup(response.text, "html.parser")

csrf_meta = soup.find("meta", attrs={"name": "csrf-token"})

if csrf_meta:
    authenticity_token = csrf_meta.get("content")
else:
    token_input = soup.find("input", attrs={"name": "authenticity_token"})
    authenticity_token = token_input.get("value") if token_input else None

if not authenticity_token:
    raise Exception("Could not find authenticity_token from login page.")

print("CSRF token:", authenticity_token)

# 3. Send login POST
payload = {
    "utf8": "✓",
    "authenticity_token": authenticity_token,
    "account_code": ACCOUNT_CODE,
    "username": USERNAME,
    "password": PASSWORD,
}

login_response = session.post(
    AUTH_URL,
    data=payload,
    headers=headers,
    allow_redirects=False
)

print("Status:", login_response.status_code)
print("Location:", login_response.headers.get("location"))
print("Cookies:", session.cookies.get_dict())

cookies = session.cookies.get_dict()

# 4. Check if login redirects to /app
if login_response.status_code == 302 and "/app" in login_response.headers.get("location", ""):
    print("Login successful!")

    app_response = session.get("https://bundy.ph/app", headers=headers)
    print("App page status:", app_response.status_code)
else:
    print("Login may have failed.")
    print(login_response.text[:500])


# The URL for the clock in/out action
url = "https://bundy.ph/employee_clock/time_in_out"

# Headers based on your browser session
# Note: User-Agent and Referer are often required for security validation
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
    "Referer": "https://bundy.ph/app",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://bundy.ph"
}

# The payload data from your request logs
data = {
    "type": type_id,
    "latitude": args.lat,
    "longitude": args.long,
    "location": args.location,
    "browser_name": "Chrome 147.0.0.0",
    "image": "",
    "is_location_spoofing": "false",
    "is_image_spoofing": "false",
    "authenticity_token": authenticity_token
}

try:
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
