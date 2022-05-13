import os
# assign directory
directory = 'bot-data'
merged = open('merged_data.csv','a')
# iterate over files in
# that directory
files = []
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)
print(files)

if len(files)!=0:
    for file in files:
        f = open(str(file),'r')
        lines = f.readlines()
        count = 0
        for line in lines:
            if count ==0:
                count+=1
                continue
            else:
                merged.write(line)
        f.close()
        os.remove(file)


        

    
