# calc-parser
A self-made calculator that parses the inputted string and shows the result. 

## Goals
This project was created with a few goals in mind.

### Test Driven Development
This project was used to take a dive in the world of test driven development using the pytest library.
As a result the python test file contains routines that test the functionality of the project

### Extensible
The program is made so it can be extended very easily.
New special functions are really easy to create thanks to the division of the interface, base functions and special functions.
This means that you only have to create a new class in the special.py file and insert it into the specialDict variable with a string to call it.

## Known issues
This project is a small project to get familiar with testing and test driven development.
This means that the user interface wasn't a priority as a result it is a basic command prompt.
Exceptions caused by typing errors or bad function invocations will not be caught.

## Usage
First install the dependencies by executing the following in the command terminal:
```
pip install -r requirements.txt
```
You can then use the program by executing the following in the command terminal:
```
python pdf.py
```
