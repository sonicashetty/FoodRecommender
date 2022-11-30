import pandas as pd
import streamlit as st
import pickle
import requests
from streamlit_lottie import st_lottie
# BACKGROUND IMAGE
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.theceomagazine.net/wp-content/uploads/2021/07/27153234/Payo_dining-700x467.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()
# TITLE AND ANIME
with st.container():
    st.markdown("<h1 style='text-align: ; color: black;'>Restaurant Dish Recommendation</h1>", unsafe_allow_html=True)

# LOADING ORDERS
order = pickle.load(open("orders.pkl","rb"))

# REGULAR CUSTOMER

with st.container():
    left_column, mid_column, right_column, et_column, ett_column, rt_column  = st.columns([3,1,1,3,1,3])
    with left_column:
        st.markdown("**<h2 style='text-align: center; color: black;'>Regular Customer</h2>**", unsafe_allow_html=True)
        id = order["user_id"].values
        user_id = [*set(id)]
        option = st.selectbox("**Enter your ID**", user_id)

# SHOWING PREVIOUS ORDERS OF REGULAR CUSTOMER
    dishes = order.loc[order['user_id'] == option, 'dish'].tolist()
    if st.button("**Previous Orders**"):
        for i in dishes:
            st.write(i)

# RECOMMENDING DISHES FOR REGULAR CUSTOMERS 
    recommended_dishes = pickle.load(open("recommendations.pkl", "rb"))
    def recommendations(id):
      point =recommended_dishes[recommended_dishes.values == id].values.tolist()
      a1=point[0][2:]
      return a1
    
    if st.button("**Recommendations for you**"):
        recommend = recommendations(option)
        for i in recommend:
            st.write(i)

with et_column:
    st.markdown("**<h2 style='text-align: center; color: black;'>New Customer</h2>**", unsafe_allow_html=True)

    food_list = pickle.load(open('food.pkl', 'rb'))
    data = pd.DataFrame(food_list)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
    
    def recommend(food):
        food_index = data[data["DishName"] == food].index[0]
        distances = similarity[food_index]
        food_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
        recommended_foods = []
        for i in food_list:
            recommended_foods.append(data.iloc[i[0]].DishName)
        return recommended_foods
    
    selected_food = st.selectbox('**What would you like to Order?**', food_list)

    if st.button("**Recommend**"):
        recommendations = recommend(selected_food)
        st.subheader("**Also try this**")
        for i in recommendations:
            st.write(i)

with rt_column:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_rc = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_tll0j4bb.json")
    st_lottie(lottie_rc, height = 100, width = 150, key='Hello')
