import json
import scraping_profiles

def main():
    with open('linkedin_success_master.json', 'r', encoding='utf-8') as f:
        linkedin_data = json.load(f)

    scraped_profiles = scraping_profiles(linkedin_data)

    with open('scraped_profiles.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_profiles, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
