import os
import pandas as pd
import numpy as np


def moving_average(data, window_size):
    """Perform moving average smoothing."""
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')


def smooth_data(input_csv_path, window_size=10):
    """
    Smooth the [H2O2] data in a longform CSV file using moving average.

    Parameters:
    - input_csv_path (str): Path to the input CSV file.
    - window_size (int): Window size for moving average. Default is 10.

    Returns:
    - None. The smoothed data is saved as a new CSV file.
    """
    # Read the input data
    data = pd.read_csv(input_csv_path)

    # Group the data by 'Filename' and apply smoothing per group
    grouped = data.groupby('Filename')

    # Initialize an empty DataFrame to store the smoothed data
    smoothed_data_df = pd.DataFrame()

    for name, group in grouped:
        time_data = group['Time (s)'].values
        h2o2_data = group['[H2O2]'].values

        # Apply moving average smoothing
        moving_avg_h2o2 = moving_average(h2o2_data, window_size)

        # Create a DataFrame for the smoothed data
        smoothed_group_df = pd.DataFrame({
            'Time (s)': time_data[window_size - 1:],  # Match the length after moving average
            'Filename': [name] * (len(time_data) - window_size + 1),
            'Original [H2O2]': h2o2_data[window_size - 1:],
            'Smoothed [H2O2]': moving_avg_h2o2
        })

        # Append the smoothed group data to the main DataFrame
        smoothed_data_df = pd.concat([smoothed_data_df, smoothed_group_df], ignore_index=True)

    # Save the smoothed data to a new CSV file
    output_csv_path = os.path.splitext(input_csv_path)[0] + '_smoothed.csv'
    smoothed_data_df.to_csv(output_csv_path, index=False)

# Example usage:
# input_csv_path = 'your_input_file.csv'
# smooth_data(input_csv_path)
