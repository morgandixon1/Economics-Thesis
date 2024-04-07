import csv
import matplotlib.pyplot as plt

# Path to the CSV file
csv_file_path = "/Users/morgandixon/Desktop/econdata/econ_paper_data.csv"

def filter_jobs_by_rp(csv_file_path, rp_threshold=0.75):
    filtered_jobs = []
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rp_value = float(row['Rp'].strip('%'))
            if rp_value > rp_threshold:
                filtered_jobs.append(row)
    return filtered_jobs

def count_jobs_with_max_employment(filtered_jobs):
    max_employment_count = sum(1 for job in filtered_jobs if int(job['Number of Jobs in 2022'].replace(',', '')) == 7099400)
    total_employed_above_75 = sum(int(job['Number of Jobs in 2022'].replace(',', '')) for job in filtered_jobs)
    return max_employment_count, total_employed_above_75

def get_top_10_highest_rp_jobs(filtered_jobs):
    top_10_highest_rp_jobs = sorted(filtered_jobs, key=lambda x: float(x['Rp'].strip('%')), reverse=True)[:10]
    return top_10_highest_rp_jobs

def create_scatter_plot(csv_file_path):
    rp_values = []
    job_counts = []
    
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            rp_value = float(row['Rp'].strip('%'))
            job_count = int(row['Number of Jobs in 2022'].replace(',', ''))
            
            rp_values.append(rp_value)
            job_counts.append(job_count)
    
    # Plot scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(job_counts, rp_values, color='blue', alpha=0.5)
    plt.title('Scatter Plot of Jobs in 2022 vs. Rp')
    plt.xlabel('Number of Jobs in 2022 (log scale)')
    plt.ylabel('Rp')
    plt.xscale('log')

    # Define custom tick locations and labels
    tick_locations = [1000, 10000, 100000, 1000000, 10000000]
    tick_labels = ['1k', '10k', '100k', '1m', '10m']

    plt.xticks(tick_locations, tick_labels)
    plt.grid(True)
    plt.show()

def sum_employed_above_rp_threshold(csv_file_path, rp_threshold=0.75):
    total_employed_above_threshold = 0
    
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            rp_value = float(row['Rp'].strip('%'))
            if rp_value > rp_threshold:
                employment_count = int(row['Number of Jobs in 2022'].replace(',', ''))
                total_employed_above_threshold += employment_count
    
    print(f"Total employed people in jobs with Rp > {rp_threshold}: {total_employed_above_threshold}")
    
    total_divided_by_19_517 = total_employed_above_threshold / 19.517
    print(f"Total employed people divided by 19.517: {total_divided_by_19_517}")

def calculate_gdp_per_job(csv_file_path, rp_threshold=0.75):
    total_gdp_per_job = 0
    
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            rp_value = float(row['Rp'].strip('%'))
            if rp_value > rp_threshold:
                employment_count = int(row['Number of Jobs in 2022'].replace(',', ''))
                pay = float(row['Pay'].replace(',', ''))
                gdp_per_job = (employment_count / 19.517) * pay
                total_gdp_per_job += gdp_per_job
    
    print(f"Total GDP per job for jobs with Rp > {rp_threshold}: ${total_gdp_per_job:.2f}")

# Call the function to calculate GDP per job for jobs with Rp > 0.75 and sum them up
calculate_gdp_per_job(csv_file_path)

sum_employed_above_rp_threshold(csv_file_path)

# Call the function to create scatter plot
create_scatter_plot(csv_file_path)
# Filter jobs by Rp
filtered_jobs = filter_jobs_by_rp(csv_file_path)

# Count jobs with max employment and total employed above 75%
max_employment_count, total_employed_above_75 = count_jobs_with_max_employment(filtered_jobs)

# Get top 10 highest Rp jobs
top_10_highest_rp_jobs = get_top_10_highest_rp_jobs(filtered_jobs)

# Print results
print(f"Number of jobs with 7,099,400 employed people: {max_employment_count}")
print(f"Total employed people in jobs with Rp > 75%: {total_employed_above_75}")

print("Top 10 Highest Rp Jobs:")
for index, job in enumerate(top_10_highest_rp_jobs, start=1):
    print(f"{index}. Job Title: {job['Job Title']}, Rp: {job['Rp']}")
