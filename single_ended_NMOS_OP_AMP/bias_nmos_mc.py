import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Add import statement for NumPy
import subprocess
import time

command1 = "scp -r vluz@193.136.221.60:/home/vluz/bias_current_NMOS_mc.csv  /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"

script_dir = os.path.dirname(__file__)

subprocess.run(command1, shell=True)
script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "bias_current_NMOS_mc.csv")
dataframe = pd.read_csv(file)
os.remove(file)

nominal_values = dataframe.loc[3::4, "Nominal"].values
std_deviation = np.std(nominal_values)
average_value = np.mean(nominal_values)
# Plot a graph with markers and improved line style
plt.plot(nominal_values, linestyle='-', color='b', label="Nominal Values")
plt.axhline(average_value, color='r', linestyle='--', label="Average Value")
plt.xlabel("RUNS", fontsize=12, weight='bold')  # x-axis label with units
plt.ylabel("IOUT (A)", fontsize=12, weight='bold')  # y-axis label with units

plt.title('Nominal IBIAS runs')
plt.legend()
plt.grid(True)  # Add grid lines for better readability
plt.tight_layout()  # Adjust layout for better spacing
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.savefig(os.path.join(script_dir, 'Nominal_IBIAS_runs.jpg'), format='jpg')
plt.show()

print("Standard Deviation:", std_deviation)
print("Average Value:", average_value)





# Create histogram plot
plt.hist(nominal_values, bins=10, color='blue', edgecolor='black', density=True, label="Histogram")
# Add x-axis label with units
plt.xlabel("IOUT (A)", fontsize=12, weight='bold')
# Add y-axis label with units
plt.ylabel("Number of Runs", fontsize=12, weight='bold')
# Add title
plt.title('Histogram of Nominal Values')
# Add grid
plt.grid(True)
# Adjust layout for better spacing
plt.tight_layout()
# Set spine linewidth
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)
# Show plot
plt.show()