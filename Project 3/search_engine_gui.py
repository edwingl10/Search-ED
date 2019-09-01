import tkinter
from webbrowser import BackgroundBrowser


class display_main_window:
    def __init__(self):
        ''' Used to start and display the main search engine window
        '''
        
        #creates root window
        self.root_window = tkinter.Tk()
        self.root_window.title("Search-ED")
        self.root_window.configure(background="ghost white")
        
        
        
        #creates label 'Search-ED'
        self.engine_name_label = tkinter.Label(self.root_window, text="Search-ED",
                                          font=("Helvetica",80), fg="coral").grid(row=0, column=1)
                                          
                                          
        #used to store text entry                                
        self.entry_query = tkinter.StringVar()
        #creates entry and stores value to entry_query variable
        self.search_box = tkinter.Entry(self.root_window, width=40, textvariable=self.entry_query,
                                        highlightbackground="RoyalBlue4", font=("Helvetica",20)).grid(row=1, column=1)
        #creates button and calls the search_button_clicked when button is clicked
        self.search_button = tkinter.Button(self.root_window, text="ED SEARCH", font=("Helvetica",20),
                                       command=self.search_button_clicked).grid(row=2,column=1, padx=10, pady=10)
        
        
        
        self.root_window.bind("<configure>")
        self.root_window.rowconfigure(1, weight=1)
        self.root_window.rowconfigure(2, weight=1)
        self.root_window.columnconfigure(1, weight=1)
        
        self.root_window.mainloop()
        
        
        
    
    def search_button_clicked(self):
        ''' Used to close the window and to return the text within the query 
        '''
        self.destroy()
        return self.entry_query.get()
        
        
    def destroy(self):
        self.root_window.quit()
        

###########################################################################################


class display_results_window:
    def __init__(self, results):
        ''' used to start and display the results page
        '''
        
        
        self.root_window = tkinter.Tk()
        self.root_window.title("Results")
        self.root_window.configure(background="ghost white")
        
        self.query_results = results
        
        #calls function to display results to window
        self.display_results()
        
        self.root_window.bind("<configure>")
        self.root_window.columnconfigure(0, weight=1)
                                                                                                                                  
        self.root_window.mainloop()
        
        
        
    def display_results(self):
        ''' used to display the results to the window
        '''
        
        self.resuls_label = tkinter.Label(self.root_window, text="RESULTS",
                                               font=("Helvetica",70), fg="coral").grid(row=0, column=0)
                                               
        if len(self.query_results) == 0:
            tkinter.Label(self.root_window, text="Sorry, No Results Were Found.",
                          font=("Helvetica", 18), fg="steel blue").grid(row=1, column=0)
            
        else:
            count=0
            for result in self.query_results:
                tkinter.Label(self.root_window, text=result, font=("Helvetica",18),
                              fg="steel blue").grid(row=count+1, column=0)
                count += 1
        
    
    