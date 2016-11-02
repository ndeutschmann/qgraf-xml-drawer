from xml.etree.ElementTree import *
from xml.etree.ElementInclude import *
import re
import sys
from propagator import *
from vertex import *
from copy import copy

graphs=XML(default_loader("grafs",parse))
diagrams=graphs.find("diagrams")

pt = {"g": "gluon", "t": "fermion", "tbar": "fermion","h": "scalar"}

file = open("diagrams.tex","w+")

for diagram in diagrams.getchildren():
    DiagID = diagram.find("id").text
    print "Doing diagram: "+DiagID
    file.write(DiagID+"~\\feynmandiagram[small]{\n")
    NOpropagators=diagram.find("propagators").getchildren()
    NOvertices=diagram.find("vertices").getchildren()
    propagators=[]
    for p in NOpropagators:
        propagators.append(propagator(p))
    vertices=[]
    for v in NOvertices:
        vertices.append(Vertex(v))
    bundles = []
    for p in propagators:
        if len(bundles) > 0:
            found = False
            for b in bundles:
                if p.fromto == b[0].fromto:
                    print "adding my propagator to an existing bundle"
                    b.append(p)
                    found = True
                    break
            if not found:
                bundles.append([p])
        else:
            bundles = [[p]]
    for b in bundles:
        if len(b)==1:
            if b[0].vfrom != b[0].vto:
                b[0].texprint(file,pt)
            else: #TADPOLE
                tadfrom = copy(b[0])
                tadto = copy(b[0])
                tadfrom.vto = "tad"+tadfrom.id
                tadto.vfrom = "tad"+tadfrom.id
                shape = "half right"
                tadfrom.texprint(file,pt,shape)
                tadto.texprint(file,pt,shape)
        if len(b)==2:
            shapedict = ["quarter right", "quarter left"]

            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
        if len(b)==3:
            shapedict = ["quarter right", "quarter left"]
            b[0].texprint(file,pt,shapedict[0])
            if b[1].vfrom == b[0].vfrom:
                b[1].texprint(file,pt,shapedict[1])
            else:
                b[1].texprint(file,pt,shapedict[0])
            b[2].texprint(file,pt)
        if len(b)>4:
            print "I don't know how to deal with this !"

    for v in vertices:
        for i in range(len(v.fields)):
            if re.search('[a-zA-Z]',v.fields[i]):
                file.write("{} [particle={}] -- [{}] {},\n".format(v.fields[i],v.fields[i],pt[v.types[i]],v.id))
#
#    file.write("ext1 -- [opacity = 0] mid,\n") add a comma above !
#    file.write("ext3 -- [opacity = 0] mid\n")
    file.write("q -- [opacity = 0] q\n")
    file.write("};\n")
