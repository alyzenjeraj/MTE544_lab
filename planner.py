import math
# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        return x, y

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        pass
        
        traj = "sigmoid"     # parabola or sigmoid
        dx   = 0.05           

        waypoints = []

        if traj == "parabola":
            # y = x^2,  x for [0, 1.5]
            x = 0.0
            while x <= 1.5 + 1e-9:
                y = x*x
                waypoints.append([float(x), float(y)])
                x += dx

        elif traj == "sigmoid":
            # sigmoid = 2/(1+e^(-2x)) - 1,  x for [0, 2.5]
            x = 0.0
            while x <= 2.5 + 1e-9:
                y = 2.0/(1.0 + math.exp(-2.0*x)) - 1.0
                waypoints.append([float(x), float(y)])
                x += dx

        return waypoints

