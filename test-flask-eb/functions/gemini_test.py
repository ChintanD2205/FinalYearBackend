import matplotlib.pyplot as plt

# Data
months = ['Jan', 'Feb', 'Mar', 'Apr']
performance = [2, 56, 44, 80]

# Plotting the graph
plt.figure(figsize=(8, 5))
plt.plot(months, performance, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)

# Adding labels and title
plt.xlabel('Months')
plt.ylabel('Performance')
plt.title('Performance Over Months')
plt.ylim(0, 100)  # Limit y-axis to 0-100

# Display the plot
plt.grid(True)
plt.tight_layout()
plt.show()
