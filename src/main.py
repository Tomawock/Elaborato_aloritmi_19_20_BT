import argparse
import sys
import json
import espressione_regolare, espressioni_regolari, \
spazio_comportamentale, spazio_comportamentale_osservabile, diagnostica, \
diagnosi_relativa_osservazione, diagnosi_lineare


def execute(args, input_read):
    # options ={
    # 1: ComportamentalFANSpace, #noi non abbiamo questi oggetti che rappresentano gli spazi ComportamentalFANSObservation
    # 2: ComportamentalFANSObservation,
    # }

    #if isinstance(input_read, )
    if args.task[0]==1:
        espressione_regolare.espressione_regolare(input_read)


if __name__ == '__main__':

    print('main started')
    desc = "ddddd"

    argParser=argparse.ArgumentParser(description=desc)
    argGroup=argParser.add_argument_group(title='Command List')
    argGroup.add_argument('-t', '--task', dest='task', required=True, nargs=1, type=int, choices=[1,2],\
                            help='Specify the task to be accomplished.')
    argGroup.add_argument('--json', dest='json', nargs=1,type=argparse.FileType('r'), help='File containing the json object') #quanti file json ci servono?
    argGroup.add_argument('--bin', dest='bin', nargs=1, type=argparse.FileType('rb'), help='File containing the binary structure')
    #argGroup.add_argument('-o', '--out-file', dest='out_file', nargs=1, type=argparse.FileType('w+'), required=True)
    argGroup.add_argument('-O', '--obs-list', dest='obs_list', action='append')
    argGroup.add_argument('-d', '--diagnosis', dest='diagnosis', action='store_true')
    argGroup.add_argument('-T', '--max-time', dest='max_time', type=float, nargs=1, action='append', help="Max execution time in seconds")

    print('argument parsed')

    args=argParser.parse_args()

    # if not args.json:
    #     print('ERROR: use json option')
    #     sys.exit()
    # else:
    lines = [line.strip() for line in args.json[0]]
    line = ''.join(line for line in lines)
    with open(line) as f:
      input_read = json.load(f)
    #input_read = json.loads(''.join(line for line in lines))

    execute(args, input_read)
