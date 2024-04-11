# SCRAPER SCRIPT PROJECT
---
### OBJECTIVE
> A script that can run on any Amazon search page.
> The script contains a function that returns the urls on the current search page for:
>    - the cheapest product
>    - the product with the highest rating
>    - the product that arrives the soonest
>
> For example : https://www.amazon.com/s?k=headphones&crid=VS7GDL0WY0ZR&sprefix=headphones%2Caps%2C522&ref=nb_sb_noss_2
---
### PRE-REQUISITES
> Before you begin, ensure you have installed the following libraries:
> 
> - [Beautiful Soup](https://pypi.org/project/beautifulsoup4/): Library for parsing HTML and XML documents.
> - [Requests](https://pypi.org/project/requests/): Library for making HTTP requests.
> - [Regular Expressions](https://docs.python.org/3/library/re.html): Library for working with regular expressions.
> - [Datetime](https://docs.python.org/3/library/datetime.html): Library for working with dates and times.
---
### SCRIPT
> - [AmazonScraperScript](./.venv/AmazonScraper/AmazonScraperScript.py) | Where the script lives
> - [AmazonScraperScriptVideo](https://drive.google.com/file/d/13E3NAViWSBpmEJPYdC7sOD3Bofw4uD06/view) | Video of script in play
---
### EXAMPLE
Running Script prompts:
```
Enter the Amazon search URL:
```
Acceptable URL format starts with `https://www.amazon.com/s?`
Non acceptable URL formats will retry or prompt to exit
```
Enter the Amazon search URL: not acceptable URL
Please enter a valid Amazon Search URL and try again. Or press 'X' to quit:
```
Entering an acceptable URL will provide the following output
```
Enter the Amazon search URL: https://www.amazon.com/s?k=headphones&crid=VS7GDL0WY0ZR&sprefix=headphones%2Caps%2C522&ref=nb_sb_noss_2
Cheapest Product:
	Title: Maxell - 190319 Stereo Headphones - 3.5mm Cord with 6-Foot Length - Soft Padded Ear Cushions, Adjustable Headband for Comfort - Sleek, Lightweight, Wired for Reliable Connection – Black
	URL: PRODUCT_URL
	Price: $6.29
Highest Rated Product:
	Title: Classroom Headphones Bulk 5 Pack, Student On Ear Color Varieties, Comfy Swivel Earphones for Library, School, Airplane, Kids, for Online Learning and Travel, Noise Stereo Sound 3.5mm Jack (Black)
	URL: PRODUCT_URL
	Rating: 4.6
Soonest Available Product:
	Title: Apple EarPods Headphones with Lightning Connector, Wired Ear Buds for iPhone with Built-in Remote to Control Music, Phone Calls, and Volume
	URL: PRODUCT_URL
	Date: Apr 11
	Time Range: 05 PM - 10 PM
```
