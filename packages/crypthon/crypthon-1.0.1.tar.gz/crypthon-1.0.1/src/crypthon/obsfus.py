#!/usr/bin/python
# -*- coding: utf-8 -*-
from dico import dico_ord, dico_chr
import os, re, hashlib
from sys import platform

system = lambda name: "lin" if name=="linux" or name=="linux2" else "osx" if name=="darwin" else "win" if name=="win32" else "uknown system"


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

class pyLoc:
    """ This class represents the pyLoc heart.
        It takes optionnal arguments:
        -either a list of file names in the current working directory. E.g: pyLoc("file1.py") or pyLoc("file1.py", "file2.py")
        -either "/" to obsfucate all python files in the current working directory. E.g: pyLoc("/").loc(key)
        -either "*" to obsfucate all python files in the current working directory and in its subfolders. E.g: pyLoc("*").loc(key)
        -either "***" to obsfucate all python source code files stored in the entire disk. E.g: pyLoc("***").loc(key)
        key --> the key is a string: a phrase or key string or a list of words or strings. E.g: key="hello"; key="hello, h*cb45#".
        genKey(key, leng) --> generates a one time pad of length "leng" key from a the key "key".
                This key is generated randomly using the secure hash algorithm with 512 bits. To do so, 
                it uses the composition function of functions initialized at sha512(key) concatenated with 
                the footprints of consecutive concatenation of footprints up to the length "leng".
        loc(key) --> locks / obfuscates python files indicated in pyLoc with the one time pad key generated from
                the key "Key"
        unlock(key) --> unlocks / de-obsfucates python files indicated in pyLoc with the one time pad key generated
                from the key "Key".
        
        E.g: 1- OBSFUCATE A PYTHON FILE or PYTHON FILES IN THE CURRENT WORKING DIRECTORY
                to OBSFUCATE the file "file1.py" located in the current working directory with the one time pad generated from key "hello",
                --> pyLoc("file1.py").loc("hello") which generates the file "LOCKED_file1.py" in the same directory. This file is obsfucated.
                to DE-OBSFUCATE the file "LOCKED_file1.py" located in the current working directory with the one time pad generated from key "hello",
                --> pyLoc("LOCKED_file1.py").unlock("hello") which generates back the file "UNLOCKED_file1.py" which is equal to "file1.py" in the same 
                    directory.
             2- OBSFUCATE ALL PYTHON FILES LOCATED IN THE CURRENT WORKING DIRECTORY
                to OBSFUCATE all python files located in the current working directory with the one time pad generated from the key "hello",
                --> pyLoc("/").loc("hello") which generates the files "LOCKED_....py" in the same directory. These files are obsfucated.
                to DE-OBSFUCATE all the obsfucated python files "LOCKED_....py" located in the current working directory with the one time pad generated from
                the key "hello", 
                --> pyLoc("/").unlock("hello") which generates back the files "UNLOCKED_....py" in the same directory.
             3- OBSFUCATE ALL PYTHON FILES LOCATED IN THE CURRENT WORKING DIRECTORY AND ITS SUB-DIRECTORIES
                to OBSFUCATE all python files located in the current working directory and its sub-directories with the one time pad generated from the key "hello",
                --> pyLoc("*").loc("hello") which generates the files "LOCKED_....py" in current working directory and all its corresponding sub-directories.
                to DE-OBSFUCATE all python files located in the current working directory and its sub-directories, 
                --> pyLoc("*").unlock("hello") which generates the files "UNLOCKED....py" in the current working directory and all its corresponding sub-directories.
             4- OBSFUCATE ALL PYTHON FILES LOCATED IN THE ENTIRE DRIVE PARTITION
                to OBSFUCATE all python files located in the entire drive partition with the one time pad generated from the key "hello",
                --> pyLoc("***").loc("hello") which generates the files "LOCKED_....py" in wherever directory or sub-directory where python files are found.
                to DE-OBSFUCATE all python files located in the entire drive partition with the one time pad generated from the key "hello",
                --> pyLoc("***").unlock("hello) which generates the files "UNLOCKED....py" in wherever directory or sub-directory where locked python files are found.

            NOTE: when calling pyLoc withe parameter without parameter delete or with parameter delete=False, (E.g pyLoc("file1.py").loc(key) or
              pyLoc("file1.py", delete=False).loc(key)), the original files are not deleted. and with parameter delete=True, original files are deleted
    """
    def __init__(self, *args:str, delete=False):
        self.args=args; self.delete=delete
        if not self.args:
            print("Please specify file names or the keywords. Please read the documentation")
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
                self.bravo+=hash_pass(self.bravo) #str(self.genKey(self.bravo, self.leng))
            return self.bravo[:self.leng]
              
    def obsfucate(self, content, key)->str:
        """obsfucation function"""
        self.key=key; self.content=content; self._=""
        for i in range(len(self.key)):
            self.p_k=dico_ord[self.key[i]]
            try:
                self.p_p=dico_ord[self.content[i]]
            except:
                raise Exception("The character "+str(self.content[i])+" DOES NOT EXIST in the dictionary dico_ord \n Please add it and/or report it")
            self._+=dico_chr[(self.p_p+self.p_k)%93]
        return self._

    def de_obsfucate(self, content, key):
        """de-obsfucation funtion"""
        self.content=content; self.key=key; self._=""
        for i in range(len(self.key)):
            self.p_k=dico_ord[key[i]]
            try:
                self.p_c=dico_ord[self.content[i]]
            except:
                raise("The character "+str(self.content[i])+" DOES NOT EXIST in the dictionnaries\n Please add it and/or report it")
            self._+=dico_chr[(self.p_c-self.p_k)%93]
        return self._
    
    def dir_walk(self, dir):
        """ function that walks through directories for python files while locking files"""
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
                    self.output = open("LOCKED_"+str(self.element.replace(".py", ""))+".py", "w")
                    self.target=self.obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.element))
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
                    self.target=self.de_obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.element))
        return "UNLOCKED_"+str(self.element[7:].replace(".py", ""))+".py"

    def loc(self, key):
        """ function that locks / obsfucate a python file"""
        self.key=key
        if "/" in self.args:
            # obsfucate all python files in the current working directory
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.files_folders:
                if self.file_name.endswith(".py"):
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                       self.content=open_f.read()
                       self.leng=len(self.content)
                       open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output = open("LOCKED_"+str(self.file_name.replace(".py", ""))+".py", "w")
                    self.target=self.obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
        elif "*" in self.args:
            # obsfucate all python files in the current working directory and in its subfolders
            self.dir_walk(os.getcwd())
            
        elif "***" in self.args:
            #obsfucate all python source code files stored in the entire disk
            if system(platform)=="win":
                self.place="C:\\"
            elif system(platform)=="lin" or system(platform)=="osx":
                self.place="/"
            else:
                raise Exception("Your system is uknown, we could not find the disk root directory.")
            self.dir_walk(self.place)
        else:
            # obsfucate the specific file whose name is given
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.args: 
                if self.file_name in self.files_folders:
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                                self.content=open_f.read()
                                self.leng=len(self.content)
                                open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output =  open("LOCKED_"+str(self.file_name.replace(".py", ""))+".py", "w")
                    self.target=self.obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
        return  "LOCKED_"+str(self.file_name.replace(".py", ""))+".py"

    def unlock(self, key):
        """ function that de_obsfucates or unhide smartly python source code"""
        self.key=key
        if "/" in self.args:
            # obsfucate all python files in the current working directory
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
                    self.target=self.de_obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))         
        elif "*" in self.args:
            # obsfucate all python files in the current working directory and in its subfolders
            self.dir_walk_U(os.getcwd())
            
        elif "***" in self.args:
            #obsfucate all python source code files stored in the entire disk
            if system(platform)=="win":
                self.place="C:\\"
            elif system(platform)=="lin" or system(platform)=="osx":
                self.place="/"
            else:
                raise Exception("Your system is uknown, we could not find the disk root directory.")
            #@self.dir_walk
            #def dir(self): return self.place
            self.dir_walk_U(self.place)
        else:
            # obsfucate the specific file whose name is given
            self.place=os.getcwd()
            self.files_folders=os.listdir(self.place)
            for self.file_name in self.args: 
                print(self.file_name)
                if self.file_name in self.files_folders:
                    with open(str(self.file_name), mode="r", encoding="utf-8") as open_f:
                                self.content=open_f.read()
                                self.leng=len(self.content)
                                open_f.close()
                    self.KEY=self.genKey(self.key, self.leng)
                    self.output =  open("UNLOCKED_"+str(self.file_name[7:].replace(".py", ""))+".py", "w")
                    self.target=self.de_obsfucate(self.content, self.KEY)
                    self.output.write(self.target)
                    self.output.close()
                    if self.delete==True:
                        os.system(self.cmd+str(self.file_name))
                    return "UNLOCKED_"+str(self.file_name[7:].replace(".py", ""))+".py"

#Begin Example
#key="Bonjour"
#p=Sabotage("LOCKED_sabo.py.py")
#print(p.smart_obsfucate(key))
#print(p.smart_de_obsfucate(key))
#p=Sabotage("sab.py")
#print(p.smart_obsfucate(key))
#print(p.loc(key))
#p=pyLoc("/", delete=False)
p=pyLoc("obsfus1.py", delete=False)
print(p.unlock("Bonjour"))
#print(p.loc(key))
# End Example
#pyLoc("/", delete=False).loc(key)