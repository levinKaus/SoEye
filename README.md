# SoEye
SoEye is a social media forensics tool. It supports the investigation of Instagram, Twitter, Facebook, and LinkedIn. It was developed as group project for CSS453 - Cyber Crimes and Digital Forensics in the first semester of the academic year 2022 at Sirindhorn International Institute of Technology (SIIT), Thammasat University.

## Dependencies
- [Python 3.8](https://www.python.org/downloads/) or higher
- snscrape
```
pip3 install snscrape
```
- pandas
```
pip3 install pandas
```

## Installation
```
git clone https://github.com/levinKaus/SoEye.git
```

## Usage
SoEye is a CLI tool. That means you can use it with your command promt. Therfore open your command promt of choice and navigate to the folder you downloaded SoEye to. In the following there is a list of commands you can run, exemplary for windows. (Run all commands without the <> symbols)
- Initialization (always run this command first)
```
py soeye.py init <project number> <'project file name'> <'project description'>
```
- Reddit user search
```
py soeye.py reddit <'username'> <number of posts to investigate>
```
- Twitter user search
```
py soeye.py twitter <'username'> <number of posts to investigate>
```
- See all available commands
```
py soeye.py --help
```
- See arguments of a command
```
py soeye.py <command> --help
```

## Members
* Annu Maria Keranen (6522808202)
* Levin Kaus (6522808210)
* Michiel Thiers (6522808160)
* Miguel Donas-Botto (6522808327)
