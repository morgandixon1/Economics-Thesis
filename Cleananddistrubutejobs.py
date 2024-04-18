import pandas as pd

def distribute_counts(file_path, output_path):
    # Load the dataset
    data = pd.read_csv(file_path)

    # Convert "Number of Jobs in 2022" and "Employment Change 2022-32" to numeric values
    data['Number of Jobs in 2022'] = data['Number of Jobs in 2022'].str.replace(',', '').astype(float)
    data['Employment Change 2022-32'] = data['Employment Change 2022-32'].str.replace(',', '').astype(float)

    # Group by 'Link' and distribute the counts
    for link, group in data.groupby('Link'):
        job_count = group['Number of Jobs in 2022'].iloc[0] / len(group)
        employment_change = group['Employment Change 2022-32'].iloc[0] / len(group)
        data.loc[data['Link'] == link, 'Number of Jobs in 2022'] = job_count
        data.loc[data['Link'] == link, 'Employment Change 2022-32'] = employment_change

    # Save the modified dataset
    data.to_csv(output_path, index=False)

# Define file paths
csv_file_path = "/econ_paper_data.csv"
output_file_path = "/modified_econ_paper_data.csv"

# Call the function
distribute_counts(csv_file_path, output_file_path)
