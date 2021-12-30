#! /usr/bin/env python3
from modify_sas import *
from translate_utils import *
import pddl_parser
import read_sas
import options
import normalize
import sys
import traceback
import signal

def python_version_supported():
    return sys.version_info >= (3, 6)

if not python_version_supported():
    sys.exit("Error: Translator only supports Python >= 3.6.")


def main():
    timer = timers.Timer()
    with timers.timing("Parsing", True):
        task = pddl_parser.open(
            domain_filename=options.domain, task_filename=options.task)

    with timers.timing("Normalizing task"):
        normalize.normalize(task)

    if options.generate_relaxed_task:
        # Remove delete effects.
        for action in task.actions:
            for index, effect in reversed(list(enumerate(action.effects))):
                if effect.literal.negated:
                    del action.effects[index]

    sas_task = pddl_to_sas(task)
    dump_statistics(sas_task)

    with timers.timing("Writing output"):
        with open(options.sas_file, "w") as output_file:
            sas_task.output(output_file)
    print("Done! %s" % timer)


def main_play():
    timer = timers.Timer()
    with timers.timing("Parsing", True):
        task = pddl_parser.open(
            domain_filename=options.domain, task_filename=options.task)

    with timers.timing("Normalizing task"):
        normalize.normalize(task)

    if options.generate_relaxed_task:
        # Remove delete effects.
        for action in task.actions:
            for index, effect in reversed(list(enumerate(action.effects))):
                if effect.literal.negated:
                    del action.effects[index]

    # this seems important :)
    sas_task = pddl_to_sas(task)
    for i in sas_task.variables.value_names:
        print(i)

    data, data_raw = parse_sas_and_mod()




    data_num = get_data_num( sas_task , data_raw )

    print(data_num)

    # sys.exit()

    # i have problems with this sorted stuff...
    # how to enfore it?

    op = sas_task.operators[0]
    # [(0, 0)]
    # (0, 0)
    # (5, -1, 0, [])

    # i just have to modify this guys :)

    # note: forbid iterative solves the problems without condtional
    # note: what happens if the matched fact is changed with a condition?


    # state1 -> action -> state2

    # for the first state, i want to see the output of the action
    # problem:
    # state1 is bad i do action which gives state 2. but at the same time,
    # the action changes the atom of state1.

    # test 1: adds a variable to block that var4 has a value different that free.


    # TODO: transform this into a test :)

    if False:
        test_1_mod_clean(sas_task, [(4, 0)])  # block Atom carry(ball1, right)
        test_1_mod_clean(sas_task, [(4, 1)])  # Atom carry(ball2, right)
    elif False:
        # block var4:  Atom carry(ball1, right)   var5 :  Atom at(ball1, rooma),  Atom at(ball1, roomb)
        test_1_mod_clean(sas_task, [(4, 0), (5, 0)])
        # note: this should give the same plan!
    elif False:
        # lets say you can not carry ball 1 and 2 at the same time
        test_1_mod_clean(sas_task, [(4, 0), (1, 1)])  # still length 5
    elif False:
        # this should have length 7
        test_1_mod_clean(sas_task, [(4, 0), (1, 1)])
        test_1_mod_clean(sas_task, [(4, 1), (1, 0)])

    elif False:
        # this should have 5
        test_2_mod_clean(sas_task, [(4, 0)], [(5, 1)])
        # carry ball1 right , at ball1 roomb

    elif False:
        # this should have 7
        test_2_mod_clean(sas_task, [(4, 0)], [(5, 1)])
        # carry ball1 right , at ball1 roomb
        test_2_mod_clean(sas_task, [(4, 1)], [(6, 1)])
        # carry ball2 right , at ball2 roomb

    # lets try a sequence of 3

    elif False:
        # this should be 5 (robot doesnt have to come back)
        test_3_mod_clean(sas_task, [(4, 0)], [(5, 1)], [(0, 0)])
        test_3_mod_clean(sas_task, [(4, 1)], [(6, 1)], [(0, 0)])

    elif False:
        # this should be 7. i can use either right or left
        test_3_mod_clean(sas_task, [(4, 0)], [(1, 1)], [(0, 1)])
        test_3_mod_clean(sas_task, [(1, 1)], [(4, 0)], [(0, 1)])
        test_3_mod_clean(sas_task, [(4, 1)], [(1, 0)], [(0, 1)])
        test_3_mod_clean(sas_task, [(1, 0)], [(4, 1)], [(0, 1)])

        test_1_mod_clean(sas_task, [(1, 1)])
        test_1_mod_clean(sas_task, [(1, 0)])

    # TODO: what happens with init state?
    elif False:
        test_3_mod_clean(sas_task, [(4, 0)], [(1, 1)], [(0, 1)])
        test_3_mod_clean(sas_task, [(1, 1)], [(4, 0)], [(0, 1)])
        test_3_mod_clean(sas_task, [(4, 1)], [(1, 0)], [(0, 1)])
        test_3_mod_clean(sas_task, [(1, 0)], [(4, 1)], [(0, 1)])

        test_1_mod_clean(sas_task, [(1, 1)])
        test_1_mod_clean(sas_task, [(1, 0)])

    elif False:
        test_1_mod_clean(sas_task, [(0, 0)])

    elif True:
        test_1_mod_clean(sas_task, [(0, 1), (1, 3)])

    #  some mutex are unorderd. TODO: solve!
    # Problems with pre_post
    # sas_task.validate()

    dump_statistics(sas_task)

    with timers.timing("Writing output"):
        with open(options.sas_file, "w") as output_file:
            sas_task.output(output_file)
    print("Done! %s" % timer)


def handle_sigxcpu(signum, stackframe):
    print()
    print("Translator hit the time limit")
    # sys.exit() is not safe to be called from within signal handlers, but
    # os._exit() is.
    os._exit(TRANSLATE_OUT_OF_TIME)


if __name__ == "__main__":
    experiment = False
    options.setup()
    if experiment: 
        read_sas.read_sas_task("output.sas")
        parse_sas_and_mod()
        sys.exit()
    try:
        signal.signal(signal.SIGXCPU, handle_sigxcpu)
    except AttributeError:
        print("Warning! SIGXCPU is not available on your platform. "
              "This means that the planner cannot be gracefully terminated "
              "when using a time limit, which, however, is probably "
              "supported on your platform anyway.")
    try:
        # Reserve about 10 MB of emergency memory.
        # https://stackoverflow.com/questions/19469608/
        emergency_memory = b"x" * 10**7
        main()
    except MemoryError:
        del emergency_memory
        print()
        print("Translator ran out of memory, traceback:")
        print("=" * 79)
        traceback.print_exc(file=sys.stdout)
        print("=" * 79)
        sys.exit(TRANSLATE_OUT_OF_MEMORY)
