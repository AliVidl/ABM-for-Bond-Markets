
" Writen by A Vidler 8 august 2024
" Use code to understand metabolism in 3rd space "


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the range of sugar and spice metabolism values
sugar_metabolism = np.linspace(1, 5.0, 10)
spice_metabolism = np.linspace(1, 5.0, 10)
sugar_metabolism, spice_metabolism = np.meshgrid(sugar_metabolism, spice_metabolism)

# Model the accumulation based on some data or function
accumulation = 50   #np.random.rand(50,50)  # Example: Random accumulation values

# Calculate the welfare values based on the formula
welfare = accumulation**(sugar_metabolism / (sugar_metabolism + spice_metabolism))

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(sugar_metabolism, spice_metabolism, welfare, cmap='viridis')

# Set labels and title
ax.set_xlabel('Bond Metabolism')
ax.set_ylabel('Spice Metabolism')
ax.set_zlabel('Welfare')
plt.title('Welfare(bonds) for Bond and Cash Metabolism (accum = 50)')
plt.show()
