# Purpose: Create JSON requests for the Attribute Generator
#   microservice, and place them in the required directory
#   'integration/requests/inbox'

import json
from datetime import datetime
import random
import os
import time
import shutil

CREATURE_LIST = ["Dwarf", "Elf", "Gnome", "Halfling", "Halforc", "Pokemon"]
ATTRIBUTES1 = ["height", "weight", "eye_color", "hair_color"]
ATTRIBUTES2 = ["type1", "type2", "legendary"]

def main():
    """
    Main function for the tester program.
    """

    #------------------------------------------
    # Create a JSON request file
    #
    # Needed: ID number, creature requested, attributes requested
    #------------------------------------------

    # ID Number:
    # This can be anything. Suggestions: uuid, shortuuid,
    #   creature + date-time stamp.
    # Some examples in the existing folders use strings generated
    #   from https://www.random.org/
    # The 'creature + date-time stamp' will be shown here.

    # Some request entries will be generated randomly. When using the
    # microservice, these would probably be selected by the user instead.

    output_dictionary = {}

    # Randomly choose a category. Use that category and the current datetime
    # as the ID number.
    category = random.choice(CREATURE_LIST)
    curr_datetime = datetime.now().strftime('%Y%m%d%H%M%S')
    id_num = category + "_" + curr_datetime

    # Generate the Attributes_Wanted list.
    # Microservice will generate only those that are requested.
    # For Pokemon, this is the whole list (in this demo).
    # For the others, a minimum of one is required.
    attributes = []

    if category == "Pokemon":
        attributes = ATTRIBUTES2
    else:
        first_att = random.choice(ATTRIBUTES1)
        attributes.append(first_att)
        for att in ATTRIBUTES1:
            if att not in attributes:
                choice = random.randint(0,1)
                if choice:
                    attributes.append(att)

    # Now that all the values have been created, populate the dictionary.
    output_dictionary["ID_Num"] = id_num
    output_dictionary["Category"] = category
    output_dictionary["Attributes_Wanted"] = attributes

    #------------------------------------------
    # Save the JSON request file:
    #  - directory: /integration/requests/inbox
    #  - filename is <ID_Num>_output
    #------------------------------------------

    path_name = f'integration/requests/inbox/{id_num}_input.json'

    with open(path_name, 'w') as out_file:
        json.dump(output_dictionary, out_file, indent=4)

    #------------------------------------------
    # Wait for a response in the outbox folder
    #------------------------------------------
    # specify the folder to look in and the expected file name
    folder_path = 'integration/responses/outbox'
    file_name = f'{id_num}_output.json'

    # generate the full path, and keep checking that full path for
    # the desired file
    full_path = os.path.join(folder_path, file_name)
    while not os.path.exists(full_path):
        time.sleep(1)


    # ------------------------------------------
    # Parse the response from the microservice
    # ------------------------------------------
    try:
        with open(full_path, 'r') as response_file:
            response = json.load(response_file)
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found in the specified path.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")

    category = response["Category"]

    print(f"Here are some random attributes for your {response["Category"]}:\n")
    for attribute, val in response["Attributes"].items():
        print(f'{attribute}: {val}')

    # ------------------------------------------
    # Move the response file to the "archived' folder.
    # ------------------------------------------
    response_original = f'integration/responses/outbox/{id_num}_output.json'

    response_done = 'integration/responses/archived/'

    try:
        shutil.move(response_original, response_done)
    except FileNotFoundError:
        print(f"Error: The source path {response_original} was not found.")
    except shutil.Error as e:
        print(f"Error moving file: {e}.")


if __name__ == '__main__':
    main()
