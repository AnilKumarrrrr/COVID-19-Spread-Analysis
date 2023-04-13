import pandas as pd
import folium
from flask import Flask, render_template

app = Flask(__name__)

def find_top_confirmed(n=15):
    # Read data from CSV file
    corona_df = pd.read_csv("dataset3.csv")

    # Group data by Province_State and sum Confirmed, Deaths, Recovered and Active columns
    by_country = corona_df.groupby('Province_State').sum()[['Confirmed', 'Deaths', 'Recovered', 'Active']]

    # Select the top n confirmed cases and return as a DataFrame
    cdf = by_country.nlargest(n, 'Confirmed')[['Confirmed']]

    return cdf

def generate_map():
    # Read data from CSV file
    corona_df = pd.read_csv("dataset3.csv")

    # Select only relevant columns and remove rows with missing values
    corona_df = corona_df[['Lat', 'Long_', 'Confirmed']].dropna()

    # Create a map centered on India
    m = folium.Map(location=[28.7041, 77.1025], tiles='Stamen toner', zoom_start=4)

    # Add circles to the map for each location
    for index, row in corona_df.iterrows():
        folium.Circle(location=[row['Lat'], row['Long_']],
                      radius=float(row['Confirmed']),
                      color='red',
                      popup='Confirmed cases: {}'.format(row['Confirmed'])
                     ).add_to(m)

    # Convert the map to HTML and return
    return m._repr_html_()

@app.route('/')
def home():
    # Get the top confirmed cases as a DataFrame and generate the map
    cdf = find_top_confirmed()
    cmap = generate_map()

    # Format the top confirmed cases as a list of pairs
    pairs = [(province_state, confirmed) for province_state, confirmed in zip(cdf.index, cdf['Confirmed'])]

    # Render the home page with the data and map
    return render_template('home.html', table=cdf, cmap=cmap, pairs=pairs)

if __name__ == '__main__':
    app.run(debug=True)
