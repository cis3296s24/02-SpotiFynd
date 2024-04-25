import os
import webbrowser

import pandas as pd


def create_dataframe(track_data):
    # Create a DataFrame from the track data
    df = pd.DataFrame(track_data)

    # Convert the Album Artwork URL column to HTML
    df["Art"] = df["Art"].apply(lambda url: f'<img src="{url}" width="50" >')

    # Offset the DataFrame index so the top row is 1
    df.index += 1

    # Setting song names to be hyperlinks to the song's URI.
    df['Song'] = df.apply(lambda x: f'<a href="{x["uri"]}">{x["Song"]}</a>', axis=1)
    df.drop(columns=['uri'], inplace=True)

    # Convert the DataFrame to HTML and center the text
    df_html = df.to_html(classes='mystyle', escape=False)

    # Center the text
    css = """
    <style>
    .mystyle thead th, .mystyle tbody td{
        text-align: center;
    }
    </style>
    """

    # Makes the table sortable
    js = """
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
    <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.5.1.js"></script>
    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {
        $('.mystyle').DataTable();
    });
    </script>
    """

    # Save the DataFrame to an HTML file
    with open('df.html', 'w', encoding='utf-8') as f:
        f.write(css)
        f.write(js)
        f.write(df_html)

    # Open the HTML file
    webbrowser.open('file://' + os.path.realpath('df.html'))

    return df
