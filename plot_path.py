import math
import matplotlib.pyplot as plt
import numpy as np

log = [[30, -2.0], [30, -2.0], [29, 7.0], [31, 13.5], [29, 13.5], [31, 3.0], [29, 10.0], [30, 8.5], [30, 8.5], [30, 10.5], [31, 10.5], [30, 19.5], [29, 19.5], [31, 13.0], [29, 13.5], [31, 13.5], [29, 20.0], [30, 9.0], [30, 8.5], [30, 1.0], [30, 1.0], [30, 1.0], [1, -90], [29, 5.5], [31, -7.0], [30, -7.5], [30, 15.5], [29, 15.5], [30, 15.5], [29, 21.0], [32, 21.0], [29, 22.5], [30, 15.5], [31, 15.5], [29, 15.5], [31, 9.5], [30, 9.0], [29, 3.0], [31, 3.0], [0, -90], [29, -90]]
class robot:
    def __init__(self):
        self.pos_x = [0]
        self.pos_y = [0]
        self.angle = 290
        
        
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
    robo.move(abs(values[0])/25,values[1])


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
print(grid)
