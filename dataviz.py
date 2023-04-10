# pip install matplotlib seaborn

import sqlite3
import pandas as pd

def get_user_data():
    conn = sqlite3.connect("needs_database.db")
    cursor = conn.cursor()

    query = """
        SELECT needs.need, user_data.location, user_data.num_people,
               user_data.demographics, user_data.effect
        FROM user_data
        JOIN needs ON user_data.need_id = needs.id
    """
    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

user_data_df = get_user_data()


import matplotlib.pyplot as plt
import seaborn as sns

def plot_effect_bar_chart(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="need", y="effect", data=df)
    plt.title("Effect of User Needs on Well-being")
    plt.xlabel("User Needs")
    plt.ylabel("Effect")
    plt.show()

plot_effect_bar_chart(user_data_df)


def plot_num_people_pie_chart(df):
    num_people_by_need = df.groupby("need")["num_people"].sum()
    plt.figure(figsize=(10, 6))
    num_people_by_need.plot(kind="pie", autopct="%.1f%%")
    plt.title("Number of People with Specific Needs")
    plt.ylabel("")
    plt.show()

plot_num_people_pie_chart(user_data_df)



# map 

# pip install folium geopy


from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="user_needs_map")

def geocode_location(location):
    try:
        geocode_result = geolocator.geocode(location)
        if geocode_result:
            return geocode_result.latitude, geocode_result.longitude
    except Exception as e:
        print(f"Error geocoding location {location}: {e}")

    return None


import folium

def create_weighted_needs_map(df):
    # Calculate the weight for each need (number of people * effect)
    df["weight"] = df["num_people"] * df["effect"]

    # Geocode location names to coordinates
    df["coordinates"] = df["location"].apply(geocode_location)

    # Drop rows with missing coordinates
    df = df.dropna(subset=["coordinates"])

    # Create a base map
    needs_map = folium.Map(location=[39.50, -98.35], zoom_start=4)

    # Add weighted needs to the map
    for index, row in df.iterrows():
        need = row["need"]
        location = row["location"]
        coordinates = row["coordinates"]
        weight = row["weight"]

        popup_text = f"{location}: {need} (Weight: {weight})"
        folium.CircleMarker(
            location=coordinates,
            radius=weight / 10,  # Adjust the scaling factor as needed
            popup=popup_text,
            color="blue",
            fill=True,
            fill_opacity=0.6,
        ).add_to(needs_map)

    return needs_map

weighted_needs_map = create_weighted_needs_map(user_data_df)
weighted_needs_map.save("weighted_needs_map.html")


# This code creates an interactive map using Folium and Geopy, with circles representing user needs, weighted by the number of people and the effect on the need. The size of the circles will be proportional to the weight. The map will be saved as an HTML file, which you can open in a web browser.

# You may need to adjust the scaling factor (currently set to 10) to better visualize the weights on the map. Also, consider handling geocoding errors or missing coordinates more gracefully, as this example simply drops rows with missing coordinates.