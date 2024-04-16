# IMPORTING NECESSARY LIBRARIES
import mysql.connector as sql

# IMPORT LOCAL MODULES
import Scripts.sql_script as sql
import Scripts.streamlit_functions as st

# CONNECT DATABASE
cursor, mydb = sql.connect_database()

# SETTING PAGE CONFIGURATIONS
st.set_page_config()

# CREATING OPTION MENU
selected = st.create_option_menu()

if selected == "Home":
    st.home(cursor, mydb)

if selected == "Insert":
    st.insert(cursor, mydb)

if selected == "Analysis":
    st.analysis(cursor, mydb)

if selected == "About":
    st.about()
