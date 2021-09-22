import argparse
import sys
import json
import espressione_regolare, espressioni_regolari, \
spazio_comportamentale, spazio_comportamentale_osservabile, diagnostica, \
diagnosi_relativa_osservazione, diagnosi_lineare


def execute(args, input_read):
    # print(args.task[0])
    # options ={
    # 0: EspressioneRegolare(input_read),
    # # 1: EspressioniRegolari(input_read),
    # # 2: SpazioComportamentale(input_read),
    # # 3: SpazioComportamentaleOsservabile(input_read),
    # # 4: DiagnosiRelativaOsservazione(input_read),
    # # 5: Diagnostica(input_read),
    # # 6: DiagnosiLineare(input_read),
    # }
    #
    # options[args.task[0]]()
    x=args.task[0]
    if args.json:

        if x==0:
            espressione_regolare.start_execution(input_read)

        elif x==1:
            espressioni_regolari.start_execution(input_read)

        elif x==2:
            spazio_comportamentale.start_execution(input_read[0], input_read[1], input_read[2]) # fa, transition, original_link

        elif x==3:
            spazio_comportamentale_osservabile.start_execution(input_read[0], input_read[1], input_read[2], input_read[3]) # fa, transition, original_link, observation list

        elif x==4:
            diagnosi_relativa_osservazione.start_execution(input_read[0], input_read[1], input_read[2], input[3]) # fa, transition, original_link, observation_list

        elif x==5:
            diagnostica.start_execution(input_read[0], input_read[1], input_read[2]) # fa, transition, original_link

        elif x==6:
            diagnosi_lineare.start_execution(input_read[0], input_read[1], input_read[2], input_read[3]) # fa, transition, original_link

        #}
    # elif args.bin:
    #     switch(args.task[0]){
    #         case 4: diagnosi_relativa_osservazione.diagnosi_relativa_osservazione(input_read[0], input_read[1])# observable-graph, final_states
    #             break
    #         case 5: diagnostica.diagnostica(input_read[0]) #generate diagnostic graph from silent space
    #             break
    #         case 6: diagnosi_lineare.diagnosi_lineare(input_read[0], input_read[1]) #generate linear diagnostic from diagnostic graph and linear observation
    #             break
    #         default: print("there was an error")
    #             break
    #     }

    #switch caricament binary file

    # case 4: diagnosi_relativa_osservazione.diagnosi_relativa_osservazione(input_read[0], input_read[1])# observable-graph, final_states
    #     break
    # case 5: diagnostica.diagnostica(input_read[0]) #generate diagnostic graph from silent space
    #         break
    # case 6: diagnosi_lineare.diagnosi_lineare(input_read[0], input_read[1]) #generate linear diagnostic from diagnostic graph and linear observation
    #         break

# def EspressioneRegolare(input_read):
#     print("helo")
#     #espressione_regolare.start_execution(input_read)
# def EspressioniRegolari(input_read):
#     espressioni_regolari.start_execution(input_read)
# def SpazioComportamentale(input_read):
#     spazio_comportamentale.start_execution(input_read[0], input_read[1], input_read[2])
# def SpazioComportamentaleOsservabile(input_read):
#     spazio_comportamentale_osservabile.start_execution(input_read[0], input_read[1], input_read[2], input_read[3])
# def DiagnosiRelativaOsservazione(input_read):
#     diagnosi_relativa_osservazione.start_execution(input_read[0], input_read[1], input_read[2], input[3])
# def Diagnostica(input_read):
#     diagnostica.start_execution(input_read[0], input_read[1], input_read[2])
# def DiagnosiLineare(input_read):
#     diagnosi_lineare.start_execution(input_read[0], input_read[1], input_read[2], input_read[3])

if __name__ == '__main__':

    desc = "ddddd"

    argParser=argparse.ArgumentParser(description=desc)
    argGroup=argParser.add_argument_group(title='Command List')
    argGroup.add_argument('-t', '--task', dest='task', required=True, nargs=1, type=int, \
    choices=[0,1,2,3,4,5,6], help='Specify the task to be accomplished.')
    argGroup.add_argument('--json', dest='json', nargs=3,type=argparse.FileType('r'), help='File containing the json object') #quanti file json ci servono?
    argGroup.add_argument('--bin', dest='bin', nargs=1, type=argparse.FileType('rb'), help='File containing the binary structure')
    #argGroup.add_argument('-o', '--out-file', dest='out_file', nargs=1, type=argparse.FileType('w+'), required=True)
    argGroup.add_argument('-O', '--obs-list', dest='obs_list', action='append')
    argGroup.add_argument('-d', '--diagnosis', dest='diagnosis', action='store_true')
    argGroup.add_argument('-T', '--max-time', dest='max_time', type=float, nargs=1, action='append', help="Max execution time in seconds")


    args=argParser.parse_args()

    # if not args.json:
    #     print('ERROR: use json option')
    #     sys.exit()
    # else:
    input_read=[]
    print("JSON", args.json[1].name)
    for i in range (len(args.json)):
        lines = [line.strip() for line in args.json[i].name]
        line = ''.join(line for line in lines)
        print("line from args.json", line)
        with open(line) as f:
          input_read.append(json.load(f))
        #input_read = json.loads(''.join(line for line in lines))

    if args.obs_list:
        arr = args.obs_list[0].split(',')
        input_read.append(arr)
    execute(args, input_read)
