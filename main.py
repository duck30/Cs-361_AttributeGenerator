import json
import random
from pathlib import Path
import shutil
import time
import signal
import threading

# create a threading event, will help with microservice shutdown
shutdown_event = threading.Event()

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

def open_oldest_file(dir_path: str):
    """
    Opens the oldest file in a directory, if possible.

    input:
        dir_path: the directory path to search
    output:
        'file handle' if found
        'None' otherwise
    """
    # wraps the directory path in a Path object from pathlib
    p = Path(dir_path)

    # p.iterdir() iterates over all entries in the file path
    # f.is_file() - checks whether the entry f is a file
    # `files` will be a list of Path objects representing files
    #   in that directory
    files = [f for f in p.iterdir() if f.is_file()]

    # if there are no files, return None
    if not files:
        return None

    # f.stat() accesses the file's metadata
    # st_mtime is modification time
    # this selects the file with the earliest modification time
    oldest_file = min(files, key=lambda f: f.stat().st_mtime)

    # open the file
    file_handle = oldest_file.open(mode='r', encoding='utf-8')

    # returns a tuple: the Path object pointing to the file, and
    #   the open file handle
    return file_handle

def generate_attributes(request: dict, attributes: dict) -> dict:
    """
    Generates the requested attributes from the master attribute file.

    input:
        request (dictionary from a JSON request file)
        attributes (master attributes dictionary, also from JSON file)
    output:
        dictionary with the id_number and creature type of the request,
            and all the random attributes that have been generated.
    """
    # preserve the ID number and the category
    output_dict = {
        "ID_Num": request["ID_Num"],
        "Category": request["Category"]
    }

    new_att_dict = {}

    # get the dictionary corresponding to the requested creature type
    type_requested = request["Category"]
    type_dict = attributes[type_requested]

    # generate the requested attributes, add them to the output dict
    for attribute_name, attribute_specs in type_dict.items():
        if attribute_name in request["Attributes_Wanted"]:
            if isinstance(attribute_specs, list):
                rand_att = gen_rand_from_list(attribute_specs)
            elif attribute_specs["min"]:
                rand_att = gen_rand_from_range(attribute_specs["min"],
                                               attribute_specs["max"])
            else:
                rand_att = None
            new_att_dict[attribute_name] = rand_att

    output_dict["Attributes"] = new_att_dict

    return output_dict

def _handle_shutdown(signum, frame):
    """
    Sets a shutdown flag; when the process sees this it will begin
    a graceful shutdown.
    """
    # Just set the flag; let the main loop finish current work and exit.
    shutdown_event.set()

def main():
    """
    Main function for Attribute Generator microservice
    """
    # -----------------------
    # Register graceful shutdown handlers - call handle_shutdown instead
    # of default behavior
    # -----------------------
    signal.signal(signal.SIGINT, _handle_shutdown)   # e.g., Ctrl+C
    signal.signal(signal.SIGTERM, _handle_shutdown)  # e.g., kill, systemd stop

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

    # -----------------------
    # Every 5 seconds, check for a JSON request file
    # -----------------------
    while not shutdown_event.is_set():
        for _ in range(5):
            if shutdown_event.is_set():
                break
            time.sleep(1)
        if shutdown_event.is_set():
            break

        file_handle = open_oldest_file('integration/requests/inbox')

        if not file_handle:
            continue

        try:
            request = json.load(file_handle)
        finally:
            file_handle.close()


        # -----------------------
        # Get the requested attributes from the requested creature type
        # -----------------------
        output_dict = generate_attributes(request, attributes)

        # -----------------------
        # Save the output into a new JSON file in /integration/responses/outbox
        # -----------------------
        path_name = f'integration/responses/outbox/{output_dict["ID_Num"]}_output.json'
        tmp_path = path_name + ".tmp"

        with open(tmp_path, 'w') as out_file:
            json.dump(output_dict, out_file, indent=4)

        os.replace(tmp_path, path_name)

        # -----------------------
        # Move the request file to "done" folder
        # -----------------------
        request_original = f'integration/requests/inbox/{output_dict["ID_Num"]}_input.json'

        request_done = 'integration/requests/done/'

        try:
            shutil.move(request_original, request_done)
        except FileNotFoundError:
            print(f"Error: The source path {request_original} was not found.")
        except shutil.Error as e:
            print(f"Error moving file: {e}.")


if __name__ == '__main__':
    main()
