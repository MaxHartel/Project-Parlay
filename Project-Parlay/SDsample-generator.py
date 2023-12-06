import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Define the number of elements
num_elements = 16

# Define the range of values
value_range = (1, 99)

# List of standard deviations
std_deviations = [10, 25, 30]

# Generate sample data for each standard deviation
for std_dev in std_deviations:
    # Generate random data with specified mean and standard deviation
    mean_value = np.mean(value_range)
    data = np.random.normal(mean_value, std_dev, num_elements)
    
    # Clip values to ensure they fall within the specified range
    data = np.clip(data, value_range[0], value_range[1])
    
    print(f"Standard Deviation: {std_dev}")
    print(data)
    print("\n")
