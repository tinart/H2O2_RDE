# RDE Analyser Sofware Manual

This README contains an overview over the most common usecases of the RDE analyser software. The methodology was developed by Dr. Lorenz Schwaiger in the Roland Ludwig lab, Boku, Austria, and the full description can be read in the initial publication (DOI). Please note that this software will only aid in handling the data generated using the rotating disk electrode, and the scientific entepretation of the results are soley the responsibility of the researcher. 

## Initializing the software

### Data file type requirements 

The data files must be in .csv files, that are seperated using (,) to ensure that the file structure is correct for the CLI, use the create_rde_analysis_file_structure.py program. This is used as follow:

create_rde_analysis_file_structure.py -p 'PATH/TO/DATA' -o '.old_file_ext' -n '.new_file_ext'

  '-p', '--path', required=True, help="Path to the directory containing the files")<br>
  '-o', '--old', required=True, help="Old file extension to be replaced"<br>
  '-n', '--new', required=True, help="New file extension to replace the old one"<br>

This will re-write all your files to be .csv files and remove Byte Order Marks from your data files. Therefore, keep a backup of you data at a secondary position.  


### Performing the data analysis

Perfrom a git clone on this respository and remember the local respository position. If you dont create a PATH VARIABLE to this position, the program can be initialized using:

python rde_analyzer.py -p "PATH" -c COMMA,SEPERATED,H202,CONCENTRATIONS 

  -p flag is the full path to the foler containing your data and should be written with quotations
  -c flag is the concentrations of H2O2 used for the standard cruve e.i 0,20,40,60,80,100





## Performing the analysis

## Post analysis data processing

### Data smoothing

Smoothing Methods Explanation
This module includes several smoothing methods, each with specific inputs to control their behavior:

Moving Average  

window_size: Specifies the number of data points used in each average. A larger window size results in smoother curves, but can potentially remove important trends or patterns.
Exponential Smoothing

alpha: A smoothing factor between 0 and 1. A higher alpha discounts older observations faster, providing a method that is more responsive to recent changes in the data.
Savitzky-Golay Filter

window_size: Determines the number of data points used in the local polynomial regression. As with the moving average, a larger window will produce a smoother curve.
poly_order: The order of the polynomial used in the regression. A higher order can fit more complex data patterns, but may also lead to overfitting.
Lowess Smoothing (Locally Weighted Scatterplot Smoothing)

frac: Represents the fraction of data points used to compute each value in the smoothed curve. A smaller fraction focuses more closely on local data points, making the curve more sensitive to local variations.
Gaussian Filter

sigma: Defines the standard deviation for the Gaussian kernel. A higher sigma value means a wider kernel, leading to a smoother curve. This method is particularly effective for removing noise while preserving edges.
Each of these methods provides a unique approach to smoothing data, allowing for flexibility in data analysis. By adjusting the input parameters, users can tailor the smoothing to the specific needs of their dataset.
