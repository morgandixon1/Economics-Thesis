import csv
import matplotlib.pyplot as plt
import numpy as np

# Path to the CSV file
csv_file_path = "econ_paper_data.csv"

def average_rp_by_education(csv_file_path):
    education_rp_sum = {}
    education_rp_count = {}
    
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            education_level = row['Education']
            rp_value = float(row['Rp'].strip('%'))
            
            # Accumulate Rp values and counts for each education level
            if education_level in education_rp_sum:
                education_rp_sum[education_level] += rp_value
                education_rp_count[education_level] += 1
            else:
                education_rp_sum[education_level] = rp_value
                education_rp_count[education_level] = 1
    
    # Calculate average Rp for each education level
    education_rp_avg = {level: (education_rp_sum[level] / education_rp_count[level]) * 100 for level in education_rp_sum}
    
    # Sort education levels by average Rp in descending order
    sorted_education_rp_avg = sorted(education_rp_avg.items(), key=lambda x: x[1], reverse=True)
    
    education_levels = [level if level != 'See How to Become One' else 'Professional Certificate' for level, _ in sorted_education_rp_avg]
    average_rp_percentages = [avg_rp for _, avg_rp in sorted_education_rp_avg]

    # Print average Rp for each education level
    for level, avg_rp in zip(education_levels, average_rp_percentages):
        print(f"{level}: {avg_rp:.2f}%")
    
    # Generate colors for each bar using a colormap
    colors = plt.cm.viridis(np.linspace(0, 1, len(education_levels)))
    plt.figure(figsize=(8, 6))  # Adjust figure size
    bars = plt.barh(education_levels, average_rp_percentages, color=colors)
    plt.xlabel('Rp %')
    plt.ylabel('Education Level')
    plt.title('Average Rp by Education Level')
    plt.gca().invert_yaxis()  # Invert y-axis to have highest Rp at the top

    # Set x-axis to range from 0 to 100
    plt.xlim(0, 100)

    # Add text annotation with average Rp value on each bar, ensuring no overlap
    for bar, rp in zip(bars, average_rp_percentages):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{rp:.2f}%', va='center')

    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Call the function to calculate average Rp by education level and plot the results
average_rp_by_education(csv_file_path)
