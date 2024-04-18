import csv
import matplotlib.pyplot as plt

# Path to the CSV file
csv_file_path = "modified_econ_paper_data.csv"


def filter_jobs_by_rp(csv_file_path, rp_threshold=0.75):  # Represents an 'Rp' value of 0.75
    """Filters jobs by a given RP threshold and returns the filtered jobs."""
    filtered_jobs = []
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            rp_value = float(row['Rp'].strip('%'))  # Ensure to strip '%' if it exists
            if rp_value >= rp_threshold:
                filtered_jobs.append(row)
    return filtered_jobs


def get_top_10_highest_rp_jobs(filtered_jobs):
    """Returns the top 10 jobs with the highest RP from the filtered jobs."""
    return sorted(filtered_jobs, key=lambda x: float(x['Rp'].strip('%')), reverse=True)[:10]

def calculate_financial_impact(filtered_jobs):
    """Calculates and prints the financial impact and the total number of jobs at risk."""
    total_gdp_per_job = 0
    total_jobs_at_risk = 0
    for job in filtered_jobs:
        employment_count = int(job['Number of Jobs in 2022'].replace(',', ''))
        pay_data = job['Pay'].replace(',', '')
        try:
            pay = float(pay_data)
            total_gdp_per_job += employment_count * pay
        except ValueError:
            if pay_data == '':
                print(f"Warning: Missing pay data for job {job['Job Title']}")
            else:
                print(f"Warning: Invalid pay data '{pay_data}' for job {job['Job Title']}")
        total_jobs_at_risk += employment_count
    print(f"Total financial impact for jobs with Rp >= 0.75: ${total_gdp_per_job:.2f}")
    print(f"Total number of jobs at risk for Rp >= 0.75: {total_jobs_at_risk}")

def create_scatter_plot(filtered_jobs):
    """Creates and displays a scatter plot of the filtered jobs."""
    rp_values = [float(job['Rp'].strip('%')) for job in filtered_jobs]
    job_counts = [int(job['Number of Jobs in 2022'].replace(',', '')) for job in filtered_jobs]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(job_counts, rp_values, color='blue', alpha=0.5)
    plt.title('Scatter Plot of Jobs in 2022 vs. Rp')
    plt.xlabel('Number of Jobs in 2022 (log scale)')
    plt.ylabel('Rp')
    plt.xscale('log')

    # Define custom tick locations and labels
    tick_locations = [100, 1000, 10000, 100000, 1000000]
    tick_labels = ['100', '1k', '10k', '100k', '1m']
    plt.xticks(tick_locations, tick_labels)

    plt.grid(True)
    plt.show()

def count_total_jobs(csv_file_path):
    """Counts total jobs in the dataset."""
    total_jobs = 0
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row['Number of Jobs in 2022']:
                total_jobs += int(row['Number of Jobs in 2022'].replace(',', ''))
    return total_jobs

if __name__ == '__main__':
    total_jobs = count_total_jobs(csv_file_path)
    filtered_jobs = filter_jobs_by_rp(csv_file_path)
    jobs_with_high_rp = len(filtered_jobs)

    print(f"Number of jobs with Rp >= 0.75: {jobs_with_high_rp}")
    print(f"Total number of jobs: {total_jobs}")
    print(f"Proportion of high Rp jobs: {jobs_with_high_rp / total_jobs:.2%}")

    calculate_financial_impact(filtered_jobs)
    top_10_highest_rp_jobs = get_top_10_highest_rp_jobs(filtered_jobs)
    print("Top 10 Highest Rp Jobs:")
    for index, job in enumerate(top_10_highest_rp_jobs, start=1):
        print(f"{index}. Job Title: {job['Job Title']}, Rp: {job['Rp']}")

    # Create and display the scatter plot
    create_scatter_plot(filtered_jobs)
