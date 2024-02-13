import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Add import statement for NumPy
import subprocess
import time







#inputs











command1 = "scp -r vluz@193.136.221.60:/home/vluz/only_PMOS_LOAD_VDC_NMOS.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"
command2 = "scp -r vluz@193.136.221.60:/home/vluz/only_PMOS_LOAD_VDC_NMOS_mc.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"
command3 = "scp -r vluz@193.136.221.60:/home/vluz/only_PMOS_LOAD_current_characteristic.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"

names = ["Nominal","ff_corner","ss_corner"] #the corners simulations

subprocess.run(command1, shell=True)

script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "only_PMOS_LOAD_VDC_NMOS.csv")

dataframe = pd.read_csv(file)
os.remove(file)
dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)



x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, [1, 3, 5]]

interception={}

for idx, value in enumerate(x):
    if value >= 27:
        break
for col in y.columns:
    interception[col] = round(y[col][idx],3)


# Generate a DataFrame from the interception dictionary
interception_df = pd.DataFrame(interception.items(), columns=['Corner', 'VOUT at 27 celsius'])

# Reorder the DataFrame based on the specified order of names
interception_df['Corner'] = pd.Categorical(interception_df['Corner'], categories=names, ordered=True)
interception_df = interception_df.sort_values('Corner')

# Replace the corner values with corresponding names
interception_df['Corner'] = names


plt.figure()
table = plt.table(cellText=interception_df.values,
                  colLabels=interception_df.columns,
                  loc='center')

# Adjust cell alignment to center
for (i, j), cell in table.get_celld().items():
    if (i == 0):
        cell.set_text_props(fontweight='bold', horizontalalignment='center', verticalalignment='center')  # Bold font and center alignment for column labels
        cell.set_fontsize(14)  # Adjust font size for column labels
        cell.set_height(0.1)  # Adjust height for column labels
        cell.set_facecolor('#f7f7f7')  # Light gray background for column labels
        cell.set_edgecolor('black')  # Black edge for column labels
        cell.set_linewidth(1.5)  # Line width for column labels
    else:
        cell.set_fontsize(12)  # Adjust font size for data cells
        cell.set_height(0.1)  # Adjust height for data cells
        cell.set_edgecolor('black')  # Black edge for data cells
        cell.set_linewidth(1.5)  # Line width for data cells
    if (i > 0 and j > 0):
        cell.set_text_props(horizontalalignment='center', verticalalignment='center')  # Center alignment for data cells

# Hide axes
plt.axis('off')
# Save the plot as a JPG image
plt.savefig(os.path.join(script_dir,"only_PMOS_LOAD_VDC_NMOS_table.jpg"), bbox_inches='tight', pad_inches=0.05, format='jpg')
#plt.show()


#plotting dc characteristic
a = 0
# Plotting only numeric columns
plt.figure()
for col in y.columns:
    if pd.api.types.is_numeric_dtype(y[col]):  # Check if column contains numeric data
        plt.plot(x, y[col], label=names[a], linewidth=1.5)
        a = a + 1

plt.xlabel("Temp (C)", fontsize=10, weight='bold')  # x-axis label with units
plt.ylabel("VOUT (V)", fontsize=10, weight='bold')  # y-axis label with units
plt.title('VOUT vs temo')
plt.legend()
plt.grid(True, which='both', linestyle='--')  # Show both major and minor grid lines
plt.minorticks_on()  # Enable minor ticks

# Set y-axis tick locations based on the data range
plt.yticks(np.linspace(y.min().min(), y.max().max(), num=10))  # Adjust num for more ticks

# Set x-axis tick locations based on the data range
plt.xticks(np.linspace(x.min(), x.max(), num=10))  # Adjust num for more ticks

for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.savefig(os.path.join(script_dir, 'only_PMOS_LOAD_VDC_NMOS.jpg'), format='jpg')
#plt.show()


subprocess.run(command2, shell=True)

script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "only_PMOS_LOAD_VDC_NMOS_mc.csv")

dataframe = pd.read_csv(file)
os.remove(file)


nominal_values = dataframe.loc[1::2, "Nominal"].values


std_deviation = np.std(nominal_values)
average_value = np.mean(nominal_values)

# Plot a graph with markers and improved line style
plt.figure()
plt.plot(nominal_values, linestyle='-', color='b', label="Nominal Values")
plt.axhline(average_value, color='r', linestyle='--', label="Average Value")

plt.xlabel("RUNS", fontsize=12, weight='bold')  # x-axis label with units
plt.ylabel("VOUT at 27 C (V)", fontsize=12, weight='bold')  # y-axis label with units
plt.title('VOUT value runs')
plt.legend()

# Add legend with standard deviation
legend_table = plt.table(cellText=[[f"Standard Deviation: {std_deviation}"]],
                         loc='lower center',
                         cellLoc='center',
                         colWidths=[0.5],
                         colLabels=[''])
legend_table.auto_set_font_size(False)
legend_table.set_fontsize(10)
legend_table.scale(1, 1.5)

plt.grid(True)  # Add grid lines for better readability
plt.tight_layout()  # Adjust layout for better spacing
for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

# Save and display the plot
script_dir = os.path.dirname(__file__)
plt.savefig(os.path.join(script_dir, 'VOUT_value_runs.jpg'), format='jpg')
#plt.show()


# Create histogram plot
plt.figure()
plt.hist(nominal_values, bins=10, color='blue', edgecolor='black', density=True, label="Histogram")
# Add x-axis label with units
plt.xlabel("VOUT at 27 C (V)", fontsize=12, weight='bold')
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
plt.savefig(os.path.join(script_dir, 'VOUT_value_runs_histogram.jpg'), format='jpg')
#plt.show()











subprocess.run(command3, shell=True)

script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "only_PMOS_LOAD_current_characteristic.csv")


dataframe = pd.read_csv(file)
os.remove(file)
dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)


x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, [1, 3, 5]]
names = ["Nominal","worst","best"] #the corners simulations




a = 0
# Plotting only numeric columns
plt.figure()
for col in y.columns:
    if pd.api.types.is_numeric_dtype(y[col]):  # Check if column contains numeric data
        plt.plot(x, y[col], label=names[a], linewidth=1.5)
        a = a + 1

plt.xlabel("Vx", fontsize=10, weight='bold')  # x-axis label with units
plt.ylabel("Ibias", fontsize=10, weight='bold')  # y-axis label with units
plt.title('Vout vs Ibias')
plt.legend()
plt.grid(True, which='both', linestyle='--')  # Show both major and minor grid lines
plt.minorticks_on()  # Enable minor ticks

# Set y-axis tick locations based on the data range
plt.yticks(np.linspace(y.min().min(), y.max().max(), num=12))  # Adjust num for more ticks

# Set x-axis tick locations based on the data range
plt.xticks(np.linspace(x.min(), x.max(), num=11))  # Adjust num for more ticks

for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.savefig(os.path.join(script_dir, 'only_PMOS_LOAD_current_characteristic.jpg'), format='jpg')
#plt.show()