# Cs-361_AttributeGenerator
Generates random attributes of fantasy races for the user.

## What kinds of races? What kinds of attributes?
The possible creatures you can generate attributes for are:
- Dwarf
- Elf
- Gnome
- Halfling
- Halforc
- Pokemon

Any of the first five creature Categories can have the following attributes generated:
- height
- weight
- eye color
- hair color

Pokemon can have the following attributes generated:
- type1
- type2
- legendary

## Microservice Directory Structure
### /integration/requests/inbox:
Incoming request files should be placed here

### /integration/requests/done:
Requests that have been processed get placed here by the microservice

### /integration/requests/error:
This functionality is currently not implemented, but this folder would hold input files that created errors upon attempted processing.

### /integration/responses/outbox:
JSON files with the randomly generated attributes (the output of the microservice) are placed here by the microservice.

### /integration/responses/archived:
The caller of the microservice can use this folder to hold microservice output files that it has already dealt with, if desired.

### /resources/attributes:
The master attributes JSON file is kept here.

## How it works - here's what you need to know!
- The caller of the microservice will need to handle a) starting the microservice and b) shutting down the microservice
- The microservice is set up so that SIGINT and SIGTERM signals sent to the microservice will cause the microservice to shut down after completing its current attribute generation, if applicable.
- Once started, the microservice will check the 'inbox' folder every 5 seconds for an inbound request.
- If at least one is found, it will process one and then return to looking for additional ones every 5 seconds.
- If more than one inbound request file is found, it will process the least recently modified request (goal is a FIFO system, roughly).

## Format of input file (JSON)
Filename: <ID_Num>_input.json  
  
{  
    &emsp;"ID_Num": "(same ID_Num as in the filename)"  
    &emsp;"Category": "(creature-type you want random attributes for)"  
    &emsp;"Attributes_Wanted": [list of attributes wanted]  
 }  

 Example:  dwarf_20260221223103_input.json
   
 {  
    &emsp;"ID_Num": "dwarf_20260221223103"  
    &emsp;"Category": "Dwarf"  
    &emsp;"Attributes_Wanted": [  
      &emsp;&emsp;"weight",  
      &emsp;&emsp;"eye_color",  
      &emsp;&emsp;"hair_color"  
    &emsp;]  
 }  

## Format of output file (JSON)
Filename: <ID_Num>_output.json  
  
{  
    &emsp;"ID_Num": "(same ID_Num as in the filename)"  
    &emsp;"Category": "(creature-type random attributes were generated for)"  
    &emsp;"Attributes": {dictionary of attributes}  
 }  
  
 Example: dwarf_20260221223103_output.json
   
 {  
    &emsp;"ID_Num": "dwarf_20260221223103"  
    &emsp;"Category": "Dwarf"  
    &emsp;"Attributes": {  
    &emsp;&emsp;  "weight": 173,  
    &emsp;&emsp;  "eye_color": "Ruby Red",  
    &emsp;&emsp;  "hair_color": "Copper"  
    &emsp;}  
 }  
 
 
    
    


