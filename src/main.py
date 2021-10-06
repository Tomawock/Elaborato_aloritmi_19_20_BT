import argparse
import time
import json
import pickle
import my_logger
import espressione_regolare
import espressioni_regolari
import \
    spazio_comportamentale, spazio_comportamentale_osservabile, diagnostica, \
    diagnosi_relativa_osservazione, diagnosi_lineare


def execute(args, input_read):
    ts = time.asctime(time.localtime(time.time()))[11:19]
    x = args.task[0]
    if args.json:
        if x == 0:
            logger = my_logger.Logger(
                "log/espressione_regolare" + "_" + str(ts)).get_logger()
            espressione_regolare.start_execution(input_read[0])
        elif x == 1:
            logger = my_logger.Logger(
                "log/espressioni_regolari" + "_" + str(ts)).get_logger()
            espressioni_regolari.start_execution(input_read[0])
        elif x == 2:
            logger = my_logger.Logger(
                "log/spazio_comportamentale" + "_" + str(ts)).get_logger()
            spazio_comportamentale.start_execution(
                input_read[0], input_read[1], input_read[2])  # fa, transition, original_link
        elif x == 3:
            logger = my_logger.Logger(
                "log/spazio_comportamentale_osservabile" + "_" + str(ts)).get_logger()
            # fa, transition, original_link, observation list
            spazio_comportamentale_osservabile.start_execution(
                input_read[0], input_read[1], input_read[2], input_read[3])
        elif x == 4:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione" + "_" + str(ts)).get_logger()
            # fa, transition, original_link, observation_list
            diagnosi_relativa_osservazione.start_execution(
                input_read[0], input_read[1], input_read[2], input_read[3])
        elif x == 5:
            logger = my_logger.Logger(
                "log/diagnostica" + "_" + str(ts)).get_logger()
            # fa, transition, original_link
            diagnostica.start_execution(
                input_read[0], input_read[1], input_read[2])
        elif x == 6:
            logger = my_logger.Logger(
                "log/diagnosi_lineare" + "_" + str(ts)).get_logger()
            # fa, transition, original_link
            diagnosi_lineare.start_execution(
                input_read[0], input_read[1], input_read[2], input_read[3])
        else:
            print("ERROR: there was an index input error")
    elif args.bin:
        if x == 7:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_spazio_comportamentale_osservabile" + "_" + str(ts)).get_logger()
            # posso richiamare diagnosi_relativa_osservazione partendo dall'observable graph
            diagnosi_relativa_osservazione.start_execution_from_serialized_obs_graph(
                input_read[0][0], input_read[0][1])  # observation_graph, finals_states
        elif x == 8:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_spazio_comportamentale" + "_" + str(ts)).get_logger()
            diagnostica.start_execution_from_serialized_behave_space(
                input_read[0][0])  # [0][0]identifing the behavioral_state_graph
        elif x == 9:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_silent_closure_space" + "_" + str(ts)).get_logger()
            diagnostica.start_execution_from_serialized_silent_space(
                input_read[0])
        elif x == 10:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_spazio_comportamental" + "_" + str(ts)).get_logger()
            diagnosi_lineare.start_execution_from_serialized_behave_space(
                input_read[0][0], input_read[1])
        elif x == 11:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_silent_closure_space" + "_" + str(ts)).get_logger()
            diagnosi_lineare.start_execution_from_serialized_silent_space(
                input_read[0], input_read[1])
        elif x == 12:
            logger = my_logger.Logger(
                "log/diagnosi_relativa_osservazione_from_diagnostic_graph" + "_" + str(ts)).get_logger()
            diagnosi_lineare.start_execution_from_serialized_diagnostic_graph(
                input_read[0], input_read[1])

        else:
            print("ERROR: there was an index input error")

    """
    TO DO if-else per file binario
    """


if __name__ == '__main__':

    desc = ""

    argParser = argparse.ArgumentParser(description=desc)
    argGroup = argParser.add_argument_group(title='Command List')
    argGroup.add_argument('-t', '--task', dest='task', required=True, nargs=1, type=int,
                          choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], help='Specify the task to be accomplished.')
    argGroup.add_argument('--json', dest='json', nargs='+', type=argparse.FileType(
        'r'), help='File containing the json object')  # quanti file json ci servono?
    argGroup.add_argument('--bin', dest='bin', nargs=1, type=argparse.FileType(
        'rb'), help='File containing the binary structure')
    argGroup.add_argument('-O', '--obs-list', dest='obs_list', action='append')

    args = argParser.parse_args()

    input_read = []
    if args.bin:
        lines = [line.strip() for line in args.bin[0].name]
        line = ''.join(line for line in lines)
        with open(line, 'rb') as f:
            input_read.append(pickle.load(f))
    elif args.json:
        for i in range(len(args.json)):
            print(i)
            lines = [line.strip() for line in args.json[i].name]
            line = ''.join(line for line in lines)
            with open(line) as f:
                input_read.append(json.load(f))

    if args.obs_list:
        arr = args.obs_list[0].split(',')
        input_read.append(arr)

    print("EXECUTING...")
    execute(args, input_read)
