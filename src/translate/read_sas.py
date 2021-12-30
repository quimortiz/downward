import sys
import sas_tasks
import timers
import pddl_parser
import normalize
import translate_utils
import options


def python_version_supported():
    return sys.version_info >= (3, 6)


if not python_version_supported():
    sys.exit("Error: Translator only supports Python >= 3.6.")


def cannonical_sas(sas):
    # make sure it is cannonical...
    return sas_tasks.SASTask(sas.variables,
                             [sas_tasks.SASMutexGroup(i.facts)
                              for i in sas.mutexes],
                             sas.init, sas.goal,
                             [sas_tasks.SASOperator(i.name, i.prevail, i.pre_post, i.cost) for i in sas.operators], sas.axioms, sas.metric)


def read_pddl(domain_filename, task_filename):

    # i have to do something with the args...  and the options module.
    # maybe set it all to defult? see the trick they use to define the options

    args = options.parse_args([domain_filename, task_filename])
    options.copy_args_to_module(args)

    # options.invariant_generation_max_candidates = 10000
    task = pddl_parser.open(
        domain_filename, task_filename)

    normalize.normalize(task)

    task = translate_utils.pddl_to_sas(task)
    task_canonical = cannonical_sas(task)
    task_canonical.validate()
    return task_canonical
    # return  task

    # make cannonical


def read_sas_task(filepath):
    #
    metric = 0
    variables = []
    mutexes = []
    state = []
    goal = []
    operators = []
    with open(filepath, 'r') as file_object:
        def readl():
            return file_object.readline()[:-1]

        def readi():
            return int(readl())

        def readis():
            l = readl().split()
            return [int(i) for i in l]

        # parse header
        assert(file_object.readline()[:-1] == "begin_version")
        assert(file_object.readline()[:-1] == "3")
        assert(file_object.readline()[:-1] == "end_version")
        assert(file_object.readline()[:-1] == "begin_metric")
        metric = int(file_object.readline()[:-1])
        assert(file_object.readline()[:-1] == "end_metric")

        num_vars = int(file_object.readline()[:-1])
        # reading the variables
        line = file_object.readline()[:-1]
        assert(line == "begin_variable")
        while (line == "begin_variable"):
            name_var = file_object.readline()[:-1]
            assert(file_object.readline()[:-1] == "-1")
            num_values = int(file_object.readline()[:-1])
            names = []
            for i in range(num_values):
                names.append(file_object.readline()[:-1])
            variables.append(names)
            assert(file_object.readline()[:-1] == "end_variable")
            line = file_object.readline()[:-1]
            print(line)
        assert (num_vars == len(variables))

        num_mutex = int(line)
        line = readl()
        # mutex
        # can i put and assert here?
        print("line", line)
        while line == "begin_mutex_group":
            mutex = []
            num_values = int(file_object.readline()[:-1])

            for i in range(num_values):
                line_list = file_object.readline().split()
                print(line_list)
                mutex.append((int(line_list[0]), int(line_list[1])))
            mutexes.append(mutex)
            assert(file_object.readline()[:-1] == "end_mutex_group")
            line = file_object.readline()[:-1]

        print(mutexes)

        # read begin state
        assert(line == "begin_state")
        for i in range(len(variables)):
            state.append(int(file_object.readline()[:-1]))
        assert(readl() == "end_state")

        # goal
        assert(readl() == "begin_goal")
        num_goal = readi()
        for i in range(num_goal):
            goal.append(tuple(readis()))
        assert(readl() == "end_goal")

        num_goal = readi()
        line = readl()
        while line == "begin_operator":
            operator = []
            var = []
            pre = []
            post = []
            cond = []
# var, pre, post, cond
            name = readl()
            num_prevail_cond = readi()
            prevail_conds = []
            entries = []
            for i in range(num_prevail_cond):
                prevail_conds.append(tuple(readis()))

            num_pre_post_cond = readi()
            # pre_post_cond  = []
            effects = []
            for i in range(num_pre_post_cond):
                line = readis()
                num_cond_effect = line[0]
                cond_effecti = []
                for i in range(num_cond_effect):
                    var_c = line[1 + 2 * i]
                    val_c = line[1 + 2 * i + 1]
                    cond_effecti.append(tuple((var_c, val_c)))
                assert (len(line[1 + 2 * num_cond_effect:]) == 3)
                vari, prei, posti = line[1 + 2 * num_cond_effect:]
                # var.append(vari)
                # pre.append(prei)
                # post.append(posti)
                # cond.append(cond_effecti)
                entries.append([vari, prei, posti, cond_effecti])
                # pre_post_cond.append( [var_pre_post , cond_effect]  )

            operator.append(name)
            operator.append(prevail_conds)
            # operator.append([var, pre, post, cond])
            operator.append(entries)
            assert(readi() == 1)
            operators.append(operator)
            assert(readl() == "end_operator")
            line = readl()

        assert(line == "0")

    print(metric)
    print(variables)
    print(mutexes)
    print(state)
    print(goal)
    print(operators)

    # self.ranges = ranges
    # self.axiom_layers = axiom_layers
    # self.value_names = value_names

    sas_variables = sas_tasks.SASVariables(
        [len(variable) for variable in variables], [-1 for variable in variables], variables)

    sas_init = sas_tasks.SASInit(state)
    sas_mutexes = [sas_tasks.SASMutexGroup(i) for i in mutexes]

    sas_goal = sas_tasks.SASGoal(goal)
    sas_metric = metric
    sas_operators = []
    sas_axioms = []

    print("operators")
    for i in operators:
        print(i[0], i[1], i[2], 1)

    sas_operators = [
        sas_tasks.SASOperator(
            " " + i[0] + " ",
            i[1],
            i[2],
            1) for i in operators]

    task = sas_tasks.SASTask(sas_variables, sas_mutexes, sas_init, sas_goal,
                             sas_operators, sas_axioms, sas_metric)

    # dump_statistics(task)
    return task
