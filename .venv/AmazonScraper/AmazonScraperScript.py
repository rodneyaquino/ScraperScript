"""
Write a script that can run on any Amazon search page.
The script should contain a function that returns the urls for
    - the cheapest product
    - the product with the highest rating
    - the product that arrives the soonest
on the current search page.
Ex. https://www.amazon.com/s?k=headphones&crid=VS7GDL0WY0ZR&sprefix=headphones%2Caps%2C522&ref=nb_sb_noss_2
"""

# Import necessary libraries
from bs4 import BeautifulSoup  # Library for parsing HTML and XML documents
import requests  # Library for making HTTP requests
import re  # Library for regular expressions
from datetime import datetime, timedelta  # Library for working with dates and times

# Define headers to mimic a browser request
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US, en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',  # Specifies accepted content encodings
    'Connection': 'keep-alive',  # Specifies to keep the connection open
    'Cache-Control': 'no-cache',  # Specifies no caching for the response
    'Pragma': 'no-cache',  # Specifies no caching for the browser
}

def parse_delivery_date(delivery_text):
    """
    Parses the delivery text to extract delivery date, start time, and end time.

    Args:
    - delivery_text (str): Text containing delivery information.

    Returns:
    - tuple: A tuple containing delivery date, start time, and end time.
    """
    # Handling for "Today"
    if 'Today' in delivery_text:  # Check if "Today" is in the delivery text
        today_date = datetime.now()  # Get today's date
        time_match = re.search(r'(\d{1,2} [AP]M) - (\d{1,2} [AP]M)', delivery_text)  # Search for time range
        if time_match:
            start_time_str, end_time_str = time_match.groups()  # Extract start and end times
            start_time = datetime.strptime(start_time_str, '%I %p').time()  # Parse start time
            end_time = datetime.strptime(end_time_str, '%I %p').time()  # Parse end time
            return today_date, start_time, end_time  # Return today's date with time range
        return today_date, None, None  # Return today's date with no specific time range

    # Special handling for "Tomorrow"
    if 'Tomorrow' in delivery_text:  # Check if "Tomorrow" is in the delivery text
        tomorrow_date = datetime.now() + timedelta(days=1)  # Get tomorrow's date
        return tomorrow_date, None, None  # Return tomorrow's date with no specific time range

    # Extract the date from the delivery text
    dates = re.findall(r'(\w{3}, \w{3} \d{1,2})', delivery_text)  # Find all dates in the text
    if dates:
        date_str = dates[-1]  # Use the last date if there are multiple dates
        try:
            date_obj = datetime.strptime(date_str + ' ' + str(datetime.now().year), '%a, %b %d %Y')  # Parse the date
        except ValueError:
            return None, None, None  # Return None if the date format is invalid

        # Adjust for year transition
        today = datetime.now()
        if date_obj < today:
            date_obj = date_obj.replace(year=today.year + 1)  # Increment year if the date is in the past

        # Extract time range if present
        time_match = re.search(r'(\d{1,2} [AP]M) - (\d{1,2} [AP]M)', delivery_text)  # Search for time range
        if time_match:
            start_time_str, end_time_str = time_match.groups()  # Extract start and end times
            start_time = datetime.strptime(start_time_str, '%I %p').time()  # Parse start time
            end_time = datetime.strptime(end_time_str, '%I %p').time()  # Parse end time
            return date_obj, start_time, end_time  # Return date with time range

        return date_obj, None, None  # Return date with no specific time range
    return None, None, None  # Return None if no delivery date is found

def get_amazon_search_results(url):
    """
    Retrieves Amazon search results based on the provided URL.

    Args:
    - url (str): URL of the Amazon search page.

    Returns:
    - dict: A dictionary containing details of the cheapest, highest-rated, and soonest available products.
    """
    # Send an HTTP GET request to the specified URL with custom headers
    response = requests.get(url, headers=HEADERS)
    # Check if the request was successful (status code 200 indicates success)
    if response.status_code != 200:
        return "Request was not successful."  # Return an error message if the request was not successful

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all products on the current page using BeautifulSoup's find_all() method
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Get today's date
    today = datetime.now().date()

    # Initialize variables for cheapest, highest-rated, and soonest available products
    cheapest_product = None
    highest_rated_product = None
    soonest_product = None
    lowest_price = float('inf')
    highest_rating = 0.0

    # Loop through each product found on the page
    for product in products:
        try:

            # Extract product title
            title_element = product.find('span', {'class': 'a-size-medium'}) or product.find('span', {
                'class': 'a-size-base-plus'})
            title = title_element.text.strip() if title_element else None

            # Extract URL
            url_suffix = product.find('a', {'class': 'a-link-normal'})['href']
            full_url = f"https://www.amazon.com{url_suffix}"

            # Extract price
            price_str = product.find('span', {'class': 'a-offscreen'}).text.replace('$', '').replace(',', '').strip()
            price = float(price_str)

            # Extract rating
            rating_element = product.find('span', {'class': 'a-icon-alt'})
            rating = float(rating_element.text.split()[0]) if rating_element else None

            # Extract delivery info
            delivery_info_elements = product.find_all('span', class_="a-color-base a-text-bold")
            earliest_delivery_date = None
            start_time = None
            end_time = None

            # Loop through each delivery info element
            for element in delivery_info_elements:

                # Extract delivery text
                delivery_text = element.text.strip()

                # Parse delivery date, start time, and end time from the delivery text
                date_obj, start, end = parse_delivery_date(delivery_text)
                if date_obj:

                    # Determine the soonest available product based on delivery date
                    if not earliest_delivery_date or date_obj < earliest_delivery_date:

                        # If no earliest delivery date or current date is earlier, update variables
                        earliest_delivery_date = date_obj
                        start_time = start
                        end_time = end

                    # If delivery date is the same but earlier time, update variables
                    elif date_obj == earliest_delivery_date and start and end:
                        if not start_time or (start and end and start < start_time):
                            start_time = start
                            end_time = end

            # Update variables for cheapest, highest-rated, and soonest available products
            if price < lowest_price:

                # Update cheapest product if current price is lower
                lowest_price = price
                cheapest_product = (title, full_url, price)

            # Update highest-rated product if current rating is higher
            if rating and rating > highest_rating:
                highest_rating = rating
                highest_rated_product = (title, full_url, rating)
            if earliest_delivery_date:
                # Update soonest available product if there is an earliest delivery date
                if not soonest_product or earliest_delivery_date < soonest_product[2]:
                    # If no soonest product or current delivery date is earlier, update variables
                    soonest_product = (title, full_url, earliest_delivery_date, start_time, end_time)
                elif earliest_delivery_date == soonest_product[2]:
                    # If delivery date is the same but earlier time, update variables
                    if start_time and end_time and soonest_product[3] and soonest_product[4]:
                        if start_time < soonest_product[3] or (
                                start_time == soonest_product[3] and end_time < soonest_product[4]):
                            soonest_product = (title, full_url, earliest_delivery_date, start_time, end_time)
        except Exception as e:
                continue  # Continue to the next product if an error occurs

    # Return a dictionary containing details of the cheapest, highest-rated, and soonest available products
    return {
        "Cheapest Product": cheapest_product,
        "Highest Rated Product": highest_rated_product,
        "Soonest Available Product": soonest_product
    }

def verify_amazon_search_url(url):
    """
    Verifies if the provided URL is a valid Amazon search URL.

    Args:
    - url (str): The URL to be verified.

    Returns:
    - bool: True if the URL is a valid Amazon search URL, False otherwise.
    """
    return url.startswith("https://www.amazon.com/s?")

# Prompt the user to enter the Amazon search URL
while True:
    url = input("Enter the Amazon search URL: ").strip().lower()
    if url == 'x':
        print("Exiting program.")
        exit()
    elif verify_amazon_search_url(url):
        break
    else:
        choice = input("Please enter a valid Amazon Search URL and try again. Or press 'X' to quit: ").strip().lower()
        if choice == 'x':
            print("Exiting program.")
            exit()

# Get Amazon search results based on the provided URL
results = get_amazon_search_results(url)

# Check if the results are a string (indicating an error) or a dictionary (indicating success)
if isinstance(results, str):
    # Print the error message if the results are a string
    print(results)
else:
    # Print details of the cheapest, highest-rated, and soonest available products
    for key, value in results.items():
        if value:
            if key == "Soonest Available Product":
                print(f"{key}:")
                print(f"\tTitle: {value[0]}")
                print(f"\tURL: {value[1]}")
                print(f"\tDate: {value[2].strftime('%b %d')}")
                print(
                    f"\tTime Range: {value[3].strftime('%I %p')} - {value[4].strftime('%I %p')}" if value[3] and value[
                        4] else "")
            elif key == "Cheapest Product":
                print(f"{key}:")
                print(f"\tTitle: {value[0]}")
                print(f"\tURL: {value[1]}")
                print(f"\tPrice: ${value[2]:.2f}")
            else:
                print(f"{key}:")
                print(f"\tTitle: {value[0]}")
                print(f"\tURL: {value[1]}")
                if key == "Highest Rated Product":
                    print(f"\tRating: {value[2]}")
        else:
            print(f"{key}: None")