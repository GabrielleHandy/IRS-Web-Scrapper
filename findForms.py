import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup



def download_pdf():
    """Function that downloads pdfs in desired years"""
    form = get_form("pdf")
    print(f"*******Searching for {form}!*************")
    print("\n")
    results = search_website(form)
    
    if not results:
        print(f"Couldn't find results for {form}. Be mindful of spacing and spelling.")
        quit()
    else: 
        all_pdfs = get_year_ranges(results, form)
        if not all_pdfs:
            quit()
    
    years = get_desired_years()

    pdf_min_year = int(years[0].strip())
    pdf_max_year = int(years[1].strip())

    save(results = all_pdfs, format_type = "pdf", form_name = form, min_year = pdf_min_year, max_year = pdf_max_year)
    quit()


def create_json():
    """Creates json filled with information based on form names inputted"""
    forms = get_form("json")
    print("Searching for results.....\n")
    print("\n")
    # holds info for each form query --this will be dumped into a JSON file in the end--
    result_list = []
    

    # goes through each form and starts a query
    for form in forms:
        # stores info such as name, title, min year, max year
        data = {}
        results = search_website(form)
        if results:
            for result in results:
                form_title = result.find('td', class_ = "MiddleCellSpacer").get_text(strip = True)
                year = int(result.find('td', class_ = "EndCellSpacer").get_text(strip = True))
                
                if "form_number" in data:
                    # checks each year to see if it is min or max year
                    if year < data['min_year']:
                        
                        data['min_year'] = year
                    elif year > data['max_year']:
                        data['max_year'] = year
                else:
                    data['form_number'] =  result.td.a.string
                    data['form_title'] = form_title
                    # sets min and max equal to first year found
                    data['min_year'] = year
                    data['max_year'] = year
        else:
            data['message'] = f"Sorry couldn't find information for {form}. Please be mindful of spelling and spacing"
            
        result_list.append(data)
    print(f'Here is your JSON data:\n {json.dumps(result_list)}\n')
    save(result_list, "json", forms)
    quit()




# ______________________User input functions__________________________
def choose_mode():
    """This calls a function based on user input"""
    print("Hello, Thank you for revisting my work! You are awesome!\n")
    print("\n")
    print("Enter json to get json data or pdf to get download pdfs!")
    answer = input()

    while answer.lower().strip() not in ['pdf','json']:
        print(answer)
        print("Please enter json to get json data or pdf to get download pdfs!")
        answer = input()
    if answer.lower().strip() == 'json':
        create_json()
    elif answer.lower().strip() == 'pdf':
        download_pdf()

def get_form(format_type):
    """Asks for form input based on function called"""
    if format_type.lower() =="json":
        print("""Enter in tax forms you want information for:\n
        ex. Form W-2, Form 1095-C """)
        input_forms= input()
        forms = input_forms.split(",")
        return forms
    elif format_type.lower() == "pdf":
        print("""What tax form are you trying to download:\n\
        Ex. Form W-2 """)
        form = input()
        
        return form


def get_desired_years():
    """Asks for years from user"""
    
    print("You want pdfs from what range of years?: \n\
        Ex. 2010-2020 ***these ranges are inclusive")  


    input_years = input()
    years = input_years.split('-')
    # ___CHECK CORRECT INPUT___
    while len(years) <= 1:
        print("Please follow format ex. 2019-2020\n\
        If you want one year ex. 2016-2016\n")
        input_years = input()
        years = input_years.split('-')

    return years


#________Web scraping function__________
def search_website(form_name):
    """Performs the query for a form name on the website"""
    result_matches =[]
    # puts the input into query form 
    form_query = form_name.replace(" ", "+").strip()
    # the URL is the base for a search query -----This is used to limit results ------
        
    URL = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?value={form_query}&criteria=formNumber&submitSearch=Find"

       
    while True:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        # checking if there are actual results by looking for error message first

        error = soup.find("div", class_="errorBlock")

        if error:
            return None
        results = soup.find('table', class_="picklist-dataTable").find_all("tr")
        for result in results:
            if result.has_attr('class'):
                if result.td.a.string.lower() == form_name.strip().lower():
                    result_matches.append(result)
        # Finding the next button to look throug heach page 
        next_page = soup.find("th", class_="NumPageViewed").find('a', string="Next »")
        if next_page: 
            URL = f"https://apps.irs.gov/{next_page['href']}"
                
        else:

            return result_matches
            
    
# ____Helper functions__________   

def get_year_ranges(results, form_name):
    """Prints the ranges of years and returns pdf links"""
    min_year = 0
    max_year = 0
    all_pdfs= {}
    for result in results:
        pdf_link = result.td.a['href']
        year = int(result.find('td', class_ = "EndCellSpacer").get_text(strip = True))
        all_pdfs[year] = pdf_link  #-->> GETS ALL AVAILABLE PDF LINKS FOR DESIRED FORM BY YEAR

        if min_year == 0:
            min_year = year
        
        if year < min_year:             
            min_year = year

        elif year > max_year:
            max_year = year
                   
    
    # double check that there are pdfs
    if not all_pdfs:
        print(f"Couldn't find results for {form_name}. Be mindful of spacing and spelling.")
        return None
                    
    print(f'{form_name} has pdfs from year: {min_year} to year: {max_year}\n')
    return all_pdfs

def save(results, format_type, form_name, min_year = 0, max_year = 0):
    """Gives the option to save results passed into the function as format pased in"""
    # ______________SAVE JSON OPTION__________________________
    if format_type.lower() == "json":  
        print("Would you like to save your JSON file Y OR N?")
        answer = input()  

        if answer.lower() in ["y", 'yes']:
            # Saved file names are differentiated by time and query
            file_date =datetime.utcnow().strftime("%B %d %Y %I:%M%p")
            filename = f"{form_name}- {file_date}.json"
            with open(f'saved-JSON/{filename}', 'w') as f:
                json.dump(results, f)

            print(f"***** Your file has been saved as {filename} in the saved-JSON folder! *****")
    # ______________FIND DESIRED PDF LINKS IN DICTIONARY_________ 
    elif format_type.lower() == "pdf":
        for year , link in results.items():
            if year >= min_year and year <= max_year:
                url = link

                response = requests.get(url)

                with open(f'saved-PDF/{form_name} - {year}.pdf', 'wb') as f:
                    f.write(response.content)

        print('***** Your pdfs are finished! They can be found in the saved-PDF folder! *****')

if __name__ == '__main__':
    choose_mode()