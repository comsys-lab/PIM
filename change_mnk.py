import os
#original path
path = ''
lists = os.listdir(path)
#storing path
path_1 = ''
for i in lists:
    old_path = path + i
    new_path = path_1 + i
    f = open(old_path,'r')
    lines = f.readlines()
    temp = []
    lines = lines[1:]
    for line in lines:
        line = line.strip()
        if line[-1:] ==",":
            temp.append(line[:-1])
        else:
            temp.append(line)
    f.close()
    f = open(new_path,'w')
    for i in temp:
        x = i.split(',')
        f.write(x[0]+','+x[1]+',1,1,1,'+x[3]+','+x[2]+',1'+'\n')
    f.close()