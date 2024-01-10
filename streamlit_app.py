import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError


#Pandas used here
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')


#welcome section up top
streamlit.title('My parents new healthy diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')



#Adding pick list so people can select their smoothie ingredients
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page
streamlit.dataframe(fruits_to_show)


##########  Create the function  ##########
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized


####  New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
    fruit_choice = streamlit.text_input('What fruit would you like more information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


#New Section to display fruityvice api response
#streamlit.header("Fruityvice Fruit Advice!")
#try:
#  fruit_choice = streamlit.text_input("What fruit would you like information about?")
#  if not fruit_choice:
 #   streamlit.error("Please select a fruit to get information.")
#  else:
  #  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  #  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  #  streamlit.dataframe(fruityvice_normalized)











#streamlit.write("The user entered", fruit_choice)

#############  Below code moved above into the else statement  #################
#requests being used here
#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


#Take the json version of the response and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output it to the screen as a table
#streamlit.dataframe(fruityvice_normalized)



#Snowflake being used here
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()


streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

#Add a button to load the fruit

if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows) 



#Allow end user to add a fruit to the list
streamlit.header("What would you like to add?")
add_my_fruit = streamlit.text_input("Whatcha thinking")
if streamlit.button('Add a fruit to the list'):
  snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)



