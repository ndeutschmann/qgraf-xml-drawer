#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from vertex import *
from line import*

graphs=XML(default_loader("grafs",parse))
diagrams=graphs.find("diagrams")

pt = {"g": "gluon", "t": "fermion", "tbar": "fermion","H": "scalar"}

file = open("diagrams.tex","w+")

for diagram in diagrams.getchildren():
    DiagID = diagram.find("id").text
    file.write(DiagID+"~\\feynmandiagram[horizontal = Hext2 to mid,small]{\n")
    file.write("{} -- [ opacity = 0 ] {} ,\n".format("gext1","mid"))
    file.write("{} -- [ opacity = 0 ] {} ,\n".format("gext3","mid"))
    NOvertices=diagram.find("vertices").getchildren()
    propagators=diagram.find("propagators").getchildren()

    vertices=[]

    for v in NOvertices:
        vertices.append(Vertex(v))
    for v in vertices:
        f = v.fields
        id = "V"+("".join(f))
        print "vertex: "+id
        t = v.types
        for i in range(len(f)): #LOOP OVER PROPS IN V
            if re.search('[a-zA-Z]',f[i]):
                file.write("{} -- [ {} ] {}{} ,\n".format(id,pt[t[i]],t[i],f[i]))
            else:
                if not (int(f[i])%2): #IF OUTGOING #NEED TO DO SOMETHING ABOUT EXTERNALS
                    found = False
                    for w in vertices:#FIND CONNECTED VERTEX
                        if str(int(f[i])-1) in w:
                            found = True
                            wid = "V"+("".join(w.fields))
                            break
                    if not found:
                        print "Error"
                    else:
                        shape = ""
                        if str(int(f[i])-1) in v:
                            shape="half right"
                            if id!=wid:
                                print "PB"
                            wid+="tad"
                            file.write("{} -- [ {}, {} ] {} ,\n".format(wid,pt[t[i]],shape,id))
                        if shape=="":
                            for wf in w.fields:
                                if not re.search('[a-zA-Z]',wf):
                                    if str(int(wf)-1) in v:
                                        shape = "quarter right"
                                        break
                        file.write("{} -- [ {}, {} ] {} ,\n".format(id,pt[t[i]],shape,wid))
    file.write("};\n")
