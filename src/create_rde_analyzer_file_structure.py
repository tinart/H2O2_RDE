
import os
import sys
import csv
import argparse

def rename_file_extension(directory_path, old_extension, new_extension):
    # Get a list of all files with the old extension in the directory
    files_to_rename = [filename for filename in os.listdir(directory_path) if filename.endswith(old_extension)]

    # Iterate through each file and rename it to have the new extension
    for old_filename in files_to_rename:
        new_filename = os.path.splitext(old_filename)[0] + new_extension
        os.rename(
            os.path.join(directory_path, old_filename),
            os.path.join(directory_path, new_filename)
        )

    print("File extensions have been changed.")

def remove_bom_from_csv_files(directory_path):
    # Get a list of all CSV files in the directory
    csv_files = [filename for filename in os.listdir(directory_path) if filename.endswith(".csv")]

    for csv_filename in csv_files:
        file_path = os.path.join(directory_path, csv_filename)

        # Read the file and remove BOM if present
        with open(file_path, 'r', newline='', encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)
            data = [row for row in reader]

        # Rewrite the original file without BOM
        with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(data)

        print(f"BOM removed from '{file_path}'.")

def keep_two_columns(directory_path):

    #Create new dir
    processed_dir = os.path.join(directory_path, "processed_files")
    os.makedirs(processed_dir, exist_ok=True)
    # Get a list of all CSV files in the directory
    csv_files = [filename for filename in os.listdir(directory_path) if filename.endswith(".csv")]

    for csv_filename in csv_files:
        file_path = os.path.join(directory_path, csv_filename)
        output_file_path = os.path.join(processed_dir, f"{csv_filename[:-4]}_processed.csv")  # New file name

        # Open the CSV file for reading and the output file for writing
        with open(file_path, 'r', newline='') as csv_file, open(output_file_path, 'w', newline='') as output_file:
            csv_reader = csv.reader(csv_file)
            csv_writer = csv.writer(output_file)

            # Read the header row
            header = next(csv_reader)

            # Write the header with the first two columns to the output CSV file
            csv_writer.writerow([header[0], header[1]])

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Extract the first two columns
                first_column = row[0]
                second_column = row[1]

                # Write the first two columns to the output CSV file
                csv_writer.writerow([first_column, second_column])

        print(f"Processed file saved as '{output_file_path}' in '{processed_dir}'.")


def main():
    parser = argparse.ArgumentParser(description="RDE Analyzer File Structure Creation Script")
    parser.add_argument('-p', '--path', required=True, help="Path to the directory containing the files")
    parser.add_argument('-o', '--old', required=True, help="Old file extension to be replaced")
    parser.add_argument('-n', '--new', required=True, help="New file extension to replace the old one")
    args = parser.parse_args()

    directory_path = args.path
    old_extension = args.old
    new_extension = args.new

    if not os.path.isdir(directory_path):
        print("Error: The specified path is not a directory.")
        sys.exit(1)

    rename_file_extension(directory_path, old_extension, new_extension)
    remove_bom_from_csv_files(directory_path)

if __name__ == "__main__":
    main()
