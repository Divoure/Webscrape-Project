import json


def make_json(output_list, headers):
    obj = {}
    list_of_objects = []
    i = 0

    for outputs in output_list:
        for output in outputs:
            if not output.isdigit():
                obj[headers[i]] = output
            else:
                obj[headers[i]] = int(output)
            i += 1
            if i == len(headers):
                i = 0
                list_of_objects.append(obj)
                obj = {}

    #print(list_of_objects)
    return list_of_objects
