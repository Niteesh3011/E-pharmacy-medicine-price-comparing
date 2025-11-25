import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
from serpapi import GoogleSearch
def compare_prices(med_name):
    # Ensure google-search-results is available (lazy import / install)

    params = {
    "engine": "google_shopping",
    "q": med_name,
    "location": "India",
    "api_key": '798199a57abcb268d9eb5722f6ac84fd93431d6e3a13726a67c00c19f7475611'
    
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get('shopping_results', [])
    return shopping_results



c1, c2 = st.columns(2)
c1.image('image.webp',width=200)
c2.header("E-Pharmacy Comparison System")


st.sidebar.title('Enter the Name of Medicine: ')
med_name = st.sidebar.text_input('Enter The Medicine Name👇: ') 
quantity = st.sidebar.text_input('Enter The Quantity👇: ')

medicine_comp = []
med_price = []


if med_name is not None:
    if st.sidebar.button('Price Compare'):
        
        shopping_results = compare_prices(med_name)
        lowest_price = shopping_results[0].get('price')[1:]
        lowest_price_index = 0
        lowest_price = float(str(lowest_price).replace(',',''))
        print(lowest_price)

        for i in range(len(shopping_results)):
            current_price = shopping_results[i].get('price')[1:]
            current_price = float(str(current_price).replace(',',''))
            
            
            medicine_comp.append(shopping_results[i].get('title', 'N/A'))
            med_price.append(shopping_results[i].get('price', 'N/A')[1:])
            
            
            #--------------------------------------------------------------------------------
            st.title(f"Result {i+1}:")
            c1,c2,c3 = st.columns(3)
            c1.write('Company Name:')
            c2.write(shopping_results[i].get('title', 'N/A'))
            
            c1.write('Price:')
            c2.write(shopping_results[i].get('price', 'N/A'))
            
            c1.write('Source:')
            c2.write(shopping_results[i].get('source', 'N/A'))
            
            url = shopping_results[i].get("product_link","N/A")
            c1.write('Product Link:')
            c2.write('[Link](%s)'%url)
            
            c3.image(shopping_results[i].get('thumbnail','N/A'),width=200)
            st.write('---')
            
            
            if (current_price < lowest_price):
                lowest_price = current_price
                lowest_price_index = i
                
        #------------------------------------------------------------------------------
        st.title(f"Best option:")
        c1,c2,c3 = st.columns(3)
        c1.write('Company Name:')
        c2.write(shopping_results[lowest_price_index].get('title', 'N/A'))
            
        c1.write('Price:')
        c2.write(shopping_results[lowest_price_index].get('price', 'N/A'))
            
        c1.write('Source:')
        c2.write(shopping_results[lowest_price_index].get('source', 'N/A'))
            
        url = shopping_results[lowest_price_index].get("product_link","N/A")
        c1.write('Product Link:')
        c2.write('[Link](%s)'%url)
        
        c3.image(shopping_results[lowest_price_index].get('thumbnail','N/A'),width=200)
        st.write('---------------------------------------------------------------------')        
        
        # Graphical Representation
        st.title('Graphical Representation: ->')
        df = pd.DataFrame(medicine_comp,med_price).reset_index()
        df.columns = ['price','company']
        st.title('\n Chart Representation of Medicine Prices from Different E-Pharmacies')
        st.bar_chart(data=df, y='price',x = 'company')
        
        
        
        fig, ax = plt.subplots(figsize=(18,18))
        
        ax.pie(med_price,labels=medicine_comp,autopct='%1.1f%%',shadow=True)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
        


        