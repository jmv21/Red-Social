#from numpy import str_


from DB import tweet
from run_app_client import color

class Command:
    #Nombre del comando
    cm_name = ""
    #Argumentos del comando
    cm_args = []

    
    def __init__(self,string_comand:str , args, client) -> None:
        self.cm_name = self.CheckNames(string_comand)
        self.cm_args = self.CheckArgs(self.cm_name,args)
        self.client = client
        print()
    
    def CheckNames(self,string_comand:str) -> str:
        
        if(string_comand == 'help'):
            return string_comand 
        elif(string_comand == 'login'):
            return string_comand 
        elif(string_comand == 'logout'):
            return string_comand 
        elif(string_comand == 'random'):
            return string_comand 
        elif(string_comand == 'update'):
            return string_comand 
        elif(string_comand == 'like'):
            return string_comand 
        elif(string_comand == 'comment'):
            return string_comand 
        elif(string_comand == 'retweet'):
            return string_comand 
        elif(string_comand == 'lookuser'):
            return string_comand 
        elif(string_comand == 'looktweet'):
            return string_comand 
        elif(string_comand == 'followuser'):
            return string_comand 
        elif(string_comand == 'info'):
            return string_comand 
        elif(string_comand == 'createaccount'):
            return string_comand 
        elif(string_comand == 'tweet'):
            return string_comand 
        
        print("\n Sorry,the command "+string_comand+" does not exist")
        raise Exception("Sorry,command not detected")
    
    
    def CheckArgs(self,string_comand:str, args):
    
        if(string_comand == 'help'):
            return [] 
        elif(string_comand == 'login'): 
            return args[0:3]
        elif(string_comand == 'logout'):
            return args[0:1]
        elif(string_comand == 'random'):
            return args[0:1]
        elif(string_comand == 'update'):
            return args[0:1] 
        elif(string_comand == 'like'):
            return args[0:2] 
        elif(string_comand == 'comment'):
            return args[0:3]  
        elif(string_comand == 'retweet'):
            return args[0:3]
        elif(string_comand == 'lookuser'):
            return args[0:2]
        elif(string_comand == 'looktweet'):
            return args[0:2]
        elif(string_comand == 'followuser'):
            return args[0:2]
        elif(string_comand == 'info'):
            return args[0:2]
        elif(string_comand == 'createaccount'):
            return args[0:3]
        elif(string_comand == 'tweet'):
            return args[0:2] 
    
        print("\n Sorry,the command "+string_comand+" does not expected does arguments")
        raise Exception("Sorry,wrong arguments")
    
    
    def Execute(self,string_comand:str) -> str:
        
        if(string_comand == 'help'):
            pass
        elif(string_comand == 'login'):
            success, token = self.client.login(self.cm_args[0], self.cm_args[1])
            pass
        elif(string_comand == 'logout'):
            self.client.token = None
            pass
        elif(string_comand == 'random'):
            tweets = self.client.random_n(self.cm_args[10])
            print()
            print(color.BLUE+'PRINTING LAST 10 RANDOM TWEETS'+color.END)
            for tweet in tweets:
                print()
                print(color.BLUE +"User: "+ color.CYAN+ tweet['user_name'] +"    |    "+color.BLUE+ "Date: "+color.CYAN+ tweet['timestamp'] +color.END)
                print(color.BLUE +"Text: "+ color.END+ tweet['content'])
                print(color.BLUE +"Likes: "+ color.CYAN+ tweet['likes']+"    |    "+color.BLUE+ "ID: "+color.CYAN+ tweet['id'] +color.END)
                print()
            pass
        elif(string_comand == 'update'):
            tweets = self.client.followed_tweets()
            print()
            print(color.BLUE+'PRINTING TWEETS FROM MY FOLLOWS'+color.END)
            for tweet in tweets:
                print()
                print(color.BLUE +"User: "+ color.CYAN+ tweet['user_name'] +"    |    "+color.BLUE+ "Date: "+color.CYAN+ tweet['timestamp'] +color.END)
                print(color.BLUE +"Text: "+ color.END+ tweet['content'])
                print(color.BLUE +"Likes: "+ color.CYAN+ tweet['likes']+"    |    "+color.BLUE+ "ID: "+color.CYAN+ tweet['id'] +color.END)
                print()
            pass
        elif(string_comand == 'like'):
            pass
        elif(string_comand == 'comment'):
            self.client.comment()
            pass
        elif(string_comand == 'retweet'):
            self.client.retweet()
            pass
        elif(string_comand == 'tweet'):
            pass
        elif(string_comand == 'lookuser'):
            pass
        elif(string_comand == 'looktweet'):
            pass
        elif(string_comand == 'followuser'):
            pass
        elif(string_comand == 'info'):
            pass
        elif(string_comand == 'createaccount'):
            success, token = self.client.register(self.cm_args[0], self.cm_args[1])
            pass 
        
    
    
    
    
    
    
    
    # ####AQUI DENTRO DE ESTOS METODOS DEBO HACER LOS RESPECTIVOS REQUESTS DE LOS DATOS PARA LUEGO USARLOS,
    # ####LA VARIABLE self.cm_args[] DE LA CLASE ES LA LISTA DE LOS ARGUMENTOS (EN STRING TODOS, PORQUE NO SE COMO TRABAJAN LOS IDS EN LA BD, 
    # # Ademas asume que el ultimo "args[-1]" , es el username del usuario que esta ejecutando el comando)
    
    # #a partir de aqui solo voy a poner los n-1 argumetos de self.cm_arg, recuerda, el n es el username
    # ###self.args[0] = username , self.args[1] = password
    # def Execute(self, command = 'login'):
    #     success, token = self.client.login(self.cm_args[0], self.cm_args[1])
    #     print("did it {}".format(token))
    #     pass
    
    
    # ###ESTO NO SE SI LO MANEJA LA BASE DE DATOS, O LO HAGO YO A NIVEL DE CLIENTE(Me parece que hacerlo yo no esta mal aunque puede dar bateo)
    # ###self.cm_args = [] ,  No recibe argumentos, dime si hace falta alguno 
    # def Execute(self, command = 'logout'):
    #     self.client.token = None
    #     pass
    
    # ####EL REQUEST DEBE DEVOLVER n TWEETS RANDOMS
    # ###self.cm_args = [] ,  No recibe argumentos, dime si hace falta alguno
    # def Execute(self, command = 'random'):
    #     tweets = self.client.random_n(self.cm_args[0])
    #     pass
    
    # ####EL REQUEST DEBE DEVOLVER n TWEETS DE LOS SEGUIDORES DEL USURAIO
    # ###self.cm_args = [] ,  No recibe argumentos, dime si hace falta alguno
    # def Execute(self, command = 'update'):
    #     tweets = self.client.followed_tweets()
    #     pass
    
    # ####EL REQUEST DEBE DAR LIKE AL TWEET
    # ###self.args[0] = tweetID  
    # def Execute(self, command = 'like'):

    #     pass
    
    # ####EL REQUEST DEBE ANADIR COMENTARIO TEXT AL TWEET
    # ###self.args[0] = tweetID, ###self.args[1] = 'TEXT'  
    # def Execute(self, command = 'comment'):
    #     self.client.comment() # + args
    #     pass
    
    # ####EL REQUEST DEBE DAR RETWEET AL TWEET
    # ###self.args[0] = tweetID,  
    # def Execute(self, command = 'retweet'):
    #     self.client.retweet() # + args
    #     pass
    
    # ####EL REQUEST DEBE BUSCAR EL USER CON EL ID
    # ###self.args[0] = userID, 
    # def Execute(self, command = 'lookuser'):
    #     pass
    
    # ####EL REQUEST DEBE BUSCAR EL TWEET CON EL ID
    # ###self.args[0] = tweetID, 
    # def Execute(self, command = 'looktweet'):
    #     pass
    
    # ####EL REQUEST DEBE SEGUIR AL USER CON EL ID
    # ###self.args[0] = userID, 
    # def Execute(self, command = 'followuser'):
    #     pass
    
    # ####EL REQUEST DEBE DEVOLVER INF0 SOBRE EL USER O TWEET CON EL ID
    # ###self.args[0] = ID, 
    # def Execute(self, command = 'info'):
    #     pass
    
    # ####EL REQUEST DEBE CREAR UN ACCOUNT
    # ###self.args[0] = username , self.args[1] = password
    # def Execute(self, command = 'createaccount'):
    #     #print(self.cm_args)#[0])
    #     success, token = self.client.register(self.cm_args[0], self.cm_args[1])
    #     pass