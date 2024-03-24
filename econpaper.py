import openai
from openai import OpenAI
import re
import pandas as pd

def query_openai_and_parse_response(job_title):
    openai.api_key = 'yourkey_here'
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Respond with only direct answers to the 7 requests."},
            {"role": "user", "content": f"Analyze the job title \"{job_title}\" for the dataset. Estimate the following:\n"
                                        "1. Digital Work (%)\n"
                                        "2. Routine Work (%)\n"
                                        "3. Cognitive/Innovation Work (%)\n"
                                        "4. Interpersonal Work (%)\n"
                                        "5. Management Work (%)\n"
                                        "6. Education Level Choice: None, Highschool, Associates, Bachelors, Masters, PhD, Doctorate, Professional Certificate \n"
                                        "7. 2 Digit NAICS Code"}
        ],
        temperature=0.15,
        max_tokens=200,
        top_p=0.25,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Correcting the response access method based on the latest OpenAI API client library
    bot_response = response.choices[0].message.content if response.choices else "No response received."

    percentages = re.findall(r"\d+%", bot_response)
    education_levels = ["None", "Highschool", "Associates", "Bachelors", "Masters", "PhD", "Doctorate", "Professional Certificate"]
    response_lines = bot_response.split('\n')
    education_level_line = response_lines[5]  # Get the 6th line (index 5)
    education_level_match = [level for level in education_levels if level.lower() in education_level_line.lower()]
    education_level = education_level_match[0] if education_level_match else "Unknown"
    naics_code_line = response_lines[-1]  # Get the last line
    naics_code_match = re.search(r'\d{2}', naics_code_line)
    naics_code = naics_code_match.group() if naics_code_match else "Unknown"

    return {
        'percentages': percentages if len(percentages) >= 5 else ["Unknown"] * 5,
        'education_level': education_level,
        'naics_code': naics_code
    }

csv_file_path = 'C:/Users/kylan/Downloads/jobs.csv'
df = pd.read_csv(csv_file_path)


count = 0  # Initialize a counter
for index, row in df[df['Digital Work'].isna()].iterrows():
    job_title = row['Job Title']
    result = query_openai_and_parse_response(job_title)

    if 'percentages' in result and len(result['percentages']) >= 5:
        df.at[index, 'Digital Work'] = result['percentages'][0]
        df.at[index, 'Routine Work'] = result['percentages'][1]
        df.at[index, 'Cognitive/ Innovation Work'] = result['percentages'][2]
        df.at[index, 'Interpersonal Work'] = result['percentages'][3]
        df.at[index, 'Management Work'] = result['percentages'][4]
    df.at[index, 'Education Level'] = result['education_level']
    df.at[index, '2 Digit NAICS Industy'] = result['naics_code']

    count += 1
    if count % 10 == 0:  # Check if the counter is a multiple of 10
        df.to_csv(csv_file_path, index=False)
        print(f"Saved progress at row {index}.")

# Save the final DataFrame to ensure any remaining changes are stored
df.to_csv(csv_file_path, index=False)
print("CSV file has been fully updated.")
