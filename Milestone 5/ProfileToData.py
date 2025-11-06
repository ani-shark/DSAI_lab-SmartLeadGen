import json
import csv
import os

INPUT_JSON_FILE = 'GeneratedProfiles.json'
OUTPUT_CSV_FILE = 'full_profile_data.csv'

ALL_FLATTENED_COLUMNS = [
    'objective',
    'optional_context',
    'name',
    'headline',
    'inferred_mbti',
    'career_history_json',         # The list of career objects, as a JSON string
    'skills_pipe_delimited',       # A '|' separated list of skills
    'recent_activity_pipe_delimited', # A '|' separated list of activities
    'company_updates_pipe_delimited'  # A '|' separated list of updates
]

# Add any column names from the list above that you want to exclude.
COLUMNS_TO_EXCLUDE = [
]

def flatten_profile_to_dict(profile):
    
    flat_row = {}
    profile_data = profile.get('profile_data', {})
    
    flat_row['objective'] = profile.get('objective', '')
    flat_row['optional_context'] = profile.get('optional_context', '')
    flat_row['name'] = profile_data.get('name', '')
    flat_row['headline'] = profile_data.get('headline', '')
    flat_row['inferred_mbti'] = profile_data.get('inferred_mbti', '')
    
    skills = profile_data.get('skills', [])
    flat_row['skills_pipe_delimited'] = '|'.join(skills)
    activity = profile_data.get('recent_activity', [])
    flat_row['recent_activity_pipe_delimited'] = '|'.join(activity)
    updates = profile_data.get('company_updates', [])
    flat_row['company_updates_pipe_delimited'] = '|'.join(updates)
    
    history = profile_data.get('career_history', [])
    try:
        flat_row['career_history_json'] = json.dumps(history)
    except Exception:
        flat_row['career_history_json'] = '[]'

    return flat_row

def convert_full_profiles_to_csv():
    
    if not os.path.exists(INPUT_JSON_FILE):
        print(f"Error: Input file '{INPUT_JSON_FILE}' not found.")
        print(f"Please ensure '{INPUT_JSON_FILE}' is in the same directory.")
        return

    final_headers = [col for col in ALL_FLATTENED_COLUMNS if col not in COLUMNS_TO_EXCLUDE]
    print(f"Loading profiles from '{INPUT_JSON_FILE}'...")
    print(f"Writing to '{OUTPUT_CSV_FILE}' with the following columns:\n{final_headers}\n")
    
    try:
        with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f_in:
            profiles = json.load(f_in)
        
        with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=final_headers)
            writer.writeheader()
            count = 0
            
            for profile in profiles:
                flat_row = flatten_profile_to_dict(profile)
                writer.writerow(flat_row)
                count += 1
                
        print(f"\nSuccessfully converted and flattened {count} profiles.")
        print(f"Full profile data saved to '{OUTPUT_CSV_FILE}'.")

    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{INPUT_JSON_FILE}'.")
        print("Please ensure the file is a valid JSON array.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    convert_full_profiles_to_csv()