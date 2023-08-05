import pickle

def getVariableName(variable, globalVariables):
    # from: https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
    """ Get Variable Name as String by comparing its ID to globals() Variables' IDs
        args:
            variable(var): Variable to find name for (Obviously this variable has to exist)
        kwargs:
            globalVariables(dict): Copy of the globals() dict (Adding to Kwargs allows this function to work properly when imported from another .py)
    """
    for globalVariable in globalVariables:
        if id(variable) == id(globalVariables[globalVariable]): # If our Variable's ID matches this Global Variable's ID...
            return globalVariable # Return its name from the Globals() dict

def pickle_wrap(filename, callback, args=None, kwargs=None, easy_override=False,
                do_dill=False):
    import os
    from time import time
    # PB: I changed the pickle wrap to have some nice features. It now says what function is passed and prints
    #     how much time was needed for the function to complete
    print('Filename:', filename)
    print('Function:', getVariableName(callback, globalVariables=globals().copy()))
    if os.path.isfile(filename) and not easy_override:
        print('Loading...')
        start = time()
        with open(filename, "rb") as file:
            pk = pickle.load(file)
            print('Load time:', time()-start)
            return pk
    else:
        print('Running...')
        start = time()
        if args:
            output = callback(*args)
        elif kwargs:
            output = callback(**kwargs)
        else:
            output = callback()
        print('Callback:', getVariableName(callback, globalVariables=globals().copy()))
        print('Function time:', time()-start)
        print('Dumping to file name:', filename)
        start = time()
        with open(os.path.join(r'C:\PycharmProjects\ScratchPad\src\last_hope', filename), "wb") as new_file:
            pickle.dump(output, new_file)
        print('Dump time:', time()-start)
        return output