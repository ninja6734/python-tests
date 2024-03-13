import random
from scratchattach import Encoding
MaxNumberLimit = 256

def splitToPackages(package):
    if (len(package) <= MaxNumberLimit - 7):
        return [str(random.randint(1,9999999)).zfill(7) + str(package)]
    else:
        packages = []
        for i in range(0,len(package),MaxNumberLimit - 7):
            packages.append(str(random.randint(1,9999999)).zfill(7)+str(package)[i:i+MaxNumberLimit-7])
        return packages

test = "bananas are really amazing and wonderful and observationary and I like them really much and I'm running out of ideas what to write here"
print(splitToPackages(Encoding.encode(test)))