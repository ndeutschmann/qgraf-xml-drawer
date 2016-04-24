import re
import sys

def pparse(p):
    lp=re.split("[+-]",p)
    for mom in [x for x in lp if x!='']:
        p=p.replace(mom,mom+",")
    lp=p.split(",")
    return [x for x in lp if x!='']


class Vertex:
    def __init__(self,element):
        try:
            self.momenta=element.find("momenta").text.split(",")
            self.type=element.find("type").text
            self.types=element.find("type").text.split(",")
            self.fields=element.find("fields").text.split(",")
            self.id=element.find("id").text
            for i in range(0,len(self.fields)):
                if int(self.fields[i])<0:
                    self.fields[i]="ext"+str(-int(self.fields[i]))
        except:
            print "Error while defining vertex object"

    def openline(self,file,line):
        "print opening the line"
        if re.search('[a-zA-Z]',self.fields[0]):
            if int(self.fields[0].split("t")[1])%2==0: # a general code should put ubar here
                file.write("*(-g_({},{})+m{})".format(line,self.momenta[0],self.types[0].split("bar")[0]))
            if int(self.fields[0].split("t")[1])%2 == 1: # a general code should put vbar here
                file.write("*(g_({},{})-m{})".format(line,self.momenta[0],self.types[0].split("bar")[0]))
        else:
            print "this vertex does no seem to contain a psibar !"

    def writenextprop(self,file,line=1):
        if not (self.types[1] in ["t","b"]):
            print "No fermion coming out of this vertex ! Something is wrong."
        elif re.search('[a-zA-Z]',self.fields[1]):
            print "This this the end of the line !"
            if int(self.fields[1].split("t")[1])%2==1:
                file.write("(g_({},{})+m{})".format(line,self.momenta[1],self.types[1]))
            if int(self.fields[1].split("t")[1])%2==0:
                file.write("(-g_({},{})-m{})".format(line,self.momenta[1],self.types[1]))
        else:
            file.write("i_*(")
            lp=pparse(self.momenta[1])
            for p in lp:
                file.write("g_({},{})+".format(line,p))
            file.write("m{})*Denom({},m{})*d_(col{},col{})".format(self.types[1],self.momenta[1],self.types[1],self.fields[1],int(self.fields[1])+1))

    def __contains__(self,f):
        f in self.fields

    def output(self,file,line=1):
        if self.type=="tbar,t,g":
            file.write("i_*g*g_({},mu{})*T(b{},col{},col{})".format(line,self.fields[2],self.fields[2],self.fields[0],self.fields[1]))
        elif self.type=="bbar,b,g":
            file.write("i_*g*g_({},mu{})*T(b{},col{},col{})".format(line,self.fields[2],self.fields[2],self.fields[0],self.fields[1]))
        elif self.type=="tbar,t,H":
            file.write("i_*Y*d_(col{},col{})".format(self.fields[0],self.fields[1]))
        elif self.type=="H,H,H":
            file.write("i_*h3")
        elif self.type=="H,H,H,H":
            file.write("i_*h4")
        elif self.type=="g,g,g":
            file.write("(-g3*f(b{},b{},b{})*(0".format(self.fields[0],self.fields[1],self.fields[2]))
            for i in range(0,3):
                j=(i+1)%3
                k=(i+2)%3
                p1=self.momenta[i]
                p2=self.momenta[j]
                lp1=pparse(p1)
                lp2=pparse(p2)
                #add the index k to each individual momentum and then p-k
                for mom in lp1:
                    if p1!="0":
                        p1=p1.replace(mom,mom+"(mu{})".format(self.fields[k]))
                for mom in lp2:
                    if p2!="0":
                        p2=p2.replace(mom,mom+"(mu{})".format(self.fields[k]))
                p="({}-({}))".format(p1,p2)
                file.write("+d_(mu{},mu{})*{}".format(self.fields[i],self.fields[j],p))
            file.write("))")
        elif self.type=="g,g,g,g":
            i=self.fields[0]
            j=self.fields[1]
            k=self.fields[2]
            l=self.fields[3]
            file.write("(-i_)*g^2*(")


            file.write("f(b{},b{},bdummy)*f(b{},b{},bdummy)*(d_(mu{},mu{})*d_(mu{},mu{})-d_(mu{},mu{})*d_(mu{},mu{}))".format(i,j,k,l,i,k,j,l,i,l,j,k))

            file.write(" +f(b{},b{},bdummy)*f(b{},b{},bdummy)*(d_(mu{},mu{})*d_(mu{},mu{})-d_(mu{},mu{})*d_(mu{},mu{}))".format(i,k,j,l,i,j,k,l,i,l,j,k))

            file.write(" +f(b{},b{},bdummy)*f(b{},b{},bdummy)*(d_(mu{},mu{})*d_(mu{},mu{})-d_(mu{},mu{})*d_(mu{},mu{}))".format(i,l,j,k,i,j,k,l,i,k,j,l))
            file.write(")")
        else:
            print "ERROR: Unknown vertex type"
            print self.type
