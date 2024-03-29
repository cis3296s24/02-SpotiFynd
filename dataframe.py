import pandas as pd
import webbrowser
import os

def create_dataframe(track_data):
    #create dataframe with basic default information (Artist and Song title)
    df = pd.DataFrame(track_data)   
    #save df to a HTML file
    df.to_html('df.html')
    #open created HTML file
    webbrowser.open('file://' + os.path.realpath('df.html'))
    
    return df