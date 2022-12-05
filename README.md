# SoEye
SoEye is a social media forensics tool. It supports the investigation of Reddit and Twitter. It was developed as group project for CSS453 - Cyber Crimes and Digital Forensics in the first semester of the academic year 2022 at Sirindhorn International Institute of Technology (SIIT), Thammasat University, Thailand.

## Dependencies
- [Python 3.8](https://www.python.org/downloads/) or higher
- snscrape
```
pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git
```
- pandas
```
pip3 install pandas
```
- flask
```
pip3 install Flask
```
## Installation
```
git clone https://github.com/levinKaus/SoEye.git
```

## Usage
- Open a terminal and move to the folder you cloned the reposetory to
- Start the app using the following command
```
flask --app soeye run
```
- Open your browser and go the following website
```
http://localhost:5000/
``` 


Alternative: 
- Run the `soeye.bat` file which does the previous described for you

Once started proceed as follows:
- Set the project details on the start page
- Start a search on the search page
- Inspect search results on the results page
- Conduct a keyword search on the search side
- Select evidence to be added to the report by clicking on a row of the result table
- Remove evidence from the report by clicking on it in the report
- The report can be extracted as json file under the following path: SoEye/static/json/report.json 


## Members
* Annu Maria Keranen (6522808202)
* Levin Kaus (6522808210)
* Michiel Thiers (6522808160)
* Miguel Donas-Botto (6522808327)
