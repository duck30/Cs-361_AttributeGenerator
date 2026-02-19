import json
import random



def main():
    """
    Main function for Attribute Generator microservice
    """
    #-----------------------
    # Import JSON file with attributes
    #-----------------------
    attribute_file = 'attributes.json'

    try:
        with open(attribute_file, 'r') as att_file:
            attributes = json.load(att_file)
    # ****** currently printing error messages - can make helpful return if/when needed *******
    except FileNotFoundError:
        print(f"Error: The file {attributes} was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")

    ##################################################################################
    # 'attributes' is the whole attribute dictionary imported from the file
    #
    # attributes["PokeAttributes"] will give you the pokemon attribute dictionary
    # by itself. then you can treat it like any other python library.
    #################################################################################
    #create shallow copy of "PokeAttributes"
    att = attributes["PokeAttributes"]
    # 18 (0-17) atrributes for type1
    type1_attribute = att["type1"][random.randint(0, 17)]
    # 19 (0-18) for type2
    type2_attribute = att["type2"][random.randint(0, 18)]
    # 2  (0-1)for legendary
    legendary_attribute = att["legendary"][random.randint(0, 1)]



if __name__ == '__main__':
    main()
