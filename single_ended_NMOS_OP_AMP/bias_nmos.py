import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Add import statement for NumPy
# Assuming this code is in a script file, get the directory of the script
script_dir = os.path.dirname(__file__)
file = os.path.join(script_dir, "bias_NMOS.csv")

dataframe = pd.read_csv(file, skiprows=1)
dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
dataframe.dropna(inplace=True)

# Extract the first column as x and the rest of the columns as y
x = dataframe.iloc[:, 0]
y = dataframe.iloc[:, 1:]

# Plotting only numeric columns
plt.figure(figsize=(10, 6))
for col in y.columns:
    if pd.api.types.is_numeric_dtype(y[col]):  # Check if column contains numeric data
        plt.plot(x, y[col], label=col, linewidth=1.5)

plt.xlabel("VOUT (V)", fontsize=20, weight='bold')  # x-axis label with units
plt.ylabel("IOUT (A)", fontsize=20, weight='bold')  # y-axis label with units
plt.title('Data Plot')
plt.legend()
plt.grid(True, which='both', linestyle='--')  # Show both major and minor grid lines
plt.minorticks_on()  # Enable minor ticks

# Set y-axis tick locations based on the data range
plt.yticks(np.linspace(y.min().min(), y.max().max(), num=10))

for spine in plt.gca().spines.values():
    spine.set_linewidth(2)

plt.show()