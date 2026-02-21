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


    #create shallow copy of "PokeAttributes"
    att = attributes["PokeAttributes"]
    # 18 (0-17) attributes for type1
    type1_attribute = att["type1"][random.randint(0, 17)]
    # 19 (0-18) for type2
    type2_attribute = att["type2"][random.randint(0, 18)]
    # 2  (0-1)for legendary
    legendary_attribute = att["legendary"][random.randint(0, 1)]



if __name__ == '__main__':
    main()
