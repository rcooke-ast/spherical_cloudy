import misc

def abundances(elem, scale):
    # If scale is a log10 value, convert to linear
    if scale < 0.0: scale = 10.0**scale
    # Set the number abundance of each element
    if elem == "H": abund = 1.0
    elif elem == "D": abund = 10.0**(-4.60)
    elif elem == "He": abund = 1.0/12.0
    elif elem == "Li": abund = 10.0**(2.70-12.0)
    elif elem == "C": abund = scale * 10.0**(8.43-12.0)
    elif elem == "N": abund = scale * 10.0**(7.83-12.0)
    elif elem == "O": abund = scale * 10.0**(8.69-12.0)
    elif elem == "Mg": abund = scale * 10.0**(7.56-12.0)
    elif elem == "Al": abund = scale * 10.0**(6.44-12.0)
    elif elem == "Si": abund = scale * 10.0**(7.51-12.0)
    elif elem == "Ar": abund = scale * 10.0**(6.40-12.0)
    elif elem == "Fe": abund = scale * 10.0**(7.47-12.0)
    else:
        print "ERROR :: Abundance is not defined for element {0:s}. Setting to 1E-10".format(elem)
        abund = 1.0E-10
    return abund

def ionization_potential(ion):
    """
    Ionization energies of each element/ion from:
    http://physics.nist.gov/PhysRefData/ASD/ionEnergy.html
    """
    data = open("data/atomic_ip.dat",'r').readlines()
    ip = None
    for i in range(len(data)):
        if data[i][0] == "#": continue
        datspl = data[i].split("|")
        if datspl[1].strip() == ion:
            iptxt = datspl[8].strip()
            # ignore the outer brackets if they exist
            if iptxt[0] == "(":
                iptxt = iptxt[1:-1]
            elif iptxt[0] == "[":
                iptxt = iptxt[1:-1]
            # Now just take the value (and remove the error)
            ip = float(iptxt.split("(")[0])
# 	if ion == "H I": ip = 13.598434005136
# 	elif ion == "D I": ip = 13.602134041842
# 	elif ion == "He I": ip = 24.587387936
# 	elif ion == "He II": ip = 54.41776311
# 	elif ion == "Li I": ip = 5.391714761
# 	elif ion == "Li II": ip = 75.6400937
# 	elif ion == "Li III": ip = 122.4543538
# 	elif ion == "N I": ip = 14.53413
# 	elif ion == "N II": ip = 29.60125
# 	elif ion == "N III": ip = 47.4453
# 	elif ion == "Si I": ip = 8.151683
# 	elif ion == "Si II": ip = 16.34585
# 	elif ion == "Si III": ip = 33.49300
# 	else:
# 		print "Ionization potential not included in calculation for ion {0:s}".format(ion)
# 		assert(False)
    if ip is None:
        print "Ionization potential not included in calculation for ion {0:s}".format(ion)
        assert(False)
#	else:
#		print ion, ip
    return ip

def getids(useelems, scale=1.0):
    iddict = dict({})
    elems = ["H", "D", "He", "Li", "C", "N", "O", "Mg", "Al", "Si", "Ar", "Fe"]
    ionlv = [1,1,2,3,6,7,8,12,13,14,18,26]
    # Add some "required" elements, but set their abundance to zero
    zeroabund = []
#	if "D I" not in useelems:
#		zeroabund += ["D I"]
#		useelems  += ["D I"]
    # Now fill in the dictionary
    for e in range(len(elems)):
        abund = abundances(elems[e],scale)
        for i in range(ionlv[e]):
            strval = elems[e] + " " + misc.numtorn(i+1)
            ip = ionization_potential(strval)
            if strval in useelems:
                for k in range(len(useelems)):
                    if useelems[k] == strval:
                        iddict[strval] = [k,abund,ip]
                        break
    for i in range(len(zeroabund)):
        e = zeroabund[i]
        iddict[e] = [iddict[e][0],0.0,iddict[e][2]]
    return iddict, zeroabund