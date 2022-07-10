import argparse
import re
from client import Client
from command_class import Command
from socket import gethostbyname, gethostname
import DB

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def main():
    #BEFORE PREPARING THE UI
    parser = argparse.ArgumentParser()
    parser.add_argument('--addr_id', default = gethostbyname(gethostname()) + ":8080", help= "This is the address of the node that identifies it in the hash space.\nIf no address is set, this automatically set the local address asigned from the local network.")
    parser.add_argument('--addr_known', default = None, help = "This is an IP address that identifies reference a node in the network.\nIf you wanna join new nodes to an existing network, you have to enter this value, otherwise your node never bee connected to the network.")
    
    parser.add_argument('--v', action = "store_false", help = "This is the vocal option. You can see the activity of the node if you enter it.")
    
    matcher = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,6}")
    args = parser.parse_args()
    error_message = "The %s must have an IP:port like format first, and after that, because the code uses this info for the hash function, if you want\n to avoide colisions, you must enter an unique string. This %s is a bad input"
    if not matcher.fullmatch(args.addr_id.split()[0]) :
        parser.error(error_message %("addr_id", args.addr_id))
    if args.addr_known and not matcher.fullmatch(args.addr_known.split()[0]):
        parser.error(error_message %("addr_known", args.addr_known))
    


    chord_args = [args.addr_id, args.addr_known, args.v]

    
    cl = Client(args.addr_id, chord_args, None)
    #cl = None

    Flags_Dict = {'user':'','user_logged': False}
    print()
    print(color.BLUE + "WELCOME TO TWISTTER, OUR SOCIAL NETWORK."+ color.END)
    print()
    
    #Main app loop
    while True:
        #resetting flags
        Flags_Dict['correct_comd'] =  False
        #printing instructions
        PrintCycle(Flags_Dict)
        
        full_string = input()
        command = CleanCommand(full_string, Flags_Dict, cl)

        if Flags_Dict['correct_comd']:
            command.Execute(command.cm_name)
            pass
        else:
            continue
        
    



def PrintCycle(Flags_Dict: dict)->None:
    if(Flags_Dict['user'] == ''):
        print()
        print('You are not logged in to an account, please create or log into one to continue:')
        print()
        print('LogIn \'username\' \'password\'')
        print()
        print('CreateAccount \'username\' \'password\'')
        print()
        print(color.CYAN+'>' + color.END, end= ' ')
        return
    else:
        print()
        print('Introduce a command.\(\'help\' to see the full list \)')
        print(color.BLUE + Flags_Dict['user'] + color.CYAN +' > '+ color.END, end= ' ')
    return




def CleanCommand(full_string_comd: str ,Flags_Dict: dict , cl) -> Command:
    
    comd = full_string_comd.split(' ')
    filter(None, comd)
    comd[0] =comd[0].lower()
    if len(comd) == 1: comd.append('')
    if comd[0] == 'tweet':
        text=''
        for word in comd:
            if word == comd[0] and text=='':
                continue
            else:
                text+=word
                text+=' '
        comd[1] = text
        comd = comd[0:2]        
    
    if comd[0] == 'comment':
        text=''
        for word in comd:
            if (word == comd[0] or word == comd[1]) and text=='':
                continue
            else:
                text+=word
                text+=' '
        comd[2] = text
        comd = comd[0:3]     
    
    
    #Checking that the user is trying to log in or create an ccount
    if not Flags_Dict['user_logged'] and comd[0] !='login' and comd[0] != 'createaccount':
        return
    if not Flags_Dict['user_logged']: Flags_Dict['user'] = comd[1]
    
    
    #try :
    args = comd[1:len(comd)]
    args.append(Flags_Dict['user'])
    full_command = Command(comd[0], args, cl)
    #except: 
    #if not Flags_Dict['user_logged']: Flags_Dict['user'] = ' '
    #return
    
    Flags_Dict['correct_comd'] =True
    if not Flags_Dict['user_logged']: Flags_Dict['user_logged'] = True
    if full_command.cm_name == 'logout':
        if Flags_Dict['user_logged']: Flags_Dict['user'] = ''
        if Flags_Dict['user_logged']: Flags_Dict['user_logged'] = False
    return full_command




main()