variable = "Aardvark"

print "Start: ",variable
def Zebra():
    global variable
    print "Zebra: ", variable
    variable = "Zebra"
    print "Zebra: ", variable
    
def Elephant():
    global variable
    print "Elephant: ",variable
    variable = "Elephant"
    print "Elephant: ",variable

Zebra()
Elephant()

print "End: ",variable