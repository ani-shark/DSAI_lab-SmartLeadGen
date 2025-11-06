import json
import csv
import os

INPUT_JSON_FILE = 'GeneratedProfiles.json'
OUTPUT_CSV_FILE = 'MBTI_test_data.csv'

def convert_json_to_csv():
    
    if not os.path.exists(INPUT_JSON_FILE):
        print(f"Error: Input file '{INPUT_JSON_FILE}' not found.")
        print(f"Please save the JSON data from the previous response into a file named '{INPUT_JSON_FILE}'.")
        return

    print(f"Loading profiles from '{INPUT_JSON_FILE}'...")
    
    try:
        with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        
        with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerow(['recent_activity', 'inferred_mbti'])
            count = 0
            
            for profile in profiles:
                profile_data = profile.get('profile_data', {})
                mbti = profile_data.get('inferred_mbti', '')
                activity_list = profile_data.get('recent_activity', [])
                
                activity = ''
                if activity_list:
                    activity = activity_list[0]
                
                writer.writerow([activity, mbti])
                count += 1
                
        print(f"\nSuccessfully converted {count} profiles.")
        print(f"Test data saved to '{OUTPUT_CSV_FILE}'.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_JSON_FILE}'.")
        print("Please ensure the file contains the valid JSON array provided in the last response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    convert_json_to_csv()