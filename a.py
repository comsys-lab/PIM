import numpy as np
bandwidth = 4

buffer1_flag = True
buffer2_flag = False

buffer1 = 50
buffer2 = 50

consume = 100

operation = 400

filling = round(buffer1/bandwidth,2)
print(filling)
temp = np.array([i for i in range(100)])
for i in range(4): temp[i] = -1
temp1 = set(temp)
temp1.discard(-1)
print(len(temp1))



input_temp = []
for i in range(3):
    x = np.random.rand(2,3)
    input_temp.append(x)

x = np.array(input_temp).reshape(2,9)
y = np.concatenate((input_temp[0],input_temp[1]),axis=1)
z = np.concatenate((y,input_temp[2]),axis=1)

print(input_temp[0])
print(x[:,:3])
print(z[:,:3])
