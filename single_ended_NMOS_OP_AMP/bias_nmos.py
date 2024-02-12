import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Add import statement for NumPy
import subprocess
import time






#inputs
names = ["Nominal","Worst corner","Best corner"] #the corners simulations
current_vall = 10 #desired current value in uA
current_val = 9.8 #current val -0.1
Maximum_working_freq = 1000000








# Assuming this code is in a script file, get the directory of the script
command1 = "scp -r vluz@193.136.221.60:/home/vluz/bias_current_NMOS.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"
command2 = "scp -r vluz@193.136.221.60:/home/vluz/bias_output_impedance_NMOS.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"
command3 = "scp -r vluz@193.136.221.60:/home/vluz/bias_current_ac_NMOS.csv /home/vasco/Desktop/circuit_design_plot_scripts/single_ended_NMOS_OP_AMP"
#code
current_val = current_val/1000000
subprocess.run(command1, shell=True)
script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "bias_current_NMOS.csv")
dataframe = pd.read_csv(file, skiprows=1)
os.remove(file)
dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)
# Extract the first column as x and the rest of the columns as y
x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, [1, 3, 5]]
print(y)
interception = {}
for col in y.columns:
    for idx, value in enumerate(y[col]):
        if value >= current_val:
            interception[col] = round(x[idx],2)
            break  # Exit the loop once the interception point is found

# Generate a DataFrame from the interception dictionary
interception_df = pd.DataFrame(interception.items(), columns=['Corner', 'Minimum VOUT'])

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
plt.savefig(os.path.join(script_dir,"interception_table.jpg"), bbox_inches='tight', pad_inches=0.05, format='jpg')
#plt.show()

#plotting dc characteristic
a = 0
# Plotting only numeric columns
plt.figure()
for col in y.columns:
    if pd.api.types.is_numeric_dtype(y[col]):  # Check if column contains numeric data
        plt.plot(x, y[col], label=names[a], linewidth=1.5)
        a = a + 1

plt.xlabel("VOUT (V)", fontsize=12, weight='bold')  # x-axis label with units
plt.ylabel("IOUT (A)", fontsize=12, weight='bold')  # y-axis label with units
plt.title('IOUT vs VOUT')
plt.legend()
plt.grid(True, which='both', linestyle='--')  # Show both major and minor grid lines
plt.minorticks_on()  # Enable minor ticks

# Set y-axis tick locations based on the data range
plt.yticks(np.linspace(y.min().min(), y.max().max(), num=10))  # Adjust num for more ticks

# Set x-axis tick locations based on the data range
plt.xticks(np.linspace(x.min(), x.max(), num=10))  # Adjust num for more ticks

for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.savefig(os.path.join(script_dir, 'IOUT_vs_VOUT.jpg'), format='jpg')
#plt.show()


#plotting the output impedance
subprocess.run(command2, shell=True)

file = os.path.join(script_dir, "bias_output_impedance_NMOS.csv")
dataframe = pd.read_csv(file, skiprows=1)
os.remove(file)
dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)
# Extract the first column as x and the rest of the columns as y
x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, [1, 3, 5]]
a = 0
plt.figure()
for col in y.columns:
    if pd.api.types.is_numeric_dtype(y[col]):  # Check if column contains numeric data
        plt.plot(x, y[col], label=names[a], linewidth=1.5)
        a = a + 1

plt.xlabel("VOUT (V)", fontsize=12, weight='bold')  # x-axis label with units
plt.ylabel("output impedance", fontsize=12, weight='bold')  # y-axis label with units
plt.title('output impedance vs VOUT')
plt.legend()
plt.grid(True, which='both', linestyle='--')  # Show both major and minor grid lines
plt.minorticks_on()  # Enable minor ticks

# Set y-axis tick locations based on the data range
plt.yticks(np.linspace(y.min().min(), y.max().max(), num=10))  # Adjust num for more ticks

# Set x-axis tick locations based on the data range
plt.xticks(np.linspace(x.min(), x.max(), num=10))  # Adjust num for more ticks

for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.savefig(os.path.join(script_dir, 'output_impedance_vs_VOUT.jpg'), format='jpg')
#plt.show()
subprocess.run(command3, shell=True)
file = os.path.join(script_dir, "bias_current_ac_NMOS.csv")
dataframe = pd.read_csv(file, skiprows=1)
os.remove(file)

dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)
# Extract the first column as x and the rest of the columns as y
x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, [1, 4, 7]]
interception = {}



for idx, value in enumerate(x):
    if value >= Maximum_working_freq:
        break



for col in y.columns:
    interception[col] = y[col][idx]


# Generate a DataFrame from the interception dictionary
interception_df = pd.DataFrame(interception.items(), columns=['Corner', 'Maximum IOUT variation'])

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
plt.savefig(os.path.join(script_dir,"ac_bias_table.jpg"), bbox_inches='tight', pad_inches=0.05, format='jpg')
#plt.show()



