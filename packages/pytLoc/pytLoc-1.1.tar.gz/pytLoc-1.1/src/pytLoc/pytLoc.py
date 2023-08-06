
import sys, os, re, hashlib
from sys import platform
from datetime import datetime

dico_chr_spec={0:"?", 1:";",2:"-", 3:"+", 4:".", 5:"=", 6:"(", 7:")", 8:"[", 9:"]", 10:":", 11:"_", 12:"\"", 13:"\'", 14:"#", 15:"*", 16:">", 17:"<", 18:",", 19:"%", 20:"$", 21:"!", 22:"&", 23:"/", 24:"\\", 25:"|"}
dico_chr_alpha_min={26:"a", 27:"b", 28:"c", 29:"d", 30:"e", 31:"f", 32:"g", 33:"h", 34:"i", 35:"j", 36:"k", 37:"l", 38:"m", 39:"n", 40:"o", 41:"p", 42:"q", 43:"r", 44:"s", 45:"t", 46:"u", 47:"v", 48:"w", 49:"x", 50:"y", 51:"z"}
dico_chr_alpha_maj={52:"A", 53:"B", 54:"C", 55:"D", 56:"E", 57:"F", 58:"G", 59:"H", 60:"I", 61:"J", 62:"K", 63:"L", 64:"M", 65:"N", 66:"O", 67:"P", 68:"Q", 69:"R", 70:"S", 71:"T", 72:"U", 73:"V", 74:"W", 75:"X", 76:"Y", 77:"Z", 78:" "}
dico_chr_num={79:"0", 80:"1", 81:"2", 82:"3", 83:"4", 84:"5", 85:"6", 86:"7", 87:"8", 88:"9", 89:"\n", 90:"@",  91:"{", 92:"}"}

dico_chr=dico_chr_spec|dico_chr_alpha_min|dico_chr_alpha_maj|dico_chr_num

dico_ord_spec={"?":0, ";":1, "-":2, "+":3, ".":4, "=":5, "(":6, ")":7, "[":8, "]":9, ":":10, "_":11, "\"":12, "\'":13, "#":14, "*":15, ">":16, "<":17, ",":18, "%":19, "$":20, "!":21, "&":22, "/":23, "\\":24, "|":25}
dico_ord_alpha_min={"a":26, "b":27, "c":28, "d":29, "e":30, "f":31, "g":32, "h":33, "i":34, "j":35, "k":36, "l":37, "m":38, "n":39, "o":40, "p":41, "q":42, "r":43, "s":44, "t":45, "u":46, "v":47, "w":48, "x":49, "y":50, "z":51}
dico_ord_alpha_maj={"A":52, "B":53, "C":54, "D":55, "E":56, "F":57, "G":58, "H":59, "I":60, "J":61, "K":62, "L":63, "M":64, "N":65, "O":66, "P":67, "Q":68, "R":69, "S":70, "T":71, "U":72, "V":73, "W":74, "X":75, "Y":76, "Z":77, " ":78}
dico_ord_num={"0":79, "1":80, "2":81, "3":82, "4":83, "5":84, "6":85, "7":86, "8":87, "9":88, "\n":89, "@":90, "{":91, "}":92}
dico_ord=dico_ord_spec|dico_ord_alpha_min|dico_ord_alpha_maj|dico_ord_num


def hash_pass(*args, **kwargs)->str:
    """ function that computes the hash of the passphrase
        or of the list of passphrases.
        1- E.g: hash_pass("mbote ya ngue") 
        2- E.g: hash_pass("passhrase1", "passp2")
    """
    hasher, ofefe = hashlib.sha3_512(), ""
    for key_word in args:
        hasher.update(key_word.encode("utf-8"))
        ofefe+=hasher.hexdigest()
    return ofefe

class pytLoc:
    """ This class represents the heart of pytLoc.
        USAGE: from pytLoc import pytLoc
               pytLoc.pytLoc(*args).[method]
               e.g. pytLoc.pytLoc("file.py").loc("password")
        It takes optionnal arguments:
        -either a list of file names in the current working directory. E.g: pytLoc.pytLoc("file1.py") or pytLoc("file1.py", "file2.py")
        -either "." to obfuscate all python files in the current working directory. E.g: pytLoc.pytLoc(".").loc(key)
        -either "*" to obfuscate all python files in the current working directory and in its subfolders. E.g: pytLoc.pytLoc("*").loc(key)
        -either "***" to obfuscate all python source code files stored in the entire disk. E.g: pytLoc.pytLoc("***").loc(key)
        key --> the key is a string: a phrase or key string or a list of words or strings. E.g: key="hello"; key="hello, h*cb45#".
        METHODS:
        genKey(key, leng) --> generates a one time pad of length "leng" key from a the key "key".
                This key is generated randomly using the secure hash algorithm with 512 bits. To do so, 
                it uses the composition function of functions initialized at sha512(key) concatenated with 
                the footprints of consecutive concatenation of footprints up to the length "leng".
        loc(key) --> locks / obfuscates python files indicated in pytLoc with the one time pad key generated from
                the key "Key"
        unloc(key)       --> unlocks / de-obfuscates python files indicated in pytLoc with the one time pad key generated
                             from the key "Key".
        genKey(key, len) --> generates a one time pad security key of length len derived from key.
        sig(file)        --> computes a hash of file.
        check(file)      --> function that checks the integrity of a locked python source.
        E.g: 1- obfuscatE A PYTHON FILE or PYTHON FILES IN THE CURRENT WORKING DIRECTORY
                to obfuscatE the file "file1.py" located in the current working directory with the one time pad generated from key "hello",
                --> pytLoc.pytLoc("file1.py").loc("hello") which generates the file "LOCKED_file1.py" in the same directory. This file is obfuscated.
                to DE-obfuscatE the file "LOCKED_file1.py" located in the current working directory with the one time pad generated from key "hello",
                --> pytLoc.pytLoc("LOCKED_file1.py").unlock("hello") which generates back the file "UNLOCKED_file1.py" which is equal to "file1.py" in the same 
                    directory.
             2- obfuscatE ALL PYTHON FILES LOCATED IN THE CURRENT WORKING DIRECTORY
                to obfuscatE all python files located in the current working directory with the one time pad generated from the key "hello",
                --> pytLoc.pytLoc(".").loc("hello") which generates the files "LOCKED_....py" in the same directory. These files are obfuscated.
                to DE-obfuscatE all the obfuscated python files "LOCKED_....py" located in the current working directory with the one time pad generated from
                the key "hello", 
                --> pytLoc.pytLoc(".").unlock("hello") which generates back the files "UNLOCKED_....py" in the same directory.
             3- obfuscatE ALL PYTHON FILES LOCATED IN THE CURRENT WORKING DIRECTORY AND ITS SUB-DIRECTORIES
                to obfuscatE all python files located in the current working directory and its sub-directories with the one time pad generated from the key "hello",
                --> pytLoc.pytLoc("*").loc("hello") which generates the files "LOCKED_....py" in current working directory and all its corresponding sub-directories.
                to DE-obfuscatE all python files located in the current working directory and its sub-directories, 
                --> pytLoc.pytLoc("*").unlock("hello") which generates the files "UNLOCKED....py" in the current working directory and all its corresponding sub-directories.
             4- obfuscatE ALL PYTHON FILES LOCATED IN THE ENTIRE DRIVE PARTITION
                to obfuscatE all python files located in the entire drive partition with the one time pad generated from the key "hello",
                --> pytLoc.pytLoc("***").loc("hello") which generates the files "LOCKED_....py" in wherever directory or sub-directory where python files are found.
                to DE-obfuscatE all python files located in the entire drive partition with the one time pad generated from the key "hello",
                --> pytLoc.pytLoc("***").unlock("hello) which generates the files "UNLOCKED....py" in wherever directory or sub-directory where locked python files are found.
                For more info visit https://github.com/GildaRech/pytLoc/ or https://github.com/GildaRech/pytLoc/issues to report a bug.
            NOTE: when calling pytLoc without parameter delete, the default delete=False is considered (E.g pytLoc.pytLoc("file1.py").loc(key) or
              pytLoc.pytLoc("file1.py", delete=False).loc(key) ), the original files are not deleted. and with parameter delete=True, original files are deleted
    """
    def __init__(self, *args:str, delete=False):
        self.args=args; self.delete=delete
        if not self.args:
            raise Exception("Please specify file names or the keywords. Please read the documentation")
        if not self.delete or self.delete==False:
            self.cmd=""
        elif self.delete==True:
            self.cmd="del /f "
        else:
            raise Exception("Invalid argument on delete.")

    def genKey(self, key, leng):
        """ generation of the key"""
        self.key, self.leng = key, leng
        self.bravo=hash_pass(key)
        if self.leng<=len(self.bravo):
            return self.bravo[:self.leng]
        else:
            while (self.leng>len(self.bravo)): 
                self.bravo+=hash_pass(self.bravo)
            return self.bravo[:self.leng]

    def sig(self, file):
        """function that returns a 256 bit signature"""
        self.file=file
        self.signature = hashlib.sha256()
        with open(self.file,"rb") as file:
            for data in iter(lambda:file.read(2048), b""):
                self.signature.update(data)
            return self.signature.hexdigest()

    def check(self, file):
        """function that checks the integrity of a locked python source """
        self.signature=self.sig(file); self.file=file
        files_folders=os.listdir(os.getcwd())
        for self.file_name in files_folders:
            if self.file_name.endswith("_signature.txt"):
                with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                    self.content=open_f.read()
                    if self.content==self.signature:
                        print("Integrity test SUCCESSFUL")
                        sys.exit()
                    else:
                        print("Integrity test FAILED. File content may have been MODIFIED")
                        sys.exit()
        print("Signature file not found in this directory")
        sys.exi()
              
    def obfuscate(self, content, key)->str:
        """obfuscation function"""
        self.key=key; self.content=content; self._=""
        for i in range(len(self.key)):
            self.p_k=dico_ord[self.key[i]]
            try:
                self.p_p=dico_ord[self.content[i]]
            except:
                raise Exception("The character "+str(self.content[i])+" DOES NOT EXIST in the dictionary dico_ord \n Please add it and/or report it")
            self._+=dico_chr[(self.p_p+self.p_k)%93]
        return self._

    def de_obfuscate(self, content, key):
        """de-obfuscation funtion"""
        self.content=content; self.key=key; self._=""
        for i in range(len(self.key)):
            self.p_k=dico_ord[key[i]]
            try:
                self.p_c=dico_ord[self.content[i]]
            except:
                raise("The character "+str(self.content[i])+" DOES NOT EXIST in the dictionnaries\n Please add it and/or report it")
            self._+=dico_chr[(self.p_c-self.p_k)%93]
        return self._
    
    def dir_walk(self, dir, share=False):
        """ function that walks through directories for python files while locking files"""
        self.share=share
        if not self.share or self.share==False:
            self.export=""
        else:
            self.export=True
        self.contents = os.listdir(dir) 
        for self.element in self.contents:   
            if os.path.isdir(self.element):
                os.chdir(os.path.abspath(self.element))
                self.dir_walk(os.getcwd())
            else:
                if self.element.endswith(".py"):
                    with open(str(self.element), mode="r", encoding="utf-8") as open_f:
                        self.content=open_f.read()
                        self.leng=len(self.content)
                        open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.name="LOCKED_"+str(self.element.replace(".py", ""))+".py"
                    self.output = open(self.name, "w")
                    self.target=self.obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.element))
                    if self.export==True:
                        self.ntangu=datetime.now()
                        self.mbote=self.ntangu.strftime("_%d_%m_%Y_(time_%H_%M_%S)")
                        self.t=str(self.element.replace(".py", ""))+str(self.mbote)
                        os.system("mkdir SHARE_"+self.t)
                        with open("SHARE_"+self.t+"\\"+str(self.element.replace(".py", ""))+"_signature.txt", "w") as f:
                            f.write(self.sig(self.name))
                            f.close()
                            os.system("copy "+str(self.name)+" SHARE_"+self.t)
        return "LOCKED_"+str(self.element.replace(".py", ""))+".py"

    def dir_walk_U(self, dir):
        """ function that walks in directories for python files while unlocking locked files """
        self.contents = os.listdir(dir) 
        for self.element in self.contents:   
            if os.path.isdir(self.element):
                os.chdir(os.path.abspath(self.element))
                self.dir_walk_U(os.getcwd())
            else:
                if self.element.startswith("LOCKED_") and self.element.endswith(".py"):
                    with open(str(self.element), mode="r", encoding="utf-8") as open_f:
                        self.content=open_f.read()
                        self.leng=len(self.content)
                        open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output = open("UNLOCKED_"+str(self.element[7:].replace(".py", ""))+".py", "w")
                    self.target=self.de_obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.element))
        return "UNLOCKED_"+str(self.element[7:].replace(".py", ""))+".py"

    def loc(self, key, share=False):
        """ function that locks / obfuscate a python file"""
        self.key=key; self.share=share
        if not self.share or self.share==False:
            self.export=""
        else:
            self.export=True
        if "." in self.args:
            # obfuscate all python files in the current working directory
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.files_folders:
                if self.file_name.endswith(".py"):
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                       self.content=open_f.read()
                       self.leng=len(self.content)
                       open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.name="LOCKED_"+str(self.file_name.replace(".py", ""))+".py"
                    self.output = open(self.name, "w")
                    self.target=self.obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
                    if self.export==True:
                        self.ntangu=datetime.now()
                        self.mbote=self.ntangu.strftime("_%d_%m_%Y_(time_%H_%M_%S)")
                        self.t=str(self.file_name.replace(".py", ""))+str(self.mbote)
                        os.system("mkdir SHARE_"+self.t)
                        with open("SHARE_"+self.t+"\\"+str(self.file_name.replace(".py", ""))+"_signature.txt", "w") as f:
                            f.write(self.sig(self.name))
                            f.close()
                            os.system("copy "+str(self.name)+" SHARE_"+self.t)
        elif "*" in self.args:
            # obfuscate all python files in the current working directory and in its subfolders
            self.dir_walk(os.getcwd(), share=self.export)
            
        elif "***" in self.args:
            #obfuscate all python source code files stored in the entire disk
            if system(platform)=="win":
                self.place="C:\\"
            elif system(platform)=="lin" or system(platform)=="osx":
                self.place="/"
            else:
                raise Exception("Your system is uknown, we could not find the disk root directory.")
            self.dir_walk(self.place, share=self.export)
        else:
            # obfuscate the specific file whose name is given
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.args: 
                if self.file_name in self.files_folders:
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                                self.content=open_f.read()
                                self.leng=len(self.content)
                                open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.name="LOCKED_"+str(self.file_name.replace(".py", ""))+".py"
                    self.output =  open(self.name, "w")
                    self.target=self.obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
                    if self.export==True:
                        self.ntangu=datetime.now()
                        self.mbote=self.ntangu.strftime("_%d_%m_%Y_(time_%H_%M_%S)")
                        self.t=str(self.file_name.replace(".py", ""))+str(self.mbote)
                        os.system("mkdir SHARE_"+self.t)
                        with open("SHARE_"+self.t+"\\"+str(self.file_name.replace(".py", ""))+"_signature.txt", "w") as f:
                            f.write(self.sig(self.name))
                            f.close()
                            os.system("copy "+str(self.name)+" SHARE_"+self.t)

    def unlock(self, key):
        """ function that de_obfuscates or unhide smartly python source code"""
        self.key=key
        if "." in self.args:
            # de-obfuscate all python files in the current working directory
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.files_folders:
                if self.file_name.startswith("LOCKED_") and  self.file_name.endswith(".py"):
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                       self.content=open_f.read()
                       self.leng=len(self.content)
                       open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output = open("UNLOCKED_"+str(self.file_name[7:].replace(".py", ""))+".py", "w")
                    self.target=self.de_obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))         
        elif "*" in self.args:
            # de-obfuscate all python files in the current working directory and in its subfolders
            self.dir_walk_U(os.getcwd())
            
        elif "***" in self.args:
            #de-obfuscate all python source code files stored on the entire disk
            if system(platform)=="win":
                self.place="C:\\"
            elif system(platform)=="lin" or system(platform)=="osx":
                self.place="/"
            else:
                raise Exception("Your system is unknown, we could not find the disk root directory.")
            self.dir_walk_U(self.place)
        else:
            # de-obfuscate the specific file whose name is given
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.args:
                if self.file_name in self.files_folders:
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                                self.content=open_f.read()
                                self.leng=len(self.content)
                                open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output =  open("UNLOCKED_"+str(self.file_name[7:].replace(".py", ""))+".py", "w")
                    self.target=self.de_obfuscate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
        return "UNLOCKED_"+str(self.file_name[7:].replace(".py", ""))+".py"

