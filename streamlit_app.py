import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError
streamlit.title('My mom\'s healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list)

#let's put a pick-list here
fruits_selected=streamlit.multiselect("Pick some Fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
#display the table
streamlit.dataframe(fruits_to_show)

#new section to display fruityvice api responses
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice=streamlit.text_input('Which fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error('Please select a fruit')
  else:
    streamlit.write('The User entered ', fruit_choice)
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    streamlit.text(fruityvice_response.json())
    #take the json version of the response and normalize it
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

#don't run while troubleshooting
streamlit.stop()


my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_datarow=my_cur.fetchall()
streamlit.header("The Fruit-Load-List contains:")
streamlit.dataframe(my_datarow)
fruit_add=streamlit.text_input('Which fruit would you add?')
streamlit.write('Thanks for adding', fruit_add)

my_cur.execute("insert into fruit_load_list values ('streamlite');")
