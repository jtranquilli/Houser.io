# Houser.io

To use the service, first run housing_scraper.py from terminal using the command 'python3 housing_scraper.py'. Depending on how many 
listings are available, it may run for up to half an hour, but it will print to the terminal continuously to show how many new
listings it has gathered. Once the program has terminated, the gathered listings will be held in a .db file in your current directory. To view
them through a streamlit web-app, and to be able to sort by price range and number of bedrooms, use the command 'streamlit run hs_frontend.py'.
