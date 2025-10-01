# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f"""
    :cup_with_straw: \
    Customise your Smoothie \
    :cup_with_straw:
""")


cnx = st.connection("snowflake")
session = cnx.session()

# name section
name_on_order = st.text_input('Name on order:')
st.write(f"The name on your order will be: {name_on_order}")

# selection section
my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = my_dataframe.select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)


if ingredient_list:

    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/watermelon"
    )
    nut_df = st.dataframe(
        data=st.text(smoothiefroot_response.json()),
        use_container_width=True
    )
    
    # st.write(ingredient_list)
    ingredient_str = ' '.join(ingredient_list)
    # st.write(ingredient_str)

    my_insert_stmt = f"""
        insert into
            smoothies.public.orders(name_on_order, ingredients)
        values
            ('{name_on_order}', '{ingredient_str}')
    """

    time_to_submit = st.button('Submit')

    if time_to_submit:
        # st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
