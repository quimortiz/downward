import sys
import re
import read_sas
import timers
import os


def get_files_in_dir(path):
    if path[-1] != '/':
        path += "/"
    return [
        path + f.name for f in os.scandir(path) if f.is_file() and f.name.endswith(".txt")]

# true:  match
# false: no match


def init_state_match_all(values, info):
    flags = [values[var] == value for var, value in info]
    return not (False in flags)


# 0: var it does not appear in the action.
# 1: var appears, with same value
# 2: var apperas, with different value

## NOTES:
# For the first:
# action a
# partial states p
# if p \subset pre(a) --> eff(a') = eff(a) \union b=1
# if pre(a) \subset p --> eff(a') = eff(a) \union b=1 if p \minus pre(a) ; else set to zero
# if 



# if one of them is false: -> add state = 0
# if one of them is true: add that inf0 = 1 , conditioned on the values of the others
# if all are 0: do nothing
def add_preconditions(var_id, inf0, sas_task, precond_for_one, allow_to_zero, is_first, is_same):
    # missing: if it does not change,
    # if previous is is one, then add conditional: if previous and the state,
    # then go to one.

    print("is_same" , is_same )
    # (7,1)
    for op in sas_task.operators:
        flags = []
        for var, value in inf0:
            # search var in prevail
            flag = 0  # default: var does not appear
            for prevail in op.prevail:
                if prevail[0] == var:
                    # it appears
                    if prevail[1] == value:
                        flag = 1  # same value
                        break
                    else:
                        flag = 2  # different value
                        # the s_{t+1} is then different
                        break
                else:
                    flag = 0
                    # it does not appear
            if flag == 0:
                # keep searching
                for pre_post in op.pre_post:
                    if pre_post[0] == var:
                        # it appears
                        if pre_post[2] == value:
                            flag = 1  # same value
                            break
                        else:
                            flag = 2  # different value
                            # the s_{t+1} is then different
                            break
                    else:
                        flag = 0
                        # it does not appear
            flags.append(flag)

        print(op.name, flags)

        # # new
        added_transtion_to_zero = False
        added_transtion_to_one = False
        # # added_something = False
        #     # [(var_id , 1)]

        if 2 in flags:
            # case: at least one atom is 2 -> add 0
            if allow_to_zero:
                added_transtion_to_zero = True
                op.pre_post.append((var_id, -1, 0, []))
        elif 1 in flags:
            # at least one of the atoms is true, the others are zero
            # add the ones that are zero as precond
            pre_ = precond_for_one[:]
            for i, var_value in zip(flags, inf0):
                if i == 0:
                    pre_.append(var_value)
            added_transtion_to_one = True
            op.pre_post.append((var_id, 0, 1, pre_))
        else:
            # old: don't do anything
            # case all zeros: don't do anything
            # Maybe new: add the conditional? but it doesn't make much more
            # sense...
            pass
        if ((not added_transtion_to_one) and (not added_transtion_to_zero) and allow_to_zero and not (is_first) ):
           pp = [(var_id , 1)]
            # op.pre_post.append((var_id, -1, 0, pp)) # always transition from 1 to zero
            # op.pre_post.append((var_id, -1, 0, pp)) # always transition from 1 to zero
           if (not is_same):
                op.pre_post.append((var_id, -1, 0 , [])) # always transition from 1 to zero
           else:
                pre_ = precond_for_one[:]
                op.pre_post.append((var_id, 0, 1 , pre_)) # always transition from 1 to zero
                # add transition to zero of the previous one. how?



def parse_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
        Parsed data

    """

    state = []
    state_raw = []
    data_raw = []
    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            if line == '\n':
                data_raw.append(state_raw)
                data.append(state)
                state = []
                state_raw = []
            else:
                # string = "xxxx(142,1, 23ERWA31,aa)"
                # l = re.findall (r'([^(,)]+)(?!.*\()', string)
                # print (l)
                # ['142', '1', ' 23ERWA31', 'aa']
                atom_raw = line[:-1]
                l = re.findall(r'([^(,)]+)(?!.*\()', line[:-1])
                print(l)
                l = [i.strip() for i in l]

                # r1 = re.compile("(.*?)\s*\(")
                # text = "this is so cool (234)"
                # m1 = r1.match(text)
                # m1.group(1)
                # 'this is so cool'
                r1 = re.compile(r"(.*?)\s*\(")
                predicate = r1.match(line).group(1)
                state.append([predicate, l])
                state_raw.append(atom_raw)
            line = file_object.readline()
        if (len(state) and len(state_raw)):
            data.append(state)
            data_raw.append(state_raw)
    return data, data_raw


def parse_sas_and_mod():
    data, data_raw = parse_file("src/infeas.txt")
    print("data")
    print(data)
    print("data_raw")
    print(data_raw)
    return data, data_raw


def load_and_save_task(filename_from, filename_to):

    task = read_sas.read_sas_task(filename_from)
    timer = timers.Timer()
    with timers.timing("Writing output"):
        with open(filename_to, "w") as output_file:
            task.output(output_file)
    print("Done! %s" % timer)

    # it is the same up to ordering, because the original sas task is not ordered... why?
    # can I easily order it?
    # i guess yes... lets add a function for that :)

    # lets create the pddl task


def test_3_mod_clean(sas_task, inf0, inf1, inf2, name):
    print("quim mod")
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas1-3(0)" + name, "Atom infeas1-3(1)" + name])
    sas_task.init.values.append(
        int(init_state_match_all(sas_task.init.values, inf0)))
    add_preconditions(var_id, inf0, sas_task, [], True, True,False)

    # add the second one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas2-3(0)" + name, "Atom infeas2-3(1)" + name])
    sas_task.init.values.append(0)


    # inf1.append((var_id,1))
    add_preconditions(var_id, inf1, sas_task, [(var_id - 1, 1)], True, False,inf0==inf1)

    # add the third one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas3-3(0)" + name, "Atom infeas3-3(1)" + name])
    sas_task.init.values.append(0)
    sas_task.goal.pairs.append((var_id, 0))

    # inf1.append((var_id,1))
    add_preconditions(var_id, inf2, sas_task, [(var_id - 1, 1)], False, False, inf2==inf1)


def test_4_mod_clean(sas_task, inf0, inf1, inf2, inf3, name):
    print("quim mod")
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas1-4(0)" + name, "Atom infeas1-4(1)" + name])
    sas_task.init.values.append(
        int(init_state_match_all(sas_task.init.values, inf0)))
    add_preconditions(var_id, inf0, sas_task, [], True, True,False)

    # add the second one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas2-4(0)" + name, "Atom infeas2-4(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf1, sas_task, [(var_id - 1, 1)], True, False,inf1==inf0)

    # add the third one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas3-4(0)" + name, "Atom infeas3-4(1)" + name])
    sas_task.init.values.append(0)
    print( "check " , inf2 , inf1 , inf2==inf1)
    add_preconditions(var_id, inf2, sas_task, [(var_id - 1, 1)], True,False, inf2==inf1)

    # add the fourth one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas4-4(0)" + name, "Atom infeas4-4(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf3, sas_task, [(var_id - 1, 1)], False, False,inf3==inf2)

    # add goal
    sas_task.goal.pairs.append((var_id, 0))


def test_5_mod_clean(sas_task, inf0, inf1, inf2, inf3, inf4, name):
    print("quim mod")
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas1-5(0)" + name, "Atom infeas1-5(1)" + name])
    sas_task.init.values.append(
        int(init_state_match_all(sas_task.init.values, inf0)))
    add_preconditions(var_id, inf0, sas_task, [], True, True,False)

    # add the second one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas2-5(0)" + name, "Atom infeas2-5(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf1, sas_task, [(var_id - 1, 1)], True,False, inf1==inf0)

    # add the third one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas3-5(0)" + name, "Atom infeas3-5(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf2, sas_task, [(var_id - 1, 1)], True,False, inf2==inf1)

    # add the fourth one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas4-5(0)-5" + name, "Atom infeas4-5(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf3, sas_task, [(var_id - 1, 1)], True,False, inf3==inf2)

    # add 5th
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas5-5(0)" + name, "Atom infeas5-5(1)" + name])
    sas_task.init.values.append(0)
    add_preconditions(var_id, inf4, sas_task, [(var_id - 1, 1)], False,False, inf4==inf3)

    # add goal
    sas_task.goal.pairs.append((var_id, 0))


def test_1_mod_clean(sas_task, inf0, name):
    print("quim mod")
    num_vars_original = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas1-1(0)" + name, "Atom infeas1-1(1)" + name])

    sas_task.init.values.append(
        int(init_state_match_all(sas_task.init.values, inf0)))

    print(type(sas_task.goal.pairs))
    print(type(sas_task.goal.pairs[0]))
    sas_task.goal.pairs.append((num_vars_original, 0))

    var_id = num_vars_original
    # inf0 = [(4,0)]
    add_preconditions(var_id, inf0, sas_task, [], False , True, False)


def test_2_mod_clean(sas_task, inf0, inf1, name):
    print("quim mod")
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas1-2(0)" + name, "Atom infeas1-2(1)" + name])

    sas_task.init.values.append(
        int(init_state_match_all(sas_task.init.values, inf0)))

    add_preconditions(var_id, inf0, sas_task, [], True, True, False)

    # add the second one
    var_id = len(sas_task.variables.ranges)
    sas_task.variables.ranges.append(2)
    sas_task.variables.axiom_layers.append(-1)
    sas_task.variables.value_names.append(
        ["Atom infeas2-2(0)" + name, "Atom infeas2-2(1)" + name])
    sas_task.init.values.append(0)
    sas_task.goal.pairs.append((var_id, 0))

    # inf1.append((var_id,1))
    add_preconditions(var_id, inf1, sas_task, [(var_id - 1, 1)], False,False, inf0==inf1)


def get_data_num(sas_task, data_raw):
    data_num = []
    for state in data_raw:
        state_num = []
        for atom in state:
            # search this atom in the
            found = False
            for idvar, var in enumerate(sas_task.variables.value_names):
                for idvalue, value in enumerate(var):
                    if atom == value:
                        print(atom, "found")
                        print(idvar, idvalue)
                        state_num.append((idvar, idvalue))
                        # match = (idvar, idvalue)
                        found = True
                        break
                if found == True:
                    break
        data_num.append(state_num)
    return data_num


def help():
    print("usage SCRIPT conflict sas sas_out ")


if __name__ == "__main__":
    # read
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]

    # check if arg1 is file or folder

    is_directory = False
    try:
        f = open(arg1)
        f.close()
    except IsADirectoryError:
        is_directory = True
        print("input is directory")

    # list with files

    files = []
    if is_directory:
        print("getting all files in directory")
        files = get_files_in_dir(arg1)
    else:
        files.append(arg1)

    sas_task = read_sas.read_sas_task(arg2)
    idd = 0
    for file in files:
        print("file {}".format(file))

        data, data_raw = parse_file(file)
        print("PYTHON: removing consecutive duplicates")

        erase_duplicates = False
        if (erase_duplicates):
            data = [v for i, v in enumerate(data) if i == 0 or v != data[i - 1]]
            data_raw = [v for i, v in enumerate(
                data_raw) if i == 0 or v != data_raw[i - 1]]

        print("PYTHON: new data is")
        print("data {}".format(data))
        print("data_raw {}".format(data_raw))

        data_num = get_data_num(sas_task, data_raw)

        num_steps = len(data)
        name = "conflict" + str(idd)
        idd += 1

        if num_steps == 1:
            test_1_mod_clean(sas_task, data_num[0], name)

        elif num_steps == 2:
            test_2_mod_clean(sas_task, data_num[0], data_num[1], name)

        elif num_steps == 3:
            test_3_mod_clean(
                sas_task,
                data_num[0],
                data_num[1],
                data_num[2],
                name)

        elif num_steps == 4:
            test_4_mod_clean(
                sas_task,
                data_num[0],
                data_num[1],
                data_num[2],
                data_num[3],
                name)

        elif num_steps == 5:
            # new
            test_5_mod_clean(
                sas_task,
                data_num[0],
                data_num[1],
                data_num[2],
                data_num[3],
                data_num[4],
                name)
        else:
            raise NotImplementedError()

    with open(arg3, "w") as output_file:
        sas_task.output(output_file)

    # how many blocks

    # modify

    # store
