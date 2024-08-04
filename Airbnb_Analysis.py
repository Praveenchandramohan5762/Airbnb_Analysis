# Importing Libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import mysql.connector

# Setting up page configuration
icon = st.image("Downloads\\airbnb_logo.jpg")
st.set_page_config(
                page_title="Airbnb Data Visualization",
                page_icon=icon,
                layout="wide",
                initial_sidebar_state="expanded")

# Title and Introduction Section
# st.image("airbnb_logo.jpg",width=350)  

st.image("airbnb_logo.jpg", width=350, use_column_width=False)
st.title(":red[ Airbnb Data Analysis: A User-friendly Dashboard]")

# Creating option menu in home page
selected = option_menu(
        "Airbnb Data Visualization | Analyze Data",
        ["Home", "View Details", "Overview", "Explore Insights"],
        icons=["house", "check", "graph-up-arrow", "bar-chart-line"],
        menu_icon="globe",
        default_index=0,
        orientation='horizontal',
        styles={ "nav-link": {"font-size": "20px","text-align": "left","margin": "-2px","--hover-color": "#FF5A5F"},
                "nav-link-selected": {"background-color": "#FF5A5F"}})

# HOME PAGE
if selected == "Home":

    # Dynamic Columns Layout
    col1, col2 = st.columns([2, 1], gap="medium")
    
    with col1:
        st.markdown("### :red[Domain]: Travel Industry, Property Management, and Tourism")
        st.markdown("### :red[Technologies Used]: Python, Pandas, Plotly, Streamlit")
        st.markdown(""" ### :red[Overview]: ##
                    \n- Processed an Airbnb JSON 2019 dataset using Python for structured DataFrame transformation,\n- Applied data preprocessing techniques, including thorough data cleaning for accuracy and reliability,\n- Analyzed Airbnb data for pricing, availability, and location trends,\n- Developed interactive visualizations and dynamic plots to provide valuable insights for hosts and guests """
        )

    with col2:
        st.image("https://media.gq.com/photos/616f02741269f766981e8bd9/4:3/w_844,h_633,c_limit/airbnb-cabins.gif", 
            width=600, 
            caption="Explore the  Insights in Airbnb Data! ", 
            use_column_width=True, 
            )
    
    # Adding Interactive Elements
    st.markdown("---")
    st.markdown("### :red[:rainbow[ Discover More Insights]]")
    
    col3, col4, col5 = st.columns(3, gap="medium")
    
    with col3:
        if st.button("View Pricing Insights"):
            st.write("Explore the interactive visualization to see how pricing varies across different locations and times of the year.")
            st.image("Airbnbimage.png")
    
    with col4:
        if st.button("Check Availability Patterns"):
            st.write("Analyze availability trends to understand how occupancy rates fluctuate seasonally and geographically.")
            st.image("imgAirbnb.png")
    with col5:
        if st.button("Discover Location Trends"):
            st.write("Gain insights into popular areas and emerging hotspots by visualizing location-based trends in Airbnb listings.")
            st.image("https://i.pinimg.com/originals/54/ef/14/54ef147d0e43918ca829a7982c9ed8d2.jpg")
    st.markdown("---")

    st.subheader(':red[Power BI :]')
    st.markdown("** The project was illustrated using Power BI. Click the button below to check out the dashboard.**")   
    st.info("""
            #### Notable findings from Power BI Dashboard
            - 📅 Ranking and visualizing each combination of country, room type, and property type
            - 🌐 The Total Count of Properties and Hosts
            - 📊 The Average of listing Price, Accommodation, Availability, number of Review Scores, and Review scores
            - 💡  Room type based average price, reviews, scores and sum of total bedrooms
            - 📈 The average number of reviews and review scores by room type
            - 🗺️ Geo representation of room type and Average listing Price
            """, icon="🔍")

    # Image paths
    image_path1 = ('Powerbi_img1.png')
    image_path2 = ('Powerbi_imgmap2.png')

    # Button to select which image to show
    if st.button('View Dashboard 1'):
        st.image(image_path1, caption='Power BI Dashboard ', use_column_width=True)

    if st.button('View Dashboard 2'):
        st.image(image_path2, caption='Power BI Dashboard ', use_column_width=True)

    st.markdown("---")
#-----------------------------------------
# View Details PAGE

# Connect to MySQL database
mydb = mysql.connector.connect( host="localhost", user="root", password="Praveen1234@", database="airbnb_data") # MySQL DB Connection
print(mydb)
mycursor = mydb.cursor() 

if selected == "View Details":
    st.subheader(":red[Explore Accommodation by Country]")

    mycursor.execute('''SELECT DISTINCT country FROM Airbnb_data''')
    result = mycursor.fetchall()
    df_Country = pd.DataFrame(result, columns=["country"])
    selected_country = st.selectbox("### Select Country", options=df_Country['country'].tolist(), index=None)

    if selected_country:
        check = st.checkbox(f"Click to view Accommodation by Property wise and room type in {selected_country}")

        if check:
            st.subheader(f":red[Explore Accommodation by Property wise and room type in {selected_country}]")

            mycursor.execute('''SELECT DISTINCT property_type 
                                FROM Airbnb_data
                                WHERE country=%s''', (selected_country,))
            result = mycursor.fetchall()
            df_property = pd.DataFrame(result, columns=["property_type"])
            selected_prop = st.selectbox('### Select a Property', options=df_property['property_type'].tolist(), index=None, key='prop_select')

            mycursor.execute('''SELECT DISTINCT room_type 
                                FROM Airbnb_data 
                                WHERE property_type=%s AND country=%s''', (selected_prop, selected_country))
            result = mycursor.fetchall()
            df_room = pd.DataFrame(result, columns=["room_type"])
            selected_room = st.selectbox('### Select a Room type', options=df_room['room_type'].tolist(), index=None, key='room_radio')

            if selected_room:
                mycursor.execute('''SELECT name as 'Hotel Name', property_type, room_type, price, longitude, latitude  
                                    FROM Airbnb_data 
                                    WHERE country = %s AND property_type = %s AND room_type = %s
                                    GROUP BY name, property_type, room_type''', (selected_country, selected_prop, selected_room))
                result = mycursor.fetchall()

                df = pd.DataFrame(result, columns=["Hotel Name", "property_type", "room_type", "price", "longitude", "latitude"])
                df[['longitude', 'latitude']] = df[['longitude', 'latitude']].astype('float')

                fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                        hover_name='Hotel Name', zoom=10,
                                        hover_data={'longitude': False, 'latitude': False, 'price': True, 'property_type': True, 'room_type': True},
                                        color_discrete_sequence=px.colors.colorbrewer.Blues_r)
                fig.update_layout(mapbox_style="open-street-map")
                fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

                st.plotly_chart(fig, use_container_width=True)

        else:
            mycursor.execute('''SELECT name as 'Hotel Name', price, longitude, latitude  
                                FROM Airbnb_data
                                WHERE country = %s''', (selected_country,))
            result = mycursor.fetchall()

            df = pd.DataFrame(result, columns=["Hotel Name", "price", "longitude", "latitude"])
            df[['longitude', 'latitude']] = df[['longitude', 'latitude']].astype('float')

            fig = px.scatter_mapbox(df, lat="latitude", lon="longitude",
                                    hover_name='Hotel Name', zoom=10,
                                    hover_data={'longitude': False, 'latitude': False, 'price': True},
                                    color_discrete_sequence=px.colors.colorbrewer.Blues_r)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------

# OVERVIEW PAGE
if selected == "Overview":
    col1, col2 = st.columns(2)

    # Read the CSV file into a DataFrame
    df = pd.read_csv(r"C:/Users/Praveen/Airbnb_data.csv")

    # RAW DATA TAB
    with col1:
        if st.button("Click to view Raw data"):
            raw_data = pd.read_csv('C:/Users/Praveen/Airbnb_data.csv')
            st.write(raw_data)

#INSIGHTS TAB
    with col1:
        # Add "Select All" option to the beginning of the list
        country_options = ['Select All'] + sorted(df['Country'].unique())
        prop_options = ['Select All'] + sorted(df['Property_type'].unique())
        room_options = ['Select All'] + sorted(df['Room_type'].unique())

        # Create Dropdown multiselects with "Select All" option
        country = st.sidebar.multiselect('Select Country', country_options, default=['Select All'])
        prop = st.sidebar.multiselect('Select Property Type', prop_options, default=['Select All'])
        room = st.sidebar.multiselect('Select Room Type', room_options, default=['Select All'])

        # Logic to handle "Select All" option
        if 'Select All' in country:
            country = sorted(df['Country'].unique())
        if 'Select All' in prop:
            prop = sorted(df['Property_type'].unique())
        if 'Select All' in room:
            room = sorted(df['Room_type'].unique())

        price = st.slider('Select Price', df['Price'].min(), df['Price'].max(), (df['Price'].min(), df['Price'].max()))

        query = f"Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}"

    col1, col2 = st.columns(2, gap='medium')
    col3 = st.columns(1)[0] 
    col4= st.columns(1)[0]  

    with col1:
        # 1.Top 10 Property Types
        df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df1, title='1. Top 10 Property Types', x='Listings', y='Property_type', orientation='h', color='Property_type', color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings', ascending=False)[:10]
        fig = px.bar(df2, title='3. Top 10 Hosts with Highest number of Listings', x='Listings', y='Host_name', orientation='h', color='Host_name', color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
        fig = px.pie(df1, title='2. Total Listings in each Room Types', names='Room_type', values='counts', color_discrete_sequence=px.colors.sequential.Rainbow)
        fig.update_traces(textposition='outside', textinfo='value+label')
        st.plotly_chart(fig, use_container_width=True)

        df2 = df.query(query).groupby(["Room_type"]).agg({"Price": "mean", "Name": "count"}).reset_index()
        df2.columns = ["Room_type", "Average_price", "Accommodation_count"]
        fig = px.bar(df2, x='Room_type', y='Average_price',  color='Average_price', title='4. Room type wise Accommodation count and Average price', 
                    color_continuous_scale=px.colors.sequential.Viridis)
        fig.update_traces(marker_line_width=1, marker_line_color='DarkSlateGrey')
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        df1 = df.query(query).groupby(["Property_type"]).agg({"Price": "mean", "Name": "count"}).reset_index()
        df1.columns = ["Property_type", "Average_price", "Accommodation_count"]
        fig = px.bar(df1, title='5. Property wise Accommodation count and Average price', x='Property_type', y=['Accommodation_count', 'Average_price'], barmode='group', color='Average_price', color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

        # Query
        df3 = df.query(query).groupby(["Property_type", "Room_type"]).agg({"Availability_365": "mean"}).reset_index()
        df3.columns = ["Property_type", "Room_type", "Average_availability_days"]
        fig = px.bar(df3, title='6. Average Availability days for specific property and country', 
            x='Average_availability_days', y='Property_type', orientation='h', color='Room_type', color_discrete_sequence=px.colors.qualitative.Bold)
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'Total_Listings'})
        fig = px.choropleth(country_df, title='7. Total Listings in each Country', locations='Country', locationmode='country names', color='Total_Listings', color_continuous_scale=px.colors.sequential.Plasma)
        fig.update_layout(mapbox_style="stamen-terrain")  # Change map style here
        st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------------

# EXPLORE PAGE
if selected == "Explore Insights":
    st.markdown("## Explore more about the Airbnb data")
    
    df = pd.read_csv(r"C:/Users/Praveen/Airbnb_data.csv")

    # Add "Select All" option to the beginning of the list
    country_options = ['Select All'] + sorted(df['Country'].unique())
    prop_options = ['Select All'] + sorted(df['Property_type'].unique())
    room_options = ['Select All'] + sorted(df['Room_type'].unique())

    # Create Dropdown multiselects with "Select All" option
    country = st.sidebar.multiselect('Select Country', country_options, default=['Select All'])
    prop = st.sidebar.multiselect('Select Property Type', prop_options, default=['Select All'])
    room = st.sidebar.multiselect('Select Room Type', room_options, default=['Select All'])

    # Logic to handle "Select All" option
    if 'Select All' in country:
        country = sorted(df['Country'].unique())
    if 'Select All' in prop:
        prop = sorted(df['Property_type'].unique())
    if 'Select All' in room:
        room = sorted(df['Room_type'].unique())

    price = st.slider('Select Price', df['Price'].min(), df['Price'].max(), (df['Price'].min(), df['Price'].max()))

    query = f"Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}"


    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## Price Analysis")
        price_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        price_df['Price'] = price_df['Price'].round(2)
        fig = px.bar(price_df, x='Room_type', y='Price', color='Price', title='Avg Price in each Room type')
        st.plotly_chart(fig, use_container_width=True)

        country_df = df.query(query).groupby('Country', as_index=False)['Price'].mean()
        country_df['Price'] = country_df['Price'].round(2)
        fig = px.scatter_geo(country_df, locations='Country', color='Price', hover_data=['Price'], locationmode='country names', size='Price', title='Avg Price in each Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#   ")
        st.markdown("#   ")

    with col2: 
        st.markdown("## Availability Analysis")
        filtered_df = df.query(query)
        filtered_df = filtered_df.rename(columns={"Availability_365": "Availability"})
        # box plot using Plotly
        fig = px.box(filtered_df, x='Room_type', y='Availability', color='Room_type', title='Availability by Room_type') 
        st.plotly_chart(fig, use_container_width=True)


        country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
        country_df = country_df.rename(columns={"Availability_365": "Availability"})
        country_df['Availability'] = country_df['Availability'].astype(int)
        fig = px.scatter_geo(country_df, locations='Country', color='Availability', hover_data=['Availability'], locationmode='country names', size='Availability', title='Avg Availability in each Country', color_continuous_scale='agsunset')
        st.plotly_chart(fig, use_container_width=True)