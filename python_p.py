import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(
    page_title="Personal Travel Log",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Header Section ---
st.title("🗺️ Your Personal Travel Log")
st.markdown("""
Welcome to your travel companion! Track your daily journeys, estimate costs, and monitor carbon emissions.
Let's get started with your details.
""")

# --- User Information Section ---
st.header("📝 Your Details")
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("👤 Enter your name:", placeholder="e.g., Alex")
    with col2:
        age = st.number_input("🎂 Enter your age:", min_value=0, max_value=120, value=25)

    col3, col4 = st.columns(2)
    with col3:
        vehicle = st.text_input("🏍️ Enter your bike model:", placeholder="e.g., Shine125, Pulsar 150")
    with col4:
        city = st.text_input("🏙️ Enter your city name:", placeholder="e.g., Mumbai")

    if not all([name, vehicle, city]):
        st.warning("Please fill in all your details above to proceed.")

st.markdown("---") # Separator for visual clarity

# --- Daily Travel Log Section ---
st.header("🗓️ Daily Travel Entries")
st.info("Input your travel details for each day of the week below.")

# Lists to store travel data for summary
daily_data = [] # To store dicts for DataFrame

# Loop through the days of the week
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for i, day in enumerate(days_of_week):
    with st.container(border=True): # Group each day's input in a bordered container
        st.subheader(f"{day} Travel")
        day_visit_status = st.radio(
            f"Did you travel on {day}?",
            ["Yes", "No"],
            key=f"visit_radio_{i}",
            index=1 # Default to 'No' for cleaner initial view
        )

        if day_visit_status == "Yes":
            travel_destination = st.text_input(
                f"🗺️ Where did you travel on {day}?",
                key=f"travel_dest_{i}",
                placeholder="e.g., Office, Market"
            )
            travel_km = st.number_input(
                f"📏 How many km did you travel on {day}?",
                min_value=0.0,
                step=0.1,
                format="%.1f",
                key=f"km_input_{i}"
            )

            if travel_km > 0:
                # Assuming rough estimates for cost and emission
                # These can be made more dynamic based on vehicle type if desired
                km_cost = travel_km * 75  # Rs per km
                km_emission = travel_km * 125 # grams of CO2 per km

                daily_data.append({
                    "Day": day,
                    "Distance (km)": travel_km,
                    "Cost (Rs)": km_cost,
                    "Emissions (g CO2)": km_emission,
                    "Destination": travel_destination
                })
                st.success(f"✅ On {day}, you traveled **{travel_km:.1f} km** to {travel_destination}. Estimated cost: **₹{km_cost:,.2f}**, Carbon emission: **{km_emission:,.2f} g CO2**.")
            else:
                st.warning(f"Please enter a valid distance for {day}.")
        else:
            st.info(f"👍 Good for you! No travel recorded for {day}. Saving money and reducing emissions!")

st.markdown("---")

# --- Summary Section ---
st.header("📊 Travel Summary")

if st.button("Show My Travel Summary", type="primary"):
    if daily_data:
        df_travel = pd.DataFrame(daily_data)

        st.subheader("Your Weekly Travel Overview")

        # Display key metrics
        total_km = df_travel["Distance (km)"].sum()
        total_cost = df_travel["Cost (Rs)"].sum()
        total_emission = df_travel["Emissions (g CO2)"].sum()

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Total Distance", f"{total_km:,.1f} km", delta_color="off")
        with metric_col2:
            st.metric("Total Cost", f"₹{total_cost:,.2f}", delta_color="off")
        with metric_col3:
            st.metric("Total Emissions", f"{total_emission:,.2f} g CO2", delta_color="off")

        st.markdown("---")

        st.subheader("Detailed Daily Breakdown")
        st.dataframe(df_travel.set_index("Day"), use_container_width=True)

        st.markdown("---")

        # Plotting the data
        st.subheader("Visualizing Your Week")

        fig_km = px.bar(
            df_travel,
            x="Day",
            y="Distance (km)",
            title="Kilometers Traveled Per Day",
            labels={"Distance (km)": "Distance (km)", "Day": "Day of the Week"},
            color="Distance (km)",
            color_continuous_scale=px.colors.sequential.Viridis,
            hover_data={"Cost (Rs)": True, "Emissions (g CO2)": True, "Destination": True}
        )
        fig_km.update_layout(xaxis={'categoryorder':'array', 'categoryarray':days_of_week})
        st.plotly_chart(fig_km, use_container_width=True)

        fig_cost = px.pie(
            df_travel,
            names="Day",
            values="Cost (Rs)",
            title="Cost Distribution Per Day",
            hover_data={"Distance (km)": True, "Emissions (g CO2)": True, "Destination": True}
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    else:
        st.warning("No travel data recorded yet. Please fill in some daily entries!")
else:
    st.info("Click the button above to see your travel summary!")

st.markdown("---")
st.caption("Powered by Streamlit ✨")
