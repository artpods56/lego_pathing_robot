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
        


#log = [[30, -2.0], [30, -2.0], [30, -2.0], [29, -2.0], [31, 5.0], [30, -1.0], [29, -4.5], [31, -4.5], [29, -4.5], [31, 1.5], [31, 1.5], [-1, -90], [31, 2.0], [28, -15.5], [31, -17.0], [30, -18.0], [30, -11.0], [29, -1.5], [31, -2.5], [30, -2.5], [30, -7.0], [30, 1.0], [29, 1.0], [31, 11.5], [30, 20.5], [30, 18.0], [30, 9.0], [30, 9.0], [29, 20.5], [31, 10.0], [29, 14.5], [30, 14.0], [30, 17.5], [30, 8.5], [31, 8.5], [29, 14.5], [30, 14.0], [31, -0.5], [30, 4.5], [29, 4.5], [30, 11.5]]
#log = log = [[21, -0.6], [20, 0.0], [20, 0.0], [20, 0.0], [19, -5.4], [20, 0.0], [21, 0.0], [20, 0.0], [20, 0.0], [19, 0.0], [20, -9.0], [21, -5.4], [19, -28.2], [20, -27.0], [20, -14.4], [21, -6.6], [20, -6.6], [19, 3.0], [21, -1.8], [19, -11.4], [21, 4.2], [19, 4.2], [21, -0.6], [19, -10.8], [19, 1.2], [21, 1.2], [19, 1.2], [22, 0.6], [19, -43.5], [21, -14.4], [20, -9.6], [19, -12.6], [21, -4.2], [19, -4.2], [21, 3.6], [20, -9.6], [19, -1.8], [20, -1.8], [20, -1.8], [20, -7.2], [20, -27.6], [20, -27.6], [20, -13.8], [20, -9.6], [20, -3.6], [20, -9.0], [20, -1.8], [20, -1.8], [21, -1.8], [20, -7.2], [20, -1.2], [19, -0.6], [20, -0.6], [21, -0.6], [20, 0.6], [19, 0.6], [20, 0.6], [20, 0.6], [20, -2.4], [20, -6.6], [19, 3.6], [21, 3.6], [20, -0.6], [20, -0.6], [20, -0.6], [20, -0.6], [21, -0.6], [20, -9.0], [19, 5.4], [20, -90], [21, 90]]
def grow(grid,point):
    y, x = point
    g_width = grid.shape[0]
    g_height = grid.shape[1]
    print(point)
    # for n in range(x-1,x+2):
    #     for m in range(y-1,y+2):
    #         if n == g_height:
    #             continue
    #         if m == g_width:
    #             continue
    #         grid[m][n] = 255
    grid[y][x] = 255        
    return grid
    


class robot:
    def __init__(self):
        self.pos_x = [0]
        self.pos_y = [0]
        self.angle = 0
        
        
    def move(self,distance,ang):
        self.angle += ang
        
        x, y = self.pos_x[-1], self.pos_y[-1]
        x += math.cos(math.radians(self.angle))*distance
        y += math.sin(math.radians(self.angle))*distance
        
        self.pos_x.append(x)
        self.pos_y.append(y)
        
    def draw(self, keep_axes=True):
        x = plt.plot(self.pos_x,self.pos_y)
        
        


log = np.array(log)

grid_shape = (1000,1000)

print(log)
while any(measure > 28 for measure in grid_shape):
    robo = robot()
    i = 1.1
    log[:,0] /= i
    for values in log:
        angle = values[1]
        if abs(angle) <= 50:
            angle = angle * 0.9
        elif abs(angle) > 50:
            angle = angle * 1
        robo.move(abs(values[0]),angle)
    
    x_cords = robo.pos_x
    y_cords = robo.pos_y
    
    min_x = int(abs(min(x_cords)))
    max_x = int(abs(max(x_cords)))
    min_y = int(abs(min(y_cords)))
    max_y = int(abs(max(y_cords)))
    
    
    width, height = min_y+max_y+1,min_x+max_x+1
    grid = np.array([[0 for y in range(height*2)] for x in range(width*2)])
    
    grid_shape = grid.shape
    #print(grid.shape)
    i += 0.1



mid_x = grid_shape[0]/2
mid_y = grid_shape[1]/2




def fill(grid):
    tab = []
    for row in grid:
        temp = []
        for _ in row:
            temp.append(_)
        while len(temp) != 28:
            temp.append(0)
        tab.append(temp)
    return tab

grid = np.array(fill(grid))

grid = np.array(fill(grid.T))



print(grid.shape)
for x,y in zip(x_cords,y_cords):
    x,y = int(x),int(y)

    #plt.scatter(x, y)
    grid = grow(grid,(y+min_y+grid.shape[1]//3,x+min_x+grid.shape[1]//3))






print(grid.shape)
grid = np.flip(grid,0)
plt.imshow(grid,cmap='gray', vmin=0, vmax=255)
plt.imsave("chudadwujazero.png",grid,cmap="gray")
plt.show()

