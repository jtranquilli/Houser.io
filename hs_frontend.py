import streamlit as st
import sqlite3
import pandas as pd

class FacebookPost(object):
    def __init__(self, post_text: str, price: int, image_url: str, post_id: str, number_of_rooms: int, user_ID: str):
      self.post_text = post_text
      self.price = price
      self.image_url = image_url
      self.post_id = post_id
      self.number_of_rooms = number_of_rooms
      self.user_ID = user_ID


dbfile = '/Users/juliustranquilli/desktop/COMP/posts.db'

# Create a SQL connection to our SQLite database
conn = sqlite3.connect(dbfile)

df = pd.read_sql_query("SELECT * FROM posts", conn) #convert into a pandas dataframe

#print(df.iloc[0]['post_text'])

st.set_page_config(page_title="Montreal Housing Source TEST", layout = "wide")

st.subheader('''Here you will find postings extracted from a handful of online sources''')
st.subheader('''
They have been reformatted into a standardized listing and compiled on the same page. The service is free to use. ''')

bedroom_selection = st.sidebar.selectbox('Bedrooms', ('1', '2', '3', '4', '5'))


with st.sidebar:
    values = st.slider(
        'Select a range of values',
        0, 4000, (0, 1000), step=1)
    

    
    

num_rows = df[df.columns[0]].count()

#now we want to convert each row in the dataframe into a FacebookPost object


postList = []

for i in range (0,num_rows-1):
    current_row = df.iloc[i]
    current_text = current_row['post_text']
    current_price = current_row['price']
    current_imgURL = current_row['image_url']
    current_PID = current_row['post_id']
    current_bedrooms = current_row['number_of_rooms']
    curr_userID = current_row['user_id']
    temp = FacebookPost(current_text, current_price, current_imgURL, current_PID, current_bedrooms,curr_userID)
    postList.append(temp)



# Now we want to reorganize postList so that it contains tuples of 3 facebook posts

def populate(lower_bound, upper_bound, num_rooms):
    # takes the upper and lower bounds of price limit and the number of rooms
    i = 0
    postListTriples = []

    while i < len(postList)-1:
        temp = []
        
        if(postList[i].price in range(lower_bound,upper_bound)): # and postList[i].number_of_rooms == num_rooms):
            temp.append(postList[i])
            if(len(temp) == 3):
                postListTriples.append(temp) #if this triple is already full, add it to list and reset it to blank
                temp = []
        if i + 1 <= len(postList)-1:
            if(postList[i+1].price in range(lower_bound,upper_bound)): #and postList[i+1].number_of_rooms == num_rooms):
                temp.append(postList[i+1])
                if(len(temp) == 3):
                    postListTriples.append(temp) #if this triple is already full, add it to list and reset it to blank
                    temp = []
        if i + 2 <= len(postList)-1:
            if(postList[i+2].price in range(lower_bound,upper_bound)): # and postList[i+2].number_of_rooms == num_rooms):
                temp.append(postList[i+2])
                if(len(temp) == 3):
                    postListTriples.append(temp) #if this triple is already full, add it to list and reset it to blank
                    temp = []
        
        if(i + 2 >= len(postList)-2): #i+2 is the last posting, add this triplet to list even if its partly empty
            if len(temp)>0:
                postListTriples.append(temp)
        
        i+=3

    columnList = []
    j = 0
    # Now we have a postList with all posts contained within it in the format of FacebookPost objects
    for postTriple in postListTriples:
        col1, col2, col3 = st.columns(3)
        columnList.append(col1)
        columnList.append(col2)
        columnList.append(col3) 
        with col1:
            st.header('$' +  str(postTriple[0].price))
            try:       
                st.image(postTriple[0].image_url)
                
            except:
                pass
            
            st.write(postTriple[0].post_text)
            
            with st.expander("Contact poster"):
                
                st.write("https://www.facebook.com/profile.php?id=" + postTriple[0].user_ID)
            
            
        if len(postTriple) > 1:
            with col2:
                st.header('$' + str(postTriple[1].price))
                try:
                    st.image(postTriple[1].image_url)
                except:
                    pass
                
                st.write(postTriple[1].post_text)
                
                with st.expander("Contact poster"):
                
                    st.write("https://www.facebook.com/profile.php?id=" + postTriple[0].user_ID)
            
        if len(postTriple) == 3:
            with col3:
                st.header('$' + str(postTriple[2].price))
                try:
                    st.image(postTriple[2].image_url)
                except:
                    pass
                st.write(postTriple[2].post_text)
                
                with st.expander("Contact poster"):
                
                    st.write("https://www.facebook.com/profile.php?id=" + postTriple[0].user_ID)
 
#At this point the page has been created with all listings being shown

# get bedrooms from bedroom_selection
# get price range from values
        
upper_bound = values[1]
lower_bound = values[0]
num_rooms = bedroom_selection

#print(upper_bound, lower_bound, num_rooms)

populate(lower_bound, upper_bound, num_rooms)


   
