Hello! Thank you for taking the time rereview my program!

Python version: 3.8.10

Libraries used: Json, requests, BeautifulSoup, Datetime

---------Install Instructions-----------

1) activate env 
>>> source env bin activate

2) install requirements from requirements.txt
>>> pip install -r requirements.txt


--------First Utility: JSON file info----------
This utility provides JSON data for inputted forms. 
In order to get user input, prompts are given through the terminal.

In order to limit query time the form name is put into a query version of the 
url given in the take home challenge.

JSON data is printed in the command line. There is also an option 
to save JSON file to a folder called saved-JSON

____Run instructions_____

1) run the findForms.py
>> python3 findForms.py

2) Enter json to call create_json function:
>> Enter json to get json data or pdf to get download pdfs!
json

3) insert form names in this format:
Form W-2, Form W-9, Form 1095-C  ----->>> must be separated by commas <<<-----

***not case sensitive or space sensitive but it will affect file name if saved
4) JSON will be printed. You will then be prompted if you want to save it ((y,yes), (n, no))

5) If yes, file will be saved in saved-JSON



--------Second Utility: Download PDF ---------
This utility downloads PDF files for a range of years. 
In order to get user input, prompts are given through the terminal. 
In order to limit query time the form name is put into a query version of the 
url given in the take home challenge.

Before the user input their ranges, the form they input is queried and the years
ranges available are given to user.


____Run instructions_____

1) run the findForms.py
>> python3 findForms.py

2) enter pdf to start download_pdf function
>> Enter json to get json data or pdf to get download pdfs!
pdf

3) enter form name in this format:
>> Publ 1 ----->>> Not case sensitive <<<-----

4) PDF will be dowloaded to saved-PDF folder.

   
