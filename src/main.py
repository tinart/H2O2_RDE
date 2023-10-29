from data_analysis import analyze

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
            print('2')
        elif choice == "3":
            print('3')
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
