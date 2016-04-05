import os
import threading

import sys

from gerbenBetterRefinement import getIsomorphismGroups
from graphIO import loadgraph
from graphUtil import isConnected, isTree

"""
    This file is the "executable" file.
    As such, it contains imports of important modules to ease in the usage of the application.
"""

class Job:
    def __init__(self, filename, aut=False):
        self.filename = filename
        self.aut = aut
        if filename[-2:] == "gr":
            self.single = True
        else:
            self.single = False
        self.g = loadgraph(filename, readlist=not self.single)
        if not self.single:
            self.g = self.g[0]
        print("Launching job [%s]..."%filename)
        threading._start_new_thread(self.run, tuple())

    def run(self):
        if self.single:
            getIsomorphismGroups([self.g], self.aut)
        else:
            getIsomorphismGroups(self.g, self.aut)
        print("\n")
        sys.stdout.write(">")
        sys.stdout.flush()


class App:
    def __init__(self):
        self.files = [f for f in os.listdir() if f[-2:] == "gr" or f[-3:] == "grl"]
        print("Welcome to the graph isomorphism and automorphism application...")
        if len(self.files) > 0:
            self.listFiles()
            print("Please use a command or type help for all the available commands.")


    def listFiles(self):
        print("\nI will now list all the available graph files:")
        for i in range(len(self.files)):
            print("id: %i, filename: %s" % (i, self.files[i]))
        print()

    def loop(self):
        running = True
        while running:
            command = input("> ")
            c = command.split(" ")
            n = c[0]
            if n == "aut":
                if len(c) != 2:
                    print("Error! Please use 'aut <file-id>'")
                else:
                    job = Job(self.files[int(c[1])], True)
            elif n == "iso":
                if len(c) != 2:
                    print("Error! Please use 'iso <file-id>'")
                else:
                    job = Job(self.files[int(c[1])], False)
            elif n == "help":
                print("All commands are:")
                print("aut <file-id> \t Calculate number of automorphisms and isomorphism groups")
                print("iso <file-id> \t Find isomorphism groups")
                print("help \t show this help message")
                print("exit \t exits the program")
                print("list \t lists files and their file-id numbers")
                print("info <file-id> \t show some basic information about the graphs")
            elif n == "exit":
                print("Stopping program...")
                running = False
            elif n == "list":
                self.listFiles()
            elif n == "info":
                if len(c) != 2:
                    print("Error! Please use 'info <file-id>'")
                else:
                    self.graphInfo(self.files[int(c[1])])
            else:
                print("I don't know that command, please retype the command or type help")

    def graphInfo(self, filename):
        if filename[-2:] == "gr":
            gl = [loadgraph(filename, readlist=False)]
        else:
            gl = loadgraph(filename, readlist=True)[0]
        print("This file contains %i graph%s"%(len(gl), "s" if len(gl) > 1 else ""))
        i = 0
        for g in gl:
            print("Graph %i:"%i)
            print("\tIs %sconnected, is %sa tree, has %i vertice%s and %i edge%s"
                  %("" if isConnected(g) else "not ",
                    "" if isTree(g) else "not ",
                    len(g.V()), "s" if len(g.V()) > 1 else "",
                    len(g.E()), "s" if len(g.E()) > 1 else ""))

            i+=1


if __name__ == "__main__":
    app = App()
    app.loop()