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
#create the repeatable codeblock
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#new section to display fruityvice api responses
streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice=streamlit.text_input('Which fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error('Please select a fruit')
  else:
    get_back_from_function=get_fruityvice_data(fruit_choice)
    streamlit.dataframe(get_back_from_function)
except URLerror as e:
  streamlit.error()



streamlit.header("The Fruit-Load-List contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
#add a button
if streamlit.button('Get Fruit Load List'):
    my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_datarow=get_fruit_load_list()
    streamlit.dataframe(my_datarow)
#don't run while troubleshooting
streamlit.stop()
def insert_row_to_snowflake(new_fruit):
        with my_cnx.cursor as my_cur:
            my_cur.execute("insert into fruit load list values ('from streamlit')")
            return "Thanks for adding "+ new_fruit
        
fruit_add=streamlit.text_input('Which fruit would you add?')
if streamlit.button('Add fruit to the list') :
    my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_to_snowflake(fruit_add)
    stream.text(back_from_function)
streamlit.write('Thanks for adding', fruit_add)

my_cur.execute("insert into fruit_load_list values ('streamlit');")
