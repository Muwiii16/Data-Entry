import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.title("FitTrack")
st.write('Welcome to the "FitTrack" Gym Logger')

if 'session_history' not in st.session_state:
    st.session_state['session_history']=[]

st.subheader("📝 Member Entry")

col1, col2=st.columns(2)

with col1:
    workout_type=st.selectbox("Workout Type",["Cardio","Strength","Yoga","HIIT"])
    dur = st.number_input("Duration", min_value=1, step=1)

with col2:
    customer = st.text_input("Member Name", placeholder="e.g. John Doe")

if st.button("Session Logs", type="primary"):
    # Create a 'Record' (A Python Dictionary)
    new_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Workout type": workout_type,
        "Duration": dur,
        "Customer": customer if customer else "Guest"
    }

    # Save the record to our Session State list
    st.session_state['session_history'].append(new_entry)
    st.success("Session recorded successfully!")

st.divider()
st.subheader("📊 Today's Session Log")

if st.session_state['session_history']:
    # Convert list of dictionaries into a Table
    df = pd.DataFrame(st.session_state['session_history'])

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Bonus: Show a quick metric
    total_time = df['Duration'].sum()
    st.metric("Total Time", f"{total_time:,} min(s)")
else:
    st.write("No data recorded yet. Fill out the form above!")

#Review
def convert_df_to_excel(df):
    # 1. Create the 'Waiting Room' (Buffer)
    output = io.BytesIO()

    # 2. Write the DataFrame to the Buffer using the 'openpyxl' engine
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Daily_Member_Sessions')

    # 3. Go back to the start of the buffer and return the data
    processed_data = output.getvalue()
    return processed_data


st.divider()
st.subheader("💾 Export Data")

if st.session_state['session_history']:
    # Step A: Convert the current history into a DataFrame
    current_df = pd.DataFrame(st.session_state['session_history'])

    # Step B: Convert that DataFrame into Excel bytes
    excel_data = convert_df_to_excel(current_df)

    # Step C: The Streamlit Download Button
    st.download_button(
        label="Download Sales as Excel",
        data=excel_data,
        file_name="daily_member_session_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Add some member sessions first to enable the download button!")

