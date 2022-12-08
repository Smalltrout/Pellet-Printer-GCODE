import re
import math

#explanation of the pattern:
#^ is beginning of the line
#* any number of the previous - in this case some people use G. instead of G[space]. 
#this basically says it will pickup on a space or a period
g0pattern = r"^G0.*"
g1pattern = r"^G1.*"

stopPattern = r"^;TIME_ELAPSED:814.387643"
startPattern = r"^;LAYER:0";
stopRE = re.compile(stopPattern)
startRE = re.compile(startPattern)

#this is converting the pattern given above into an object, which can be used for matching and searching
g0re = re.compile(g0pattern)
g1re = re.compile(g1pattern)


m82pattern = r"^M82"
m82RE = re.compile(m82pattern)

#same thing going on here as above. Essentially this pulls the X Y and Z coordinates
#the * is applied here as well similar to above
#breaking down the brackets:
    #\d finds any individual digit
    #here \. is being used to look for the non metacharacter . 
Xpattern = r".*X[-\.\d]+"
Ypattern = r".*Y[-\.\d]+"
Zpattern = r".*Z[-\.\d]+"
Epattern = r".*E[-\.\d]+"
Xre = re.compile(Xpattern)
Yre = re.compile(Ypattern)
Zre = re.compile(Zpattern)
Ere = re.compile(Epattern)

#variables which will be tracked and overwritten as necessary for pasting to CSV
prevX = 0
prevY = 0
prevZ = 0

curX = 0
curY = 0
curZ = 0


def extrudeLength():
    result = math.sqrt(math.pow((float(curX)-float(prevX)),2)+math.pow((float(curY)-float(prevY)),2))

    return round(result, 5)*-1
    
fout = open("result.gcode", "w")

#opening the gcode file; assigning the variable f to it
with open("forcsv.gcode", "r+") as f:

    #copies lines until it reaches the core g-code
    for line in f:
        
        #if there is an m82 it is changed to m83
        if(m82RE.match(line)):
        
            toRep = re.findall(m82pattern,line)[0].split('M')[1]
            fout.writelines(line.replace(toRep, "83"))
        
        else:
        
            fout.writelines(line)
        
        #break statement 
        if startRE.match(line):
            break
    
    #copies over core g-code, tracks x and y values, modifies E values as necessary 
    for line in f: 

        #checks stop case so we only modify the E values located in the core region of code
        if stopRE.match(line):
            break
                
        #if there is an x or y value it will be updated.
            #if there is also an E value it will be updated to be the result of extrudeLength
            #if there is no E value the line is just copied over
        if bool(Xre.match(line)) | bool(Yre.match(line)):
            prevX = curX
            curX = re.findall(Xpattern,line)[0].split('X')[1]
         
            prevY = curY
            curY = re.findall(Ypattern,line)[0].split('Y')[1]
        
            if Ere.match(line):
                toRep = re.findall(Epattern,line)[0].split('E')[1]
                repWith = extrudeLength()
                fout.writelines(line.replace(toRep, str(repWith)))
            else:
                fout.writelines(line)
                
        #if there is no X or Y value check if there is an E value
            #E values appear without an X or Y to usually retract the filament, we need to elminate this, so it sets that E value to 0
            #If there is no E value we just copy the line
        else:
        
            if Ere.match(line):
            
                toRep = re.findall(Epattern,line)[0].split('E')[1]
                fout.writelines(line.replace(toRep, str("0")))
         
            else:
                fout.writelines(line)
            
    
    #copies over remaining lines, sets any remaining extrusion values to 0. 
    for line in f:
    
        if Ere.match(line):
        
            toRep = re.findall(Epattern,line)[0].split('E')[1]
            fout.writelines(line.replace(toRep, str("0")))
            
        else:

            fout.writelines(line)
            
    print(
    
    '\n' + "--------------------------" + 
    '\n' + "Pellet conversion complete" +
    '\n' + "--------------------------" + '\n'
    
        )        
            
    
fout.close()            
         
                   

