
# coding: utf-8

# In[1]:


import math
def best_hotel_location(grid, sight_r):
    min_x, max_x = float('inf'), -float('inf')
    min_y, max_y = min_x, max_x
    total_happiness = 0. #happiness from each event = W/D,W is the value and D is the distance
    total_event_visited = 0
    res_x, res_y = 0, 0
    for point in grid:
        min_x = min(min_x, point[0])
        min_y = min(min_y, point[1])
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            cur_happiness = 0.
            cur_event_visited = 0
            for point in grid:
                distance = 1 + math.sqrt(pow(point[0]-x, 2) + pow(point[1]-y))
                if distance <= sight_r:
                    cur_happiness += point[2] / distance
                    cur_event_visited += 1
            if cur_happiness > total_happiness:
                total_happiness = cur_happiness
                total_event_visited = cur_event_visited
                res_x, res_y = x, y
            elif cur_happiness == total_happiness:
                if cur_event_visited > total_event_visited:
                    total_event_visited = cur_event_visited
                    res_x, res_y = x, y
                elif cur_event_visited == total_event_visited:
                    if math.sqrt(x**2 + y**2) < math.sqrt(res_x**2 + res_y**2):
                        res_x, res_y = x, y
    return [res_x, res_y]

