!pip install streamlit-option-menu 
!pip nstall psycopg2
!pip install python-dotenv

import streamlit as st
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
#import database_conn as db
from database_conn import connect_to_database, close_database_connection, insert_flight_details,insert_airport_details,insert_aircraft_details,fetch_table_data


#settings
page_title = "AIRQUEST"
page_icon = ":airplane:"
layout = "centered"

# setting up page title
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
# # Set background image using local file path
# background_image_path = '/Users/abhijit/Desktop/BUFFALO/SEM-2/DMQL/PROJECT/web_app/background_image.jpeg' 

# # Embed local image file in CSS for background
# st.markdown(
#     f"""
#     <style>
#     .reportview-container {{
#         background-image: url('{background_image_path}');
#         background-size: cover;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.title(" " + page_icon + " " + page_title + " " + page_icon)

# NAVIGATION BAR

nav_bar = option_menu(
    menu_title=None,
    options=["Flight Details","Airport Details","Aircraft Details","Busiest Airports","Flight Revenue"],
    icons=["pencil_fill","pencil_fill","pencil_fill", "pencil_fill","pencil_fill"],
    orientation="horizontal",
)

# Dropdown values for flight entry
airport_code_flight = ["JFK","SFO","REN","KXK","IKT","TBW","AER","NBC","KRR","PKC","NYA","EGO","KLF","VKT","GOJ","GRV","RTW","URS",
           "YKS","UUS","VOG","LED","SLY","NJC","OGZ","UKX","KUF","MCX","CEE","OSW","UIK","UUD","MQF","KJA",
           "KGD","BZK","CNN","IAR","SVX","KZN","USK","ABA","BQS","UUA","PEZ","SWT","MJZ","MMK","KVX","ULY",
           "DME","MRV","RGK","ARH","PEE","PYJ","BTK","CSY","GDZ","KRO","EYK","OMS","ROV","UCT","VOZ","PES",
           "ULV","DYR","KYZ","SCW","VKO","URJ","LPK","BAX","KEJ","ASF","VVO","KHV","NUX","TOF","NNM","NFG",
           "AAQ","OVB","NYM","STW","TJM","GDX","KGP","OVS","UFA","SVO","IJK","HTA","IWA","NOJ","JOK","SKX",
           "HMA","NOZ","NAL","ESL","NSK","PKV","SGC","CEK"]

status = ["On Time","Departed","Arrived","Cancelled","Delayed","Scheduled"]

aircraft_code_flight = ["CN1","CR2","763","773","319","733","SU9","321"]

#helper functions
def generate_timestamp_with_timezone(timestamp, timezone):
    dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    tz = pytz.timezone(timezone)
    timestamp_timezone = tz.localize(dt)
    return timestamp_timezone

# flight details form
if nav_bar == "Flight Details":
    st.header(f"Flight Details")
    with st.form("flight_form", clear_on_submit=True):

        flight_id = st.text_input(label="Flight ID:", value="")
        flight_no = st.text_input(label="Flight No:", value="")

        # departure and arrival airports
        da, aa = st.columns(2)
        departure_airport = da.selectbox("Departure Airport:", airport_code_flight, key = "departure_airport" )
        arrival_airport = aa.selectbox("Arrival Airport:", airport_code_flight, key = "arrival_airport" )

        #flight status 
        flight_status = st.selectbox("Flight Status:", status, key = "flight_status" )

        #aircraft code
        aircraft_code = st.selectbox("Aircraft Code:", aircraft_code_flight, key = "aircraft_code" )

        departure_time, arrival_time = st.columns(2)

        departure_timestamp = 0
        arrival_timestamp = 0

        
        #departure time
        with departure_time.expander("Departure Time"):
            timestamp_dept = st.text_input("Enter timestamp(YYYY-MM-DD HH:MM:SS ):", key = "timestamp_dept")
            timezone_dept = st.selectbox("Select timezone:", pytz.all_timezones, key = "timezone_dept")
            if timestamp_dept:
                try:
                    departure_timestamp = generate_timestamp_with_timezone(timestamp_dept, timezone_dept)
                    st.write("Departure time:", departure_timestamp)
                except ValueError:
                    st.error("Invalid timestamp format. Please use YYYY-MM-DD HH:MM:SS format.")

        #arrival time
        with arrival_time.expander("Arrival Time"):
            timestamp_arr = st.text_input("Enter timestamp(YYYY-MM-DD HH:MM:SS ):",key = "timestamp_arr")
            timezone_arr = st.selectbox("Select timezone:", pytz.all_timezones, key = "timezone_arr")
            if timestamp_arr:
                try:
                    arrival_timestamp = generate_timestamp_with_timezone(timestamp_arr, timezone_arr)
                    st.write("Arrival time:", arrival_timestamp)
                except ValueError:
                    st.error("Invalid timestamp format. Please use YYYY-MM-DD HH:MM:SS format.")

        "---"
        flight_submit = st.form_submit_button("Save Flight")

        if flight_submit:
            st.write("Flight id:",flight_id)
            st.write("flight no:", flight_no)
            st.write("flight_status:", flight_status)
            st.write("aircraft_code:", aircraft_code)
            st.write("departure_timestamp", departure_timestamp)
            st.write("arrival_timestamp", arrival_timestamp)
            st.write("departure_airport:", departure_airport)
            st.write("arrival_airport:", arrival_airport)
            #connect to database
            conn = connect_to_database()
            if conn is None:
                st.error("Failed to connect to the database.")
            else:
                # Save flight details to the database
                if insert_flight_details(conn, flight_id, flight_no, flight_status, aircraft_code, departure_timestamp, arrival_timestamp, departure_airport, arrival_airport):
                    st.success("Flight details saved!")
                else:
                    st.error("Failed to save flight details. Please try again later.")

            # Close the database connection
            close_database_connection(conn)


# Airport Details form
if nav_bar == "Airport Details":
    st.header(f"Airport Details")   
    with st.form("airports_form", clear_on_submit=True):
        airport_code = st.text_input(label="Airport Code:", value="")
        airport_name = st.text_input(label="Airport Name:", value="")
        city = st.text_input(label="City:", value="")
        airport_timezone = st.selectbox("Select timezone:", pytz.all_timezones, key = "airport_timezone")

        "---"
        airport_submit = st.form_submit_button("Save Airport")
        if airport_submit:
            st.write("Airport code:",airport_code)
            st.write("Airport name:", airport_name)
            st.write("City:", city)
            st.write("airport timezone:", airport_timezone)
            #connect to database
            conn = connect_to_database()
            if conn is None:
                st.error("Failed to connect to the database.")
            else:
                # Save flight details to the database
                if insert_airport_details(conn, airport_code, airport_name, city, airport_timezone):
                    st.success("Airport details saved!")
                else:
                    st.error("Failed to save airport details. Please try again later.")

            # Close the database connection
            close_database_connection(conn)

# Aircrafts Details form
if nav_bar == "Aircraft Details":
    st.header(f"Aircraft Details")   
    with st.form("aircrafts_form", clear_on_submit=True):
        aircraft_code = st.text_input(label="Aircraft Code:", value="")
        model = st.text_input(label="Aircraft Model:", value="")
        range = st.text_input(label="Range:", value="")

        "---"
        aircraft_submit = st.form_submit_button("Save Aircraft")
        if aircraft_submit:
            st.write("Aircraft Code:",aircraft_code)
            st.write("Aircraft Model:", model)
            st.write("Range:", range)
            #connect to database
            conn = connect_to_database()
            if conn is None:
                st.error("Failed to connect to the database.")
            else:
                # Save flight details to the database
                if insert_aircraft_details(conn, aircraft_code, model, range):
                    st.success("Aircraft details saved!")
                else:
                    st.error("Failed to save aircraft details. Please try again later.")

            # Close the database connection
            close_database_connection(conn)


# busiest airports
if nav_bar == "Busiest Airports":
    st.header(f"Busiest Airports")
    with st.form("busy_airport_form", clear_on_submit=True):
        limit = st.number_input("Enter the number of airports to display:", min_value=1, max_value=None, value=10, step=1)

        dept_airport_submit = st.form_submit_button("Get Departure Stats")
        if dept_airport_submit:
            # Retrieve data from the database
            query = f"""
            SELECT ad.airport_name, COUNT(*) AS num_departures
            FROM flights f
            JOIN airports_data ad ON f.departure_airport = ad.airport_code
            GROUP BY ad.airport_name
            ORDER BY num_departures DESC
            LIMIT {limit};
            """
            df = fetch_table_data(query)

            if df is not None:
                # Display the data table
                st.write("Top Departure Airports:")
                st.dataframe(df)

                # Plot the visual graph
                st.write("Visual Graph:")
                st.bar_chart(df.set_index('airport_name'))

        arr_airport_submit = st.form_submit_button("Get Arrival Stats")
        if arr_airport_submit:
            # Retrieve data from the database
            query = f"""
            SELECT ad.airport_name, COUNT(*) AS num_arrivals
            FROM flights f
            JOIN airports_data ad ON f.arrival_airport = ad.airport_code
            GROUP BY ad.airport_name
            ORDER BY num_arrivals DESC
            LIMIT {limit};
            """
            df = fetch_table_data(query)

            if df is not None:
                # Display the data table
                st.write("Top Arrival Airports:")
                st.dataframe(df)

                # Plot the visual graph
                st.write("Visual Graph:")
                st.bar_chart(df.set_index('airport_name'),color='#00ff00')


# flight revenue
if nav_bar == "Flight Revenue":
    st.header(f"Flight Revenue")
    with st.form("flight_revenue_form", clear_on_submit=True):
        limit = st.number_input("Enter the number of flights to display:", min_value=1, max_value=None, value=10, step=1)

        dept_airport_submit = st.form_submit_button("Get Flight Revenue")
        if dept_airport_submit:
            # Retrieve data from the database
            query = f"""
            SELECT f.flight_no, SUM(ft.amount) AS total_revenue
            FROM flights f
            JOIN ticket_flights ft ON f.flight_id = ft.flight_id
            GROUP BY f.flight_no
            ORDER BY total_revenue DESC
            LIMIT {limit};
            """
            df = fetch_table_data(query)

            if df is not None:
                # Display the data table
                st.write("Top Revenue Flights:")
                st.dataframe(df)

                # Plot the visual graph
                st.write("Visual Graph:")
                st.bar_chart(df.set_index('flight_no'), color='#800080')
