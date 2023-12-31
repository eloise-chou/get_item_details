import streamlit as st
from datetime import datetime
import pandas as pd
# import model.validate
from model.data_handle import df_column_to_item_details
import model.file

### Read file
st.header("Get item details")
st.caption("Please upload the csv file, colunms titles = [shop_id, item_id]")
input_csv_file =  st.file_uploader("File：", type = 'csv', help= "Please upload the csv file, colunms titles = [shop_id, item_id]")


### Display table
if input_csv_file is not None:
    df = pd.read_csv(input_csv_file)
    unique_df = df.drop_duplicates(subset = ['shop_id', 'item_id'])
    unique_df = unique_df.reset_index(drop = True)

    st.write(unique_df)

### Select country
api_url_options = {
    "TW": "https://shopee.tw/api/v4/pdp/get_pc",
    "SG": "https://shopee.sg/api/v4/pdp/get_pc",
    "MY": "https://shopee.my/api/v4/pdp/get_pc",
}

selected_country = st.selectbox("Select Country:", list(api_url_options.keys()))
selected_api = api_url_options[selected_country]

### Button -> Fetch and Check 

if st.button("Check"):
    fetched_df = unique_df.copy()

    total_num = len(fetched_df)
    df_fetch_progress_bar = st.progress(0, text="Processing Progress")

    combined_data = pd.DataFrame()

    for i, row in fetched_df.iterrows():
        percent_complete = (i+1) / total_num
        current_item_id = row['item_id']
        df_fetch_progress_bar.progress(percent_complete, text= f"Processing Progress：{current_item_id:,}" )

        item_details = df_column_to_item_details(row, selected_api)
        item_df = pd.DataFrame(item_details)
        combined_data = pd.concat([combined_data, item_df], ignore_index = True)

## Display new table

    fetched_df = combined_data
    fetched_df 



### 下載 Logger 報告

    today_date = datetime.today().strftime('%Y-%m-%d %H-%M-%S')
    st.download_button(
        label       = "Download Product Check Report",
        data        = model.file.df_to_csv_utf8(fetched_df),
        file_name   = f"{today_date}_checked.csv",
        mime        = 'text/csv'
    )