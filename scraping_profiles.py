import json
import time
import requests
from linkdapi import LinkdAPI

def profile_scraping(linkedin_data):
  '''
  Extract profile information from Linkedin using data from recent graduate
  '''
  linkedin_urls = [item.get('LinkedIn URL') for item in linkedin_data if item.get('LinkedIn URL')]
  #linkedin_ids = [url.split('/in/')[-1].split('/')[0] for url in linkedin_urls]
  linkedin_ids = ['isabela=sag','otavioconquista']
  
  # Initialize with API key
  api_key = "li-r9CRYTKjdUbULQsdXtvk39_MmzxlmKzkK7I5zgouC42XMG9ZZcdx1KDhNwVS88iUSiGB4eCqiAt6hDgQpPQvcyD0zUNpbQ"
  headers = {"X-linkdapi-apikey": f"{api_key}"}
  
  all_profiles_data = []
  not_found_profile = []

  for profile_id in linkedin_ids:
    combined_data = {}
  
    # profile overview
    url_ov = f"https://linkdapi.com/api/v1/profile/overview?username={profile_id}"
    overview_response = requests.get(url_ov, headers=headers)
  
    if overview_response.status_code == 200:
        overview_data = overview_response.json()
        if overview_data and overview_data.get('success'):
            combined_data.update(overview_data.get('data', {}))
            urn = overview_data.get('data', {}).get('urn')
  
            if urn:
                # profile skills
                url_skills = f"https://linkdapi.com/api/v1/profile/skills?urn={urn}"
                skills_response = requests.get(url_skills, headers=headers)
                if skills_response.status_code == 200:
                    skills_data = skills_response.json()
                    if skills_data and skills_data.get('success'):
                        combined_data['skills'] = skills_data.get('data', {}).get('skills', [])
  
  
                # profile certifications
                url_cert = f"https://linkdapi.com/api/v1/profile/certifications?urn={urn}"
                certifications_response = requests.get(url_cert, headers=headers)
                if certifications_response.status_code == 200:
                    certifications_data = certifications_response.json()
                    if certifications_data and certifications_data.get('success'):
                        combined_data['certifications'] = certifications_data.get('data', {}).get('certifications', [])
  
  
                # profile education
                url_educ = f"https://linkdapi.com/api/v1/profile/education?urn={urn}"
                education_response = requests.get(url_educ, headers=headers)
                if education_response.status_code == 200:
                    education_data = education_response.json()
                    if education_data and education_data.get('success'):
                        combined_data['education'] = education_data.get('data', {}).get('education', [])
    else:
        not_found_profile.append(profile_id)
        print(f"Error fetching overview for {profile_id}: Status Code {overview_response.status_code}")
  
    all_profiles_data.append(combined_data)
    time.sleep(1) # Add a small delay to avoid hitting the rate limit
  
  # Convert the combined list of dictionaries to a JSON string
  combined_json = json.dumps(all_profiles_data, indent=4)
  return combined_json
