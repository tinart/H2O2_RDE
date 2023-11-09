import os.path

from data_analysis import analyze, intial_rate_analysis, plot_precomputed_rolling_regression_facet_grid, intial_rate_manual
from data_smoothing import smooth_data
import argparse



def main():
    parser = argparse.ArgumentParser(description="Data Processing CLI")
    parser.add_argument("-p", "--path", required=True, help="Path to the data file")
    args = parser.parse_args()

    path = args.path

    print("""
    
                             
                              
         Credits:                                                ..                
            -Methodology: Lorenz Schwaiger                       ..               
            -Software: Ole Golten                               :++.               
                                                               .+=+=               
                                                               ==..+.             
                                                              -+. .:=             
                                                             .+:  ..+              
                                                             +-     ::           
                                                           .==.     .+.          
                                                          .-=.       .:          
                                                         .-:.         =:           
                                                        .=.            =-.        
                                                      .==.              :+:       
                                                   .:+-.                  :+-.      
                                              ..=++:.                       ..+=.  
                                   ...::-=+==-.                                  :=-:.   
                    ....-=+++++=:......                                                ...:=++-:..... 
            .--:.                                       RDE ANALYZER                   .:--::::-----::.. 
            .-:::-----=++++++++++=-:.                                            .+=..      
                                      ...:-=+=-.                           .-=:.       
                                               .=+..                    .=-.             
                                                  .:=.                 -=.                
                                                    .=.              ==.                  
                                                     -=            .=- 
                                                      +-        .=-  
                                                      -+.      ==.  
                                                      .+-    .+:    
                                                       ==:  .+.     
                                                       :+=..=:      
                                                        ++=:=
                                                        -+++        
                                                         =+        
                                     
                
    """)
    
    
    while True:
        print("\nMenu:")
        print("1) Analysis")
        print("2) Smoothing")
        print("3) Determine Initial Rate")
        print("4) Plot Data")
        print("5) Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            analyze(path)
        elif choice == "2":
            file_name = input('\nType in .csv filename')

            smoothing_window = input('\nSelect window size for smothing')
            smooth_data(input_csv_path= os.path.join(path,file_name),window_size=smoothing_window)
        elif choice == "3":
            file_name = input('\nType in .csv filename')
            intial_rate_manual(file_name, path)

            #data, results = intial_rate_analysis(input_filename=file_name)
            #plot_precomputed_rolling_regression_facet_grid(data, results)
        elif choice == "4":
            print('4')
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")




if __name__ == '__main__':
    main()

    #data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\b\Selection'
