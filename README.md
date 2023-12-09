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


### Starting the program

Perfrom a git clone on this respository and remember the local respository position. If you dont create a PATH VARIABLE to this position, the program can be initialized using:

python rde_analyzer.py -p "PATH" -c COMMA,SEPERATED,H202,CONCENTRATIONS 

  -p flag is the full path to the foler containing your data and should be written with quotations<br>
  -c flag is the concentrations of H2O2 used for the standard cruve e.i 0,20,40,60,80,100<br>


## Performing the analysis

### Analysis

Once the program is sucessfully started, the RDE ANALYZER logo should apear and the menu will allow both initial analysis and post analysis data handeling. 



     Once Analysis is chosen, the first data file will be read in and the raw data will be plotted, this will allow        the user to inspect the raw data and choose if the analysis should be continued on this file. Exit the figure 
     window to continue.

     1. Baseline selection, due to the drift in the system, all values need to be corrected for a baseline shift, 
       this can be done by selecting either one or two point calibration. By using the mouse, select one point in the 
       first 30 seconds, and a second point during the return to baseline after the reaction is done. After selecting 
       two points, exit the figure. This will show the selected points and the baseline regression, approve the 
       selection by typing (y)
    
     2. Calibration, the next window will allow the selection of the calibration data points, zoom into the 
       calibration region and remeber to un-click the zoom button. Select all the calibration points and exit the 
       window. This will show you where the selection wsa performed. Confirm your selection with (y) and continue 
       exiting the windows until all calibration related plots are complete.
    
     3. Pick data start, using the zoom function zoom inn to the start of the data and pick only one point. Exit the 
       plot after selection and confirm the truncation with (y).
    
Once the truncation is complete that data file is complete and it will be moved to new folder called (Analyzed)                


## Post analysis data processing

### Data smoothing

Smoothing Methods Explanation
This module includes several smoothing methods, each with specific inputs to control their behavior:

1. Moving Average  

  window_size: Specifies the number of data points used in each average. A larger window size results in smoother       curves, but can potentially remove important trends or patterns.<br>

2. Exponential Smoothing

  alpha: A smoothing factor between 0 and 1. A higher alpha discounts older observations faster, providing a method     that is more responsive to recent changes in the data.<br>

3. Savitzky-Golay Filter

  window_size: Determines the number of data points used in the local polynomial regression. As with the moving         average, a larger window will produce a smoother curve.
  poly_order: The order of the polynomial used in the regression. A higher order can fit more complex data patterns,    but may also lead to overfitting.<br>

4. Lowess Smoothing (Locally Weighted Scatterplot Smoothing)

  frac: Represents the fraction of data points used to compute each value in the smoothed curve. A smaller fraction     focuses more closely on local data points, making the curve more sensitive to local variations.<br>

5. Gaussian Filter

  sigma: Defines the standard deviation for the Gaussian kernel. A higher sigma value means a wider kernel, leading     to a smoother curve. This method is particularly effective for removing noise while preserving edges.


Each of these methods provides a unique approach to smoothing data, allowing for flexibility in data analysis. By adjusting the input parameters, users can tailor the smoothing to the specific needs of their dataset.

## Plotting

There are several plotting methods that will allow plotting the output files.  

  1. Plot data

     When selecting this selection, the raw data will be plotted allowing a review of all the data.

  2. Plot smoothed data

     When selecting this selection, the smoothed data can be selected and plotted

  3. Plot smoothed over raw data

     The user will be prompted to first choose the raw data, then the smoothed data, this will allow showing the   
     smoothed data over the raw traces.

 4. Plot initial rates

    This selection plots the initial rates as a bar plot. 
