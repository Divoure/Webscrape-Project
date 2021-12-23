# Functions that creates dictionaries (objects) out of a list of headers and a list of data in this format; header: data
def make_json(output_list, headers):
    obj = {}    # Empty dictionary (object)
    list_of_objects = []    # Empty list
    i = 0   # Counter

    # For each list in output_list
    for outputs in output_list:
        # For each data in the list
        for output in outputs:
            # If the data is able to be cast as int, saves it to the object with the correct header
            if output.isdigit():
                obj[headers[i]] = int(output)   # Saves int
            else:
                obj[headers[i]] = output    # Saves string
            i += 1  # Counter incremented by 1
            # Checks if the counter is at the end of the cycle (the end being the length of the list of headers)
            if i == len(headers):
                i = 0   # Sets counter back up to zero
                list_of_objects.append(obj)  # Appends the put together dictionary (object) to the list of objects
                obj = {}    # Cleans the dictionary (object), otherwise it will overwrite everything with the last entry

    return list_of_objects  # Returns the list of objects in json-friendly format
