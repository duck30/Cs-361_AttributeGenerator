import json
import random

def gen_rand_from_list(att_list: list):
    """
    Generates a random value from an input list.
    """
    return random.choice(att_list)

def gen_rand_from_range(min_: int, max_: int) -> int:
    """
    Generates a random value from input range, inclusive.
    """
    return random.randint(min_, max_)

def main():
    """
    Main function for Attribute Generator microservice
    """
    #-----------------------
    # Import JSON file with attributes
    #-----------------------
    attribute_file = 'resources/attributes/attributes.json'

    try:
        with open(attribute_file, 'r') as att_file:
            attributes = json.load(att_file)
    # ****** currently printing error messages - can make helpful return if/when needed *******
    except FileNotFoundError:
        print(f"Error: The file {attributes} was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")


    # create shallow copy of "PokeAttributes"
    att = attributes["PokeAttributes"]
    # 18 (0-17) attributes for type1
    type1_attribute = gen_rand_from_list(att["type1"])
    # 19 (0-18) for type2
    type2_attribute = gen_rand_from_list(att["type2"])
    if type2_attribute == type1_attribute:
        type2_attribute = gen_rand_from_list(att["type2"])
    # 2  (0-1)for legendary
    legendary_attribute = gen_rand_from_list(att["legendary"])
    
    response = {
        "Category": "Pokemon",
        "Attributes": {
        "type1": type1_attribute,
        "type2": type2_attribute,
        "legendary": legendary_attribute
        }}
     
    file_name = 'response_file.json'
    try:
        with open(file_name, 'w') as response_file:
            msg_error = json.dump(response, response_file, indent=4, ensure_ascii=False)
    # ****** currently printing error messages - can make helpful return if/when needed *******
    except FileNotFoundError:
        print(f"Error: The file {msg_error} was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")



if __name__ == '__main__':
    main()
