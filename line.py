import re
from vertex import *

class Line:
    def __init__(self):
        self.vertices = []
        self.open = False
    def __getitem__(self,index):
        return self.vertices[index]
    def __setitem__(self,index,value):
        self.vertices[index]=value
    def additem(self,v):
        if re.search('[a-zA-Z]',v.fields[0]):
            self.vertices.insert(0,v)
            self.open = True
        elif re.search('[a-zA-Z]',v.fields[1]):
            self.vertices.append(v)
            self.open = True
        else:
            (next,prev)=(str(int(v.fields[1])+1),str(int(v.fields[0])-1))
            i = 0
            found = False
            for w in self.vertices:
                if next == w.fields[0]:
                    self.vertices.insert(i,v)
                    found = True
                    break
                if prev == w.fields[1]:
                    self.vertices.insert(i+1,v)
                    found = True
                    break
                i=i+1
            if not found:
                self.vertices.append(v)


    def __iter__(self):
        return iter(self.vertices)
    def __len__(self):
        len(self.vertices)
    def __contains__(self,v):
        print ""
        print "trying to see if"
        print v.fields
        print "is connected to"
        for w in self.vertices:
            print w.fields
        contained = False
        for w in self.vertices:
            try:
                if int(v.fields[0])-1 == int(w.fields[1]):
                    contained = True
                    break
            except ValueError:
                pass
            try:
                if int(v.fields[1])+1 == int(w.fields[0]):
                    contained = True
                    break
            except ValueError:
                pass

        return contained

        #v in self.vertices
    def __add__(self,line2):
        nline = Line()
        for v in self:
            nline.additem(v)
        for v in line2:
            nline.additem(v)
        return nline
