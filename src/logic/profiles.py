import requests

URI_PROFILES = "http://a48085841837c4e16a907ae6d6147724-1134772844.us-east-1.elb.amazonaws.com"

def get_candidates_profiles(data:any):
    skills_endpoint = f"{URI_PROFILES}/api/profiles/candidates"
    skills_response = requests.get(skills_endpoint,  json=data)
    if (skills_response.status_code == 200):
        skills = skills_response.json()
        return skills["data"]