import math
import matplotlib.pyplot as plt
import numpy as np
import ast

log = []
with open("log.txt","r") as file:
        for line in file:
            if line[0] != "[":
                continue
            else:
                line = ast.literal_eval(line)
                for values in line:

                    log.append([float(values[0]),float(values[1])])
        

class robot:
    def __init__(self):
        self.pos_x = [0]
        self.pos_y = [0]
        self.angle = 160
        
        
    def move(self,distance,ang):
        self.angle += ang
        
        x, y = self.pos_x[-1], self.pos_y[-1]
        x += math.cos(math.radians(self.angle))*distance
        y += math.sin(math.radians(self.angle))*distance
        
        self.pos_x.append(x)
        self.pos_y.append(y)
        
    def draw(self, keep_axes=True):
        x = plt.plot(self.pos_x,self.pos_y)
        
        
robo = robot()
for values in log:
    angle = values[1]
    if abs(angle) <= 50:
        angle = angle * 0.9
    elif abs(angle) > 50:
        angle = angle * 1
    robo.move(abs(values[0])/25,angle)


x_cords = robo.pos_x
y_cords = robo.pos_y

min_x = int(abs(min(x_cords)))
max_x = int(abs(max(x_cords)))
min_y = int(abs(min(y_cords)))
max_y = int(abs(max(y_cords)))


width, height = min_y+max_y+1,min_x+max_x+1

grid = np.array([[255 for y in range(height)] for x in range(width)])
print(grid.shape)

for x,y in zip(x_cords,y_cords):
    x,y = int(x),int(y)
    #plt.scatter(x, y)
    
    grid[y+min_y][x+min_x] = 0
    
    
plt.imshow(grid,cmap='gray', vmin=0, vmax=255)
plt.show()
print(grid)
