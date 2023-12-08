import pandas as pd
import csv
from file_handling import find_csv_files, select_csv_file
import seaborn as sns
import matplotlib.pyplot as plt


def plotting_handler(csv_file_path,path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        files_list = next(reader)  # Assuming the first row contains filenames
        return files_list
    plotting_menu(files_list,path)





def plotting_menu(path):


    while True:
        print("\nSmoothing Methods:")
        print("1) Plot data")
        print("2) Plot smoothed data")
        print("3) Plot smoothed data over raw data")
        print("4) Plot intital rates")
        print("5) Return to Main Menu")

        method_choice = input("Enter your choice: ")

        if method_choice == "5":
            break
        elif method_choice == '1':
            raw_csv_file = find_csv_files(path)
            print('Select raw data file')
            raw_data_path = select_csv_file(raw_csv_file, path)
            plot_raw_data(raw_data_path)

        elif method_choice == '2':

            smoothed_csv_file = find_csv_files(path)
            print('Select smoothed data file')
            smoothed_data_path = select_csv_file(smoothed_csv_file, path)
            plot_smoothed_data(smoothed_data_path)

        elif method_choice == '3':

            raw_csv_file = find_csv_files(path)
            print('Select raw data file')
            raw_data_path = select_csv_file(raw_csv_file,path)
            smoothed_csv_file = find_csv_files(path)
            print('Select smoothed data file')
            smoothed_data_path = select_csv_file(smoothed_csv_file, path)
            plot_smoothed_over_raw(raw_data_path, smoothed_data_path)

        elif method_choice == '4':
            file_list = list_files_from_csv(path)
            ask_user_for_replicates(file_list)
        else:
            print('Invalid choice, please select a number from the menu.')

def plot_smoothed_over_raw(raw_data_path, smoothed_data_path):
    # Read the data
    raw_data_df = pd.read_csv(raw_data_path)
    smoothed_data_df = pd.read_csv(smoothed_data_path)

    # Combine both datasets for plotting
    combined_data = pd.merge(raw_data_df, smoothed_data_df, on=['Filename', 'Time (s)'], suffixes=('_raw', '_smoothed'), how='inner')

    # Initialize and plot the FacetGrid
    g = sns.FacetGrid(combined_data, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]_raw', marker=".", label="Raw Data", alpha=0.5)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]_smoothed', marker="", color='red', label="Smoothed Data", linewidth=2)

    # Add a legend to each subplot
    for ax in g.axes.flatten():
        ax.legend()

    # Adjust the plot titles
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Comparison of Raw and Smoothed [H2O2] Data Across Different Experiments')

    # Show plot
    plt.show()


def plot_raw_data(raw_data_path):
    # Read the raw data
    raw_data_df = pd.read_csv(raw_data_path)

    # Plot the raw data using FacetGrid
    g = sns.FacetGrid(raw_data_df, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]', marker=".", label="Raw Data", alpha=0.5)
    g.add_legend()
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Raw [H2O2] Data Across Different Experiments')
    plt.show()

def plot_smoothed_data(smoothed_data_path):
    # Read the smoothed data
    smoothed_data_df = pd.read_csv(smoothed_data_path)

    # Plot the smoothed data using FacetGrid
    g = sns.FacetGrid(smoothed_data_df, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]', marker="", color='red', label="Smoothed Data", linewidth=2)
    g.add_legend()
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Smoothed [H2O2] Data Across Different Experiments')
    plt.show()


def list_files_from_csv(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        files_list = next(reader)  # Assuming the first row contains filenames
        return files_list

def ask_user_for_replicates(files_list):
    replicates_info = {}
    for i, file_name in enumerate(files_list, start=1):
        print(f"{i}) {file_name}")
    print("Please specify which numbers are replicates in the format: 1,2; 3,4")
    print("This means 1 and 2 are replicates, and 3 and 4 are replicates.")
    user_input = input("Enter replicates: ")
    for group in user_input.split(';'):
        replicate_group = list(map(str.strip, group.split(',')))
        for replicate in replicate_group:
            replicates_info[replicate] = replicate_group
    return replicates_info


