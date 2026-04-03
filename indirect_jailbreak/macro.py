import utilities as ut

def replaceMacro(sequence: str):
    try:
        string = ""
        for ch in sequence:
            string += ut.substituteIntoSmallLetter(ch)
        object = ut.getGlobalVariable(string)
        return object
    except Exception as e:
        raise e

def applyMacros(sequence: str) -> str:
    mappings = []
    temp_sequence = sequence
    adjustor = 0
    while True:
        try:
            idx_1 = temp_sequence.index("__")
            temp_sequence = temp_sequence[idx_1 + 1:]
            idx_2 = temp_sequence.index("__")
            while idx_2 == 0:
                idx_1 += 1
                temp_sequence = temp_sequence[idx_1 + 1:]
                idx_2 = temp_sequence.index("__")
            MACRO_PREREPLACED = temp_sequence[1:idx_2]
            MACRO_SYMBOL = f"__{temp_sequence[1:idx_2]}__"
            temp_sequence = temp_sequence[idx_2 + 2:]
            try:
                object = replaceMacro(MACRO_PREREPLACED)
                sequence = sequence.replace(MACRO_SYMBOL, object)
                temp_sequence = sequence
            except Exception as e:
                print(e)
                continue
        except ValueError as ve:
            break
    return sequence



        

