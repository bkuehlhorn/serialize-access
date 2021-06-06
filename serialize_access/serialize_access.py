"""
Dict with access to nested dict and list thru a single flat key
-----------------------------------------------------------------

Support to access values with one complex key
"""
import collections
from functools import singledispatchmethod
import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(levelogging.INFO)
class myDictHelp(object):
    @singledispatchmethod
    def init_my_dict(self, my_dict, part_key, tabs):
        if my_dict == ():
            if part_key.isnumeric():
                my_dict = [None] * int(part_key)
            else:
                my_dict = {part_key: None}
        else:
            logger.error(f"{tabs}error: part_key: {part_key}, {my_dict}")
            pass
        logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
        return my_dict, part_key

    @init_my_dict.register
    def _(self, my_dict: dict, part_key, tabs):
        if part_key not in my_dict:
            my_dict[part_key] = ()
        logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
        return my_dict, part_key

    @init_my_dict.register
    def _(self, my_dict: list, part_key, tabs):
        part_key = int(part_key)
        if part_key < len(my_dict):
            my_dict += [()] * (part_key + 1 - len(my_dict))
        logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
        return my_dict, part_key

    @singledispatchmethod
    def addElement(self, my_dict, last_part_key, prior_my_dict, prior_part_key):
        if last_part_key.isnumeric():
            last_part_key = int(last_part_key)
            if last_part_key >= len(my_dict):
                prior_my_dict[prior_part_key] += [()] * (
                    last_part_key + 1 - len(my_dict)
                )
        else:
            prior_my_dict[prior_part_key] = dict()
        my_dict = prior_my_dict[prior_part_key]
        return last_part_key, my_dict

    @addElement.register
    def _(self, my_dict: list, last_part_key, prior_my_dict, prior_part_key):
        last_part_key = int(last_part_key)
        if last_part_key >= len(my_dict):
            my_dict += [()] * (last_part_key + 1 - len(my_dict))
        return last_part_key, my_dict

    @addElement.register
    def _(self, my_dict: dict, last_part_key, prior_my_dict, prior_part_key):
        return last_part_key, my_dict

    def addElementx(self, my_dict, last_part_key, prior_my_dict, prior_part_key):
        if isinstance(my_dict, list):
            last_part_key = int(last_part_key)
            if last_part_key >= len(my_dict):
                my_dict += [()] * (last_part_key + 1 - len(my_dict))
        elif not isinstance(my_dict, dict):
            if last_part_key.isnumeric():
                last_part_key = int(last_part_key)
                if last_part_key >= len(my_dict):
                    prior_my_dict[prior_part_key] += [()] * (
                        last_part_key + 1 - len(my_dict)
                    )
            else:
                prior_my_dict[prior_part_key] = dict()
            my_dict = prior_my_dict[prior_part_key]
        return last_part_key, my_dict
my_dict_help = myDictHelp()

"""


"""
DELIMITER = ":"


def getValue(json_dict_list, key):
    """
    Key contains individual dict and list keys separated by ":"
    Returns final value from complex key. None is returned when partial key is not found

    :param key: string of keys with ":" DELIMITER
    :return: value of final key
    """
    if isinstance(key, int):
        keys = [key]
    elif isinstance(key, str):
        keys = key.split(DELIMITER)
    else:
        keys = key
    my_dict = json_dict_list
    logger.debug(f"keys: {list(keys)}")
    index = 0
    try:
        for part_key in keys:
            logger.debug(f"\tpart_key: {part_key}")
            if isinstance(part_key, str):
                if part_key.isnumeric():
                    part_key = int(part_key)
                elif part_key == "":
                    return ""
            my_dict = my_dict[part_key]
            index += 1
    except (KeyError, IndexError) as e:
        e.args = (f"{e.args[0]} for entry {index}:{part_key}",)
        raise e
    logger.debug(f"my_dict: {my_dict}")
    return my_dict


def setValue(json_dict_list, key, value):
    """
    Find last key in json_dict_list from key string
    Add [] for missing keys when next is int
    add MyDict() for missing keys when next is not int

    verify key:
        is int: make list
        is list: make copy
        is other: split by delimiter

    verify json_dict_list:
        is list or dict:
            set myDict
        is other:

    pop last_key

    for each key
        if can walk: walk to next myDict
        else: add new node for key

    if myDict is (dict or list):
    else: add dict or list

    myDict[last_key] = value

    :param key: string of keys with ":" DELIMITER
    :param value: value for last key
    :return: None
    """
    if isinstance(key, int):
        keys = [key]
    elif isinstance(key, list):
        keys = key.copy()
    else:
        keys = key.split(DELIMITER)
    last_part_key = keys.pop()
    prior_part_key = None
    prior_my_dict = {}
    my_dict = json_dict_list
    logger.debug(f"keys: {list(keys)}, value: {value}")
    tabs = ""
    # my_dict_help = myDictHelp()
    for part_key in keys:
        tabs += "\t"
        logger.debug(f"\tpart_key: {part_key}")
        my_dict, part_key = my_dict_help.init_my_dict(my_dict, part_key, tabs)
        prior_part_key = part_key
        prior_my_dict = my_dict
        my_dict = my_dict[part_key]
    last_part_key, my_dict = my_dict_help.addElement(my_dict, last_part_key, prior_my_dict, prior_part_key)
    my_dict[last_part_key] = value
    return



# class myDictHelp(object):
#     # @format.register
#     # def _(self, arg: date):
#     def init_my_dict(self, my_dict, part_key, tabs):
#         if isinstance(my_dict, dict):
#             if part_key not in my_dict:
#                 my_dict[part_key] = ()
#             logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
#         elif isinstance(my_dict, list):
#             part_key = int(part_key)
#             if part_key < len(my_dict):
#                 my_dict += [()] * (part_key + 1 - len(my_dict))
#             logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
#         else:
#             if my_dict == ():
#                 if part_key.isnumeric():
#                     my_dict = [None] * int(part_key)
#                 else:
#                     my_dict = {part_key: None}
#             else:
#                 logger.error(f"{tabs}error: part_key: {part_key}, {my_dict}")
#                 pass
#             logger.debug(f"{tabs}part_key: {part_key}, my_dict[part_key]")
#         return my_dict, part_key



def getKeys(json_dict_list, serialize=True):
    """
    get unique string of keys to values in response dict
    list use 0 for entry

    Add support to return keys as list

    :return: list of all key string to access elements
    """
    response = json_dict_list
    notDone = True
    if isinstance(response, dict):
        keys = iter(response.keys())
        logger.debug(f"dict keys: {response.keys()}")
    elif isinstance(response, list):
        keys = iter(range(len(response)))
        logger.debug(f"list keys: {list(range(len(response)))}")
    else:
        logger.debug(f"scalar keys: {response}")
        notDone = False
    jsonStack = collections.deque()
    fullKeys = []
    fullKey = []
    while notDone:
        tabs = "\t" * len(jsonStack)
        if isinstance(response, dict):
            key = next(keys, None)
        elif isinstance(response, list):
            key = next(keys, None)
        else:
            key = None
        logger.debug(f"\t{tabs}key: {key}")
        if key is None:
            if len(jsonStack) > 0:
                (response, fullKey, keys) = jsonStack.pop()
            else:
                notDone = False
        else:
            logger.debug(f"\t{tabs}\tresponse[key]: {response[key]}")
            if isinstance(response[key], (list, dict)):
                logger.debug(f"\t\t\t{tabs}list/dict")
                jsonStack.append((response, fullKey, keys))
                fullKey = fullKey.copy()
                response = response[key]
                key = key if isinstance(key, str) else str(key)
                fullKey.append(key)
                if isinstance(response, dict):
                    sortedKeys = sorted(response.keys())
                    keys = iter(sortedKeys)
                else:
                    response = [0] if len(response) == 0 else response
                    keys = iter(range(len(response)))
                    pass
            else:
                logger.debug(f"\t\t\t{tabs}value")
                if len(response) > 0 and isinstance(response[key], (dict, list)):
                    key = response[key]
                else:
                    key = key if isinstance(key, str) else str(key)
                    fullKeys.append(
                        DELIMITER.join(fullKey + [key]) if serialize else fullKey + [key]
                    )
        logger.debug(
            f'{tabs}*** last fullKey: {fullKeys[-1] if len(fullKeys) > 0 else  "start"}'
        )
    return fullKeys

# new functionality to improve coding
from datetime import date, time

class Formatter:
    @singledispatchmethod
    def format(self, arg):
        raise NotImplementedError(f"Cannot format value of type {type(arg)}")

    @format.register
    def _(self, arg: date):
        return f"{arg.day}-{arg.month}-{arg.year}"

    @format.register
    def _(self, arg: time):
        return f"{arg.hour}:{arg.minute}:{arg.second}"

# f = Formatter()
# print(f.format(date(2021, 5, 26)))
# # 26-5-2021
# print(f.format(time(19, 22, 15)))
# # 19:22:15
