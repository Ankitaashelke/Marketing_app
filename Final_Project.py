import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import requests
import seaborn as sns


#setting the icon
st.set_page_config(page_icon=":moneybag:")


#calculating most sales in the city

def most_sales_cities(dataframe, category):
    city_sales =dataframe[dataframe['Category'] ==category].groupby('ship-city')['Quantity'].sum()

    sorted_cities= city_sales.sort_values(ascending=False)
    return sorted_cities.index[:3].tolist()


def marketing_formats(dataframe,category):

    marketing_formats= dataframe[dataframe['Category']== category]['Marketing Channel'].value_counts()

    return marketing_formats.idxmax()

def main():
    
    st.title("Marketing via analysis")

    st.write("Welcome to the sales analysis tool!")

    file_url ='https://raw.githubusercontent.com/Ankitaashelke/Marketing_app/master/Week11_dataset.csv'
    content= requests.get(file_url).content
    df =pd.read_csv(io.StringIO(content.decode('utf-8')))


    content= requests.get(file_url).content
    df =pd.read_csv(io.StringIO(content.decode('utf-8')))

    df['Date']= pd.to_datetime(df['Date'])
    df['Month']= df['Date'].dt.strftime('%B')  

    st.subheader("Data sample: ")

    st.dataframe(df.head(10))

    categories =df['Category'].unique()
    selected_category =st.selectbox("Select a product category:", categories)

    if st.button("Show Details") :

        most_sales_cities_list =most_sales_cities(df, selected_category)

        marketing_format= marketing_formats(df, selected_category)
        
        st.write(f"{selected_category} has most sales in these cities: {', '.join(most_sales_cities_list)}.")

        st.write(f"{selected_category} was sold more through {marketing_format} ")

        # Displaying Average Rating and Total Sales
        filtered_df =df[df['Category']== selected_category]  

        average_rating= round(filtered_df["Rating"].mean(), 1)

        total_sales =filtered_df["Amount"].sum()
        
        st.write(f"Average Rating: {average_rating}")
        st.write(f"Total Sales: INR {total_sales:,}")

    if st.button("Show More"):
        top_months =df[df['Category'] == selected_category].groupby('Month')['Quantity'].sum().nlargest(10)
        
        fig, ax =plt.subplots()

        sns.barplot(x=top_months.values, y=top_months.index, palette='viridis', ax=ax)

        ax.set_title(f'Top Months with Highest Sales for {selected_category}')
        ax.set_xlabel('Total Sales')
        ax.set_ylabel('Month')


        st.pyplot(fig)

    

if __name__ == "__main__":
    main()
