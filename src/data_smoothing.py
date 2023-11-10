import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from print_statments import print_smoothing_help
from data_calculations import gaussian_smoothing, lowess_smoothing, exponential_smoothing, savitzky_golay_smoothing, moving_average_smoothing



def smoothing_handler(file_name,path):
    df = pd.read_csv(file_name)

    # It might be a good idea to drop the 'Unnamed: 0' column if it's just an index
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Group the DataFrame by 'Filename' and create a dictionary of DataFrames
    data_by_file = {file: group.reset_index(drop=True) for file, group in df.groupby('Filename')}
    smoothing_menu(data_by_file,path)





def smoothing_menu(data_by_file,path):


    while True:
        print("\nSmoothing Methods:")
        print("1) Moving Average")
        print("2) Exponential Smoothing")
        print("3) Savitzky-Golay Filter")
        print("4) Lowess Smoothing")
        print("5) Gaussian Filter")
        print("6) Help")
        print("7) Return to Main Menu")

        method_choice = input("Enter your choice: ")
        if method_choice == "6":
            print_smoothing_help()
            break
        if method_choice == "7":
            break
        else:
            method_params = get_method_parameters(method_choice)
            method_name, params = convert_choice_to_method(method_choice, method_params)
            smoothed_data_by_file = apply_smoothing_to_all_files(
            data_by_file, '[H2O2]', method_name, params)

            plot_smoothed_data_facet_grid(smoothed_data_by_file, data_by_file)

            # Ask user if they are satisfied
            user_satisfied = input("Are you satisfied with the smoothing? (y/n): ").lower()
            if user_satisfied == 'y':
                export_smoothed_data(smoothed_data_by_file,data_by_file,path)
                print('Good')
                print(smoothed_data_by_file)
            #export_smoothed_data(smoothed_data_by_file)
                break


def apply_smoothing_to_all_files(data_by_file, column_name, method, params):
    smoothed_data_by_file = {}

    for filename, df in data_by_file.items():
        data = df[column_name]
        time = df['Time (s)'] if 'Time (s)' in params else None  # Only get time if needed for the method
        smoothed_data = apply_smoothing_method(data, time, method, params)
        smoothed_data_by_file[filename] = smoothed_data


    return smoothed_data_by_file

def get_method_parameters(choice):

    params = {}
    if choice == "1":
        # Moving Average requires a window size
        window_size = int(input("Enter window size for Moving Average: "))
        params['window_size'] = window_size
    elif choice == "2":
        # Exponential Smoothing requires an alpha value
        alpha = float(input("Enter alpha value for Exponential Smoothing (0 < alpha < 1): "))
        params['alpha'] = alpha
    elif choice == "3":
        # Savitzky-Golay Filter requires a window size and a polynomial order
        window_size = int(input("Enter window size for Savitzky-Golay Filter: "))
        poly_order = int(input("Enter polynomial order for Savitzky-Golay Filter: "))
        params['window_size'] = window_size
        params['poly_order'] = poly_order
    elif choice == "4":
        # Lowess Smoothing requires a fraction of the data to be used in smoothing
        frac = float(input("Enter fraction for Lowess Smoothing (0 < frac < 1): "))
        params['frac'] = frac
    elif choice == "5":
        # Gaussian Filter requires a sigma value
        sigma = float(input("Enter sigma value for Gaussian Filter: "))
        params['sigma'] = sigma

    return params


def convert_choice_to_method(choice, params):
    method_name = None
    if choice == "1":
        method_name = 'moving_average'
    elif choice == "2":
        method_name = 'exponential'
    elif choice == "3":
        method_name = 'savitzky_golay'
    elif choice == "4":
        method_name = 'lowess'
    elif choice == "5":
        method_name = 'gaussian'
    return method_name, params

def apply_smoothing_method(data, time, method_name, params):
    if method_name == 'moving_average':
        return moving_average_smoothing(data, **params)
    elif method_name == 'exponential':
        return exponential_smoothing(data, **params)
    elif method_name == 'savitzky_golay':
        return savitzky_golay_smoothing(data, **params)
    elif method_name == 'lowess':
        # Lowess smoothing requires time, ensure it's provided
        if time is not None:
            return lowess_smoothing(data, time, **params)
        else:
            raise ValueError("Time series is required for lowess smoothing.")
    elif method_name == 'gaussian':
        return gaussian_smoothing(data, **params)
    else:
        raise ValueError(f"Unknown smoothing method: {method_name}")






def apply_smoothing_to_all_files(data_by_file, column_name, method, params):
    smoothed_data_by_file = {}

    for filename, df in data_by_file.items():
        data = df[column_name]
        time = df['Time (s)'] if 'Time (s)' in params else None  # Only get time if needed for the method
        smoothed_data = apply_smoothing_method(data, time, method, params)
        smoothed_data_by_file[filename] = smoothed_data

    return smoothed_data_by_file

def apply_smoothing_method(data, time, method, params):
    if method == 'moving_average':
        return moving_average_smoothing(data, **params)
    elif method == 'exponential':
        return exponential_smoothing(data, **params)
    elif method == 'savitzky_golay':
        return savitzky_golay_smoothing(data, **params)
    elif method == 'lowess':
        # Lowess requires the time parameter
        if time is not None:
            return lowess_smoothing(data, time, **params)
        else:
            raise ValueError("Time series is required for lowess smoothing.")
    elif method == 'gaussian':
        return gaussian_smoothing(data, **params)
    else:
        raise ValueError(f"Unknown smoothing method: {method}")


def plot_smoothed_data_facet_grid(smoothed_data_by_file, raw_data_by_file, column_name='[H2O2]'):
    # Assuming that smoothed_data_by_file and raw_data_by_file are dictionaries
    # with filenames as keys and Pandas Series/DataFrames as values.

    # Create a Pandas DataFrame to hold all the data for plotting
    plot_data = pd.DataFrame()

    for filename in smoothed_data_by_file:
        # Get raw and smoothed data
        raw_data = raw_data_by_file[filename][column_name]
        smoothed_data = smoothed_data_by_file[filename]

        # Combine raw and smoothed data into a single DataFrame
        temp_df = pd.DataFrame({
            'Time (s)': raw_data_by_file[filename]['Time (s)'],
            'Raw Data': raw_data,
            'Smoothed Data': smoothed_data,
            'Filename': filename
        })

        # Append to the main DataFrame
        plot_data = pd.concat([plot_data, temp_df])

    # Melt the DataFrame to have a long-form DataFrame which seaborn can use to plot
    plot_data_melted = plot_data.melt(id_vars=['Time (s)', 'Filename'],
                                      var_name='Data Type', value_name=column_name)

    # Create a FacetGrid object with seaborn
    g = sns.FacetGrid(plot_data_melted, col='Filename', col_wrap=3, hue='Data Type', sharey=False)

    # Map the data to the grid
    g = g.map(plt.plot, 'Time (s)', column_name, marker=".")

    # Add a legend
    g.add_legend()

    # Adjust the axis labels and titles
    g.set_axis_labels('Time (s)', column_name)
    g.set_titles('{col_name}')

    # Show the plot
    plt.show()

# Example usage of the function:
# plot_smoothed_data_facet_grid(smoothed_data_by_file, data_by_file)


def export_smoothed_data(smoothed_data_by_file, raw_data_by_file, path):
    # Create an empty DataFrame for the long-form data
    longform_data = pd.DataFrame()

    for filename, smoothed_data in smoothed_data_by_file.items():
        # Get the corresponding raw data for the time column
        raw_data = raw_data_by_file[filename]
        # Combine the time, raw, and smoothed data into a single DataFrame
        temp_df = pd.DataFrame({
            'Filename': filename,
            'Time (s)': raw_data['Time (s)'],
            '[H2O2]': smoothed_data

        })
        # Append to the long-form DataFrame
        longform_data = pd.concat([longform_data, temp_df])

    # Reset index before saving to ensure a clean CSV format
    longform_data.reset_index(drop=True, inplace=True)
    os.chdir(path)
    # Export to CSV
    longform_data.to_csv("smoothed_data.csv", index=False)
    print("Exported combined smoothed data to 'combined_smoothed_data.csv'")

