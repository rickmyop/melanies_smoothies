# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f"""
    :cup_with_straw: \
    Customise your Smoothie \
    :cup_with_straw:
""")

# option =st.selectbox(
#     'xxx', 
#     ('a', 'b')
# )
# st.write('You selected', option)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = my_dataframe.select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

name_on_order = st.text_input('Name')
st.write(f"The name on your order will be: {name_on_order}")

if ingredient_list:
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

        cnx = st.connection("snowflake")
        session = cnx.session()
