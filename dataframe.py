import pandas as pd
import webbrowser
import os
from IPython.display import HTML

def create_dataframe(track_data):
    
# Create a DataFrame from the track data
    df = pd.DataFrame(track_data)
    
    # onvert the Album Artwork URL column to HTML
    df["Art"] = df["Art"].apply(lambda url: f'<img src="{url}" width="50" >')
    
    #Offset the DataFrame index so the top row is 1
    df.index += 1
    
    #Convert the DataFrame to HTML and center the text
    df_html = df.to_html(classes='mystyle', escape=False)
    
    #Center the text
    css = """
    <style>
    .mystyle thead th, .mystyle tbody td{
        text-align: center;
    }
    </style>
    """
    
    #Save the DataFrame to an HTML file
    with open('df.html', 'w') as f:
        f.write(css)
        f.write(df_html)
    
    #Open the HTML file
    webbrowser.open('file://' + os.path.realpath('df.html'))
    
    return df