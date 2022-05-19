f = open("report.csv","w")
readfrom = open("./trainer/report.txt","r")
f.write("Layers,Activation,Average Score,Average Accuracy\n")
lines = readfrom.readlines()
count = 0
data=[]
for line in lines:
    sentence = ""
    parsing = line.split()
    if len(parsing)!=0:
        if parsing[0]=="Layers:":
            for individual in range(1,len(parsing)):
                sentence+= parsing[individual]+"-"
            sentence = sentence[:-1]
            sentence+=","
        elif parsing[0]=="Activation:":
            for individual in range(1,len(parsing)):
                sentence+=parsing[individual].replace(',',"")[0:3]+"-"
            sentence = sentence[:-1]
            sentence+=","
        elif parsing [0]=="Average":
            sentence+=parsing[2]
            sentence+=","
            sentence+=parsing[6]
            sentence+="\n"
        data.append(sentence)

for info in data:
    f.write(info)