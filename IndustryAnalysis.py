import csv
import matplotlib.pyplot as plt
import numpy as np

# Path to the CSV file
csv_file_path = "econ_paper_data.csv"

def average_rp_by_naics(csv_file_path):
    naics_rp_sum = {}
    naics_rp_count = {}
    
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            naics_industry = row['2 Digit NAICS Industy']
            rp_value = float(row['Rp'].strip('%'))
            
            # Accumulate Rp values and counts for each NAICS industry
            if naics_industry in naics_rp_sum:
                naics_rp_sum[naics_industry] += rp_value
                naics_rp_count[naics_industry] += 1
            else:
                naics_rp_sum[naics_industry] = rp_value
                naics_rp_count[naics_industry] = 1
    
    # Calculate average Rp for each NAICS industry
    naics_rp_avg = {industry: (naics_rp_sum[industry] / naics_rp_count[industry]) * 100 for industry in naics_rp_sum}
    
    # Sort NAICS industries by average Rp in descending order
    sorted_naics_rp_avg = sorted(naics_rp_avg.items(), key=lambda x: x[1], reverse=True)
    
    # Extract NAICS industries and average Rp for plotting
    naics_industries = [industry for industry, _ in sorted_naics_rp_avg]
    average_rp_percentages = [avg_rp for _, avg_rp in sorted_naics_rp_avg]
    
    # Print average Rp for each NAICS industry
    for industry, avg_rp in zip(naics_industries, average_rp_percentages):
        print(f"{industry}: {avg_rp:.2f}%")
    
    # Generate colors for each bar using a colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(naics_industries)))
    
    # Plot bar graph with different colors for each bar
    plt.figure(figsize=(10, 8))  # Adjust figure size
    bars = plt.barh(naics_industries, average_rp_percentages, color=colors)
    plt.xlabel('Rp %')
    plt.ylabel('2 Digit NAICS Industry')
    plt.title('Average Rp by 2 Digit NAICS Industry')
    plt.gca().invert_yaxis()  # Invert y-axis to have highest Rp at the top

    # Set x-axis to range from 0 to 100
    plt.xlim(0, 100)

    # Add text annotation with average Rp value on each bar, ensuring no overlap
    for bar, rp in zip(bars, average_rp_percentages):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{rp:.2f}%', va='center')

    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Call the function to calculate average Rp by NAICS industry and plot the results
average_rp_by_naics(csv_file_path)
