import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.title("My First Data App")
st.write("Welcome to the Coffee Sales Logger!")

if 'sales_history' not in st.session_state:
    st.session_state['sales_history']=[]

st.subheader("📝 New Sale Entry")

col1, col2=st.columns(2)

with col1:
    item=st.selectbox("Product",["Espresso","Latte","Flat White","Long Black"])
    qty = st.number_input("Quantity", min_value=1, step=1)

with col2:
    price = st.number_input("Unit Price ($)", min_value=0.0, value=4.50)
    customer = st.text_input("Customer Name (Optional)", placeholder="e.g. John Doe")

if st.button("Log Transaction", type="primary"):
    # Create a 'Record' (A Python Dictionary)
    new_entry = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Product": item,
        "Quantity": qty,
        "Price": price,
        "Total": qty * price,  # This is "calculated" data!
        "Customer": customer if customer else "Guest"
    }

    # Save the record to our Session State list
    st.session_state['sales_history'].append(new_entry)
    st.success("Transaction recorded successfully!")

st.divider()
st.subheader("📊 Today's Transaction Log")

if st.session_state['sales_history']:
    # Convert list of dictionaries into a Table
    df = pd.DataFrame(st.session_state['sales_history'])

    # Display the table
    st.dataframe(df, use_container_width=True)

    # Bonus: Show a quick metric
    total_revenue = df['Total'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")
else:
    st.write("No data recorded yet. Fill out the form above!")

#Review
def convert_df_to_excel(df):
    # 1. Create the 'Waiting Room' (Buffer)
    output = io.BytesIO()

    # 2. Write the DataFrame to the Buffer using the 'openpyxl' engine
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Daily_Sales')

    # 3. Go back to the start of the buffer and return the data
    processed_data = output.getvalue()
    return processed_data


st.divider()
st.subheader("💾 Export Data")

if st.session_state['sales_history']:
    # Step A: Convert the current history into a DataFrame
    current_df = pd.DataFrame(st.session_state['sales_history'])

    # Step B: Convert that DataFrame into Excel bytes
    excel_data = convert_df_to_excel(current_df)

    # Step C: The Streamlit Download Button
    st.download_button(
        label="Download Sales as Excel",
        data=excel_data,
        file_name="daily_espresso_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Add some sales data first to enable the download button!")

