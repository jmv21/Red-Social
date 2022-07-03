import re
from command_class import Command

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
    
    Flags_Dict = {'user':''}
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
        command = CleanCommand(full_string, Flags_Dict)

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




def CleanCommand(full_string_comd: str ,Flags_Dict: dict ) -> Command:
    
    comd = full_string_comd.split(' ')
    filter(None, comd)
    comd[0] =comd[0].lower()
    if len(comd) == 1: comd.append('')
    
    #Checking that the user is trying to log in or create an ccount
    if Flags_Dict['user'] == '' and comd[0] !='login' and comd[0] != 'createaccount':
        return
    
    
    try :full_command = Command(comd[0], comd[1:len(comd) -1]) 
    except: 
        return
    
    Flags_Dict['correct_comd'] =True
    return full_command




main()