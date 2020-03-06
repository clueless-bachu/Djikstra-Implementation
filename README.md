# Implementation of Dijkstra algorithm for a Point and Rigid Robot

### Overview
This project implements Dijkstra algorithm on both point and rigid robot to find optimal path from start point and goal point in obstacle space.

### Prerequisites
Python and python libraries like Numpy, Opencv, Heapq and Time are required to run the code.  

### Run
  - To run the code in terminal:
  ```
  python dijkstra.py
  ```
  - The program will ask for the radius of the robot to genrate the map. For point robot, radius is to be given as '0', while any other integer for rigid robots. It is assumed that the rigid robots are circular in shape.
  - Next, the clearance of the robot is asked. For point robot, clearance is to be given as '0', while any other integer for rigid robots.
  - Then, start point and goal point is asked from the user.
  - Dijkstra algorithm is then used to find the optimal path between the start and goal point.
  - The animation finally shows the optimal path found between the start and goal point.
  - In cases where no optimal path is found, "Path not found" is printed.

------------------------------------------------------------------------------------------------------------------
## Authors
- Vasista Ayyagari 
- Sayani Roy
