import pandas as pd
import webbrowser
import os
from IPython.display import HTML

def create_dataframe(track_data):
    #create dataframe with basic default information (Artist, Song title, Album Artwork URL)
    df = pd.DataFrame(track_data)
    
    # Convert the Album Artwork URL column to HTML
    df["Art"] = df["Art"].apply(lambda url: f'<img src="{url}" width="50" >')
    
    #offset dataframe so top row is 1
    df.index += 1
    
    # Display the DataFrame
    
    #save df to a HTML file
    df.to_html('df.html', escape=False)
    
    #open created HTML file
    webbrowser.open('file://' + os.path.realpath('df.html'))
    
    return df