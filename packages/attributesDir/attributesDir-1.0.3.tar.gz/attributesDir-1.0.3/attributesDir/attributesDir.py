"""Module Usage:
    To list the properties, functions, methods, class, modules
    of object with pretty format.

Args:
    object_name (object): An object name. Defaults to os.

Main Functions:
    adir(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    classify(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    modules(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    classes(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    functions_or_methods(object_name=object_name, columns=4, width=30,
        pattern=r"^[^_]")
    functions(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    methods(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    constants(object_name=object_name, columns=4, width=30, pattern=r"^[^_]")
    aprint(sequence_or_mapping, columns=4, width=30, pattern=r"^[^_]")
"""
import re
import os
from collections.abc import Iterable
from importlib import import_module
import textwrap

object_name = os
__package__ = os.path.basename(os.path.dirname(__file__))
__author__ = "Dillon"
__email__ = "aa269440877@outlook.com"
__version__ = "1.0.3"
__url__ = "https://gitee.com/ld269440877/tools/blob/master/my_modules/dir_objectName.py"
__license__ = "MIT Licence"

def adir(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Print and return an alphabetized list of names, which have a number and
    background color if print them, comprising (some of) the attributes of the
    given object, and of attributes reachable from it.

    Args:
        object_name (object, optional): An object name, default os.
        columns (int, optional): Number of Names attributes or methods will
            be printed in one line. defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. defaults to 30.
        pattern (regexp, optional): A string that match each names of
            attributes with the pattern. defaults to r"^[^_]".

    Returns:
        attributes_list (list(str)): An alphabetized list of names comprising
            (some of) the attributes of the given object

    Examples:
        >>> import os
        >>> adir(os)[5]
        ['DirEntry', 'F_OK', 'MutableMapping', 'O_APPEND', 'O_BINARY']

    """

    attributes_list = list()
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            attributes_list.append(attribute)
    # print()
    return attributes_list


def is_module(attribute):
    """True if attribute's name equals to module.

    type(module_object).__name__ == "module".

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is module.
    """
    if type(attribute).__name__ == "module":
        return True
    else:
        return False


def is_class(attribute):
    """True if attribute's name equals to type.

    type(class_object).__name__ == "type"

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is module.
    """

    if type(attribute).__name__ == "type":
        return True
    else:
        return False


def is_function_or_method(attribute):
    """True if attribute's name equals to function,
    method or builtin_function_or_method.

    type(class_object).__name__ == "type"
    type(class_object.callable_object).__name__ == "function"
    type(instance_object.callable_object).__name__ == "method"
    type(built_callable_object).__name__ == "builtin_function_or_method"

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is function, method or
        builtin_function_or_method.
    """

    if type(attribute).__name__ == 'builtin_function_or_method' or\
            type(attribute).__name__ == "function" or\
            type(attribute).__name__ == "method":
        return True
    else:
        return False


def is_function(attribute):
    """True if attribute's name equals to function or
    builtin_function_or_method.

    type(class_object.callable_object).__name__ == "function"
    type(built_callable_object).__name__ == "builtin_function_or_method"

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is function or
        builtin_function_or_method.
    """
    if type(attribute).__name__ == 'builtin_function_or_method' or\
            type(attribute).__name__ == "function":
        return True
    else:
        return False


def is_method(attribute):
    """True if attribute's name equals to method or
    builtin_function_or_method.

    type(instance_object.callable_object).__name__ == "function"
    type(built_callable_object).__name__ == "builtin_function_or_method"

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is method or
        builtin_function_or_method.
    """
    if type(attribute).__name__ == 'builtin_function_or_method' or\
            type(attribute).__name__ == "method":
        return True
    else:
        return False



def is_constant(attribute):
    """True if attribute's name not equals to module, class, function, method
    or builtin_function_or_method.

    Args:
        attribute (object): An attribute of object.

    Returns:
        bool: True if attribute's name is not module, class, function, method
    or builtin_function_or_method.
    """
    if not is_module(attribute) and\
        not is_class(attribute) and\
            not is_function_or_method(attribute):
        return True
    else:
        return False


def classify(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains classes, functions or methods,
    constants objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains classes, functions or methods, constants
        objects.
    """
    classes_list = classes(object_name=object_name, columns=columns,
                           width=width, pattern=pattern)

    functions_or_methods_list = functions_or_methods(object_name=object_name,
                                                     columns=columns,
                                                     width=width,
                                                     pattern=pattern)

    constants_list = constants(object_name=object_name, columns=columns,
                               width=width, pattern=pattern)
    classify_dict = {
        "classess": classes_list,
        "function_or_methods": functions_or_methods_list,
        "constants": constants_list
    }
    # print()
    return classify_dict


def modules(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains module objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains module objects.
    """
    count = 0
    modules_list = list()

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")
        raise AttributeError(str(e))

    # print(f'\033[41m{"Modules":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_module(getattr(object_name, str(attribute))):
                modules_list.append(attribute)
    return modules_list


def classes(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains class objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains class objects.
    """
    count = 0
    classes_list = list()
    # import_module(object_name.__name__)

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")

    # print(f'\033[41m{"Classes":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_class(getattr(object_name, str(attribute))):
                classes_list.append(attribute)
    # print()
    return classes_list


def functions_or_methods(object_name=object_name, columns=4,
                         width=30, pattern=r"^[^_]"):
    """Get dict object that contains function or method objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains function or method objects.
    """
    count = 0
    functions_or_methods_list = list()

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")

    # print(f'\033[41m{"Functions or Methods":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_function_or_method(getattr(object_name, str(attribute))):
                functions_or_methods_list.append(attribute)
    # print()
    return functions_or_methods_list


def functions(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains function objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains function objects.
    """
    count = 0
    functions_list = list()

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")

    # print(f'\033[41m{"Functions":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_function(getattr(object_name, str(attribute))):
                functions_list.append(attribute)
    # print()
    return functions_list


def methods(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains method objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains method objects.
    """
    count = 0
    methods_list = list()

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")

    # print(f'\033[41m{"Functions":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_method(getattr(object_name, str(attribute))):
                methods_list.append(attribute)
    # print()
    return methods_list


def constants(object_name=object_name, columns=4, width=30, pattern=r"^[^_]"):
    """Get dict object that contains constant objects.

    Args:
        object_name (object, optional): Object name to get attributes.
            Defaults to object_name.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".

    Returns:
        list: A list that contains constant objects.
    """
    count = 0
    constants_list = list()

    try:
        locals()[object_name.__name__] = object_name
    except AttributeError as e:
        print("If it is a callable object then you can assign a __name__ attribute to it.\n\
But the value assigned to __name__ must be the name of the callable object.")

    # print(f'\033[41m{"Constants":^50}\033[0m')
    for index, attribute in enumerate(dir(object_name), start=1):
        if re.search(pattern, attribute):
            if is_constant(getattr(object_name, str(attribute))):
                constants_list.append(attribute)
    # print()
    return constants_list


def adoc(object_name=object_name, print_classess=True, print_function_or_methods=True, print_constants=True):
    classify_dict = dict()
    if print_classess:
        classify_dict.update({"classess": classes(object_name)})

    if print_function_or_methods:
        classify_dict.update({"function_or_methods": functions_or_methods(object_name)})

    if print_constants:
        classify_dict.update({"constants": constants(object_name)})

    print(f'\033[41m{getattr(object_name, "__name__", str(object_name))}\033[0m', [getattr(object_name, "__doc__", "__doc__ is not provided!")][0])
    for sub_object, attributes in classify_dict.items():
        print(f'\033[41m{sub_object: ^50}\033[0m', end="\n")
        for attribute in attributes:
            print(f'\033[42m{attribute: ^{len(attribute)}}\033[0m')
            if sub_object in ['classess', 'function_or_methods']:
                doc = getattr(getattr(object_name, attribute), "__doc__", str())
                print(textwrap.indent(doc if doc != None  else str(), prefix=" " * 4))
            else:
                value = repr(getattr(object_name, attribute, str()))
                print(textwrap.indent(value if value != None else str(), prefix=" " * 4))


def aprint(sequence_or_mapping, columns=4, width=30, pattern=r"^[^_]"):
    """Print each element of iterable object with giving format and columns
    in multi-line.

    Args:
        sequence_or_mapping (object): sequence or mapping.
        columns (int, optional): Number of Names attributes or methods
            will be printed in one line. Defaults to 4.
        width (int, optional): Placeholder length of each attributes or
            methods names. Defaults to 30.
        pattern (regexp, optional):  A string that match each names of
            attributes with the pattern. Defaults to r"^[^_]".
    """
    if isinstance(sequence_or_mapping, dict):
        for key in sequence_or_mapping:
            print(f'\033[41m{key: ^50}\033[0m', end="\n")
            aprint(sequence_or_mapping[key], columns=4,
                         width=30, pattern=r"^[^_]")
    elif isinstance(sequence_or_mapping, Iterable):
        for index, attribute in enumerate(sequence_or_mapping, start=1):
            if re.search(pattern, attribute):
                if index % columns == 0:
                    print(f'\033[41m{index:0>3}\033[0m {attribute:<{width}}',
                          end="\n")
                else:
                    print(f'\033[41m{index:0>3}\033[0m {attribute:<{width}}',
                          end="")
    else:
        print(sequence_or_mapping)
    print()



def help():
    print("__file__", __file__, "\n__doc__", __doc__)

if __name__ == "__main__":
    aprint(classify(object_name))
    adoc(object_name)