class propagator:
    def __init__(self, element):
        try:
            self.vfrom = element.find("from").text
            self.vto = element.find("to").text
            self.fromto = {self.vfrom, self.vto}
            self.field = element.find("field").text
            self.id = element.find("id").text
        except:
            print "Error while defining propagator object"
    def texprint(self,file,particledict,shape=""):
        if shape=="":
            file.write("{} -- [ {} ] {},\n ".format(self.vfrom, particledict[self.field] ,self.vto))
        else:
            file.write("{} -- [ {},{} ] {},\n".format(self.vfrom, particledict[self.field],shape ,self.vto))
