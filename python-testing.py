import random
MaxNumberLimit = 256

def splitToPackages(package):
    if (len(package) <= MaxNumberLimit - 7):
        return [str(random.randint(1,9999999)) + str(package)]
    else:
        packages = []
        for i in range(0,len(package),MaxNumberLimit - 7):
            packages.append(str(random.randint(1,9999999))+str(package)[i:i+MaxNumberLimit-7])
        return packages

print(splitToPackages(("banana")*50))