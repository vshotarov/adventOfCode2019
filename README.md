## All my solutions for [Advent of Code 2019](https://adventofcode.com/2019) in Python 2
Although I have used python 3 for some of them, I've not used any backwards incompatible features, so if anyone ever wants to run these solutions, make sure you are using python 2.

After all, AoC 2019 took place literally in the last month before Python 2 reached it's end of life.

### Reflections
#### Ones I struggled with
I am happy I was able to solve almost all of the tasks without having to look for help. The two that I had to look up are:

- [Day 16: Flawed Frequency Transmission](https://adventofcode.com/2019/day/16) - Although I had some inclination that at the middle point it's all ones and then zeroes start creeping in from the left, I wasn't able to fully wrap my head around it at the time. It all made sense when I saw some on the subreddit describing it with a diagonal matrix.

- [Day 22: Slam Shuffle](https://adventofcode.com/2019/day/22) - I solved part 1 with a very naive list implementation and, even though, I could see what needs to be done I wasn't aware of the *Modular inverse* operation, so I had to look up how to solve the *deal with increment* function.

#### Breadth-first search
Since there were a lot of path finding tasks I got to use it quite a bit which I enjoyed.

I had heard the term before, but I hadn't really put much thought in it. Once I solved the first path finding task (the oxygen one) and looked up people's solutions I realized what I was doing is actually BFS.

The one thing I was missing initially was that I was doing it recursively, so exploring each neighbour would fire off a recursion, but very quickly that reached python's recursion limits, which I didn't want to change as it felt a bit like cheating. It was fairly easy to convert the recursive implementation to an iterative one, though.

After looking up how other people do BFS in python I learned about heapq (Python's priority queue data structure).

### Answers
The following is a slightly trimmed version of the output you get from my *runAll.py* file, which runs all the days and prints their answers along with some other statements along the way to the solution.

The full version of this output is in *fullOutputs.txt*

    ########## Day 1
    ##### Answers:
    Fuel for modules only:  3249817
    Total fuel:  4871866
    
    ########## Day 2
    ##### Answers:
    Start opcodes: [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 10, 19, 1, 9, 19, 23, 1, 13, 23, 27, 1, 5, 27, 31, 2, 31, 6, 35, 1, 35, 5, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 5, 51, 2, 10, 51, 55, 1, 5, 55, 59, 1, 59, 5, 63, 2, 63, 9, 67, 1, 67, 5, 71, 2, 9, 71, 75, 1, 75, 5, 79, 1, 10, 79, 83, 1, 83, 10, 87, 1, 10, 87, 91, 1, 6, 91, 95, 2, 95, 6, 99, 2, 99, 9, 103, 1, 103, 6, 107, 1, 13, 107, 111, 1, 13, 111, 115, 2, 115, 9, 119, 1, 119, 6, 123, 2, 9, 123, 127, 1, 127, 5, 131, 1, 131, 5, 135, 1, 135, 5, 139, 2, 10, 139, 143, 2, 143, 10, 147, 1, 147, 5, 151, 1, 151, 2, 155, 1, 155, 13, 0, 99, 2, 14, 0, 0]
    First part answer: 3765464
    Second part answer: 7610
    
    ########## Day 3
    ##### Answers:
    Manhattan distance to closest intersection (part 1) is 870
    Fewest combined steps along wires to reach an intersection (part 2) is 13698
    
    ########## Day 4
    ##### Answers:
    Inefficient looping through each number in range, which was my initial solution
    Part 1: 1790 (0.000 s)
    Part 2: 1206 (0.000 s)
    Matt Jenkins' much nicer solution for generating the numbers
    Part 1: 1790, Part 2: 1206 (0.014 s)
    
    ########## Day 5
    ##### Answers:
    Part 1:
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 0
    Output: 9961446
    Part 2:
    Output: 742621
    
    ########## Day 6
    ##### Answers:
    ('Total orbits (Part 1):', 154386)
    ('Num orbitral transfers between me and Santa (Part 2):', 346)
    
    ########## Day 7
    ##### Answers:
    ('Part 1:', 212460, [3, 2, 0, 1, 4])
    ('Part 2:', 21844737, [8, 5, 9, 6, 7])
    
    ########## Day 8
    ##### Answers:
    Part 1: 2460
    Part 2: v
    
    1    111  1111 1  1 1  1 
    1    1  1 1    1 1  1  1 
    1    1  1 111  11   1  1 
    1    111  1    1 1  1  1 
    1    1 1  1    1 1  1  1 
    1111 1  1 1    1  1  11  
    
    ########## Day 9
    ##### Answers:
    Part 1: (Input 1)
    ('Output:', 2350741403)
    Part 2: (Input 2)
    ('Output:', 53088)
    
    ########## Day 10
    ##### Answers:
    ('Max visible asteroids (Part 1):', 292)
    ('200th destroyed:', 'Vec2(3, 17)')
    ('Part 2: ', 317)
    
    ########## Day 11
    ##### Answers:
    Part 1:
                                                      
             ##                                       
            # #         ##                            
              ##      ####                            
          # ## # ##    # ###    ####   ### ###        
         ## ##        ## # #    #    #    #  #        
      ## ## ##   ##   # ###      #####       #        
      # # #   #  # # ###   #        ## #  # ##        
       ### ##     # ## ## ##  ##     #   #  #  #      
          # #  ##   #  # ##  #  #       # ## ## #     
            #  ## ##    # #  # ####      ## # # ####  
       # # ## ###     ##### ##### #    # # #### ### # 
       ###    #     ###   ##   ###     ## ######## # #
       #  # ###  ########   ####  # ### ### #  ##    #
       # # # #### #   ### #  # # # #  # # #  # ## ##  
       ######### # # #   #   ## # # ### #####  # ### #
     ##  # #  # #  #  # ## ##  ###  ##  #     ##    ##
     #           # # # # ##   # ###    #   #    ###   
     ### ### ###  ## ####    #### # #  ##  # ## # #   
       # ## ## ### ###  # ###### #       ####   #     
     #   # # # ## # ###    # #   # #  ## ##     ##    
      ###  ## ##   # ## # #  ####    # ### # #        
       #  ##   ## # #    #####  #  ##  ## ## ###      
     #    # #  # #  ###### ##   ### #  #   ##         
     #  ## #   #   ###   ###  # # # # ####   #        
      ##  ##     ####  ## ## ## # #     #### # #      
           ##   #  #    # ##  #######  # ####  #      
               # ###  # ## ### ## ##   ### #####      
            ###      ## ###       # # ### #  ##       
            ###  ###     #    ##    # # ###  ##       
              # ## # # ### #  ##    #   ####          
     ## ##   # ####     ##   ###  #  #     ##         
    #  ####  #   # ## ####  #   ### ##      #         
    ### ### ###  # #####  ##  ##   #   ##             
       ## #  #  # ##  ## ##   ## # #### #  #          
       ##    # #### ## # ## ###  ##  ######   #       
      #  #  ###   # # # ## #  #    # # ###  # ##      
      # # ###  #  ### #    #  ### #### #      #####   
        ### # # #    ## #### ### ## # #   #   #    #  
        # # #    ##  #####   ###       #####    ####  
       #   #  #    ## ####   # ######  #     #        
        #    # ##    ## ##   #    ###   ##  ##        
         ### # #  # ##     # ## ##  #    ##           
       #   ## # # # ##      #  ##   ###               
        #  #### ##  ## #  # # #  ###  #               
       # # # # ######  ##    ##    # #                
         ##### # # #   #### ##     ##                 
           # #  ####   # #                            
            ###   ###                                 
           #   #  # #                                 
          # ### # # ##                                
          ##  ####  ##                                
               #  #                                   
               ##                                     
    ('Num panels painted at least once', 1686)
    Part 2:
     ##   ##  ###  ###  #  # #### #  # #      
    #  # #  # #  # #  # # #     # #  # #      
    #    #  # #  # #  # ##     #  #  # #      
    # ## #### ###  ###  # #   #   #  # #      
    #  # #  # # #  #    # #  #    #  # #      
     ### #  # #  # #    #  # ####  ##  ####   
    
    ########## Day 12
    ##### Answers:
    ('Total energy (Part 1):', 5937)
    ('Z cycle is', 96236)
    ('X cycle is', 135024)
    ('Y cycle is', 231614)
    ("The first repeating state is at the step that's the LCD of the inverse of", 135024, 231614, 96236)
    ('Part 2 answer:', 376203951569712)
    
    ########## Day 13
    ##### Answers:
    |||||||||||||||||||||||||||||||||||||
    |                                    
    | ########### # ### ###### ## ###### 
    | ## # #### ##### # ## ####  ### # # 
    |  ###  # ## ####  # ####### # ### # 
    | ########### ###  # # ## ## ##### # 
    | # ## ##########   ### # ##  ## ### 
    | #### #  ### ### # #  ### ###  # ## 
    |  ## ############## #### # ### ###  
    | ## #  ###   # ### ## #######   #   
    |  ##  #### ###  # ## #########   ## 
    | #  ####### # # ############## #  # 
    | ## ### ## # #    ##########  ## ## 
    | ## ##### # #####  #### ## #### # # 
    | ## # ###### ###### ## ### ######## 
    |                                    
    |                o                   
    |                                    
    |                                    
    |                  _                 
    ('Num block tiles (Part 1):', 320)
    ('Final score (Part 2):', 15156)
    
    ########## Day 14
    ##### Answers:
    Ore needed for one unit of fuel (Part 1): 261960
    Fuel created by 1000000000000 ORE (Part 2): 4366186
    
    ########## Day 15
    ##### Answers:
    ('Part 1:', 380)
    ('Part 2:', 410)
    
    ########## Day 16
    ##### Answers:
    Part 1: 96136976
    Part 2: 85600369
    
    ########## Day 17
    ##### Answers:
    ('Part 1:', 4408)
    ['A', 'B', 'B', 'A', 'C', 'A', 'A', 'C', 'B', 'C']
    ('Part 2: ', 862452)
    
    ########## Day 18
    ##### Answers:
    Part 1: 4270
    Part 2: 1982
    
    ########## Day 19
    ##### Answers:
    0#.................................................
    1..................................................
    2..................................................
    3..................................................
    4...#..............................................
    5....#.............................................
    6.....#............................................
    7......#...........................................
    8......##..........................................
    9.......##.........................................
    10........#.........................................
    11........##........................................
    12.........##.......................................
    13..........##......................................
    14...........##.....................................
    15...........###....................................
    16............###...................................
    17.............###..................................
    18.............####.................................
    19..............###.................................
    20...............###................................
    21................###...............................
    22................####..............................
    23.................####.............................
    24..................####............................
    25...................####...........................
    26...................#####..........................
    27....................#####.........................
    28.....................#####........................
    29.....................#####........................
    30......................#####.......................
    31.......................#####......................
    32........................#####.....................
    33........................######....................
    34.........................######...................
    35..........................######..................
    36..........................#######.................
    37...........................#######................
    38............................######................
    39.............................######...............
    40.............................#######..............
    41..............................#######.............
    42...............................#######............
    43...............................########...........
    44................................########..........
    45.................................########.........
    46..................................########........
    47..................................#########.......
    48...................................########.......
    49....................................########......
    Total affected (Part 1):  213
    Part 2:  7830987
    
    ########## Day 20
    ##### Answers:
    ('Part 1: ', 498, '(0.014 s)')
    ('Part 2: ', 5564, '(3.230 s)')
    ('Part 2 using portals instead of tiles as nodes: ', 5564, '(0.029 s)')
    
    ########## Day 21
    ##### Answers:
    Part 1: 19357335
    Part 2: 1140147758
    
    ########## Day 22
    ##### Answers:
    ('Part 1: ', 8502)
    ('Part 2: ', 41685581334351L)
    
    ########## Day 23
    ##### Answers:
    ('First Y value sent to 255', 17740)
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    Restart after idle
    ('First repeated Y value sent to 0 from NAT', 12567)
    
    ########## Day 24
    ##### Answers:
    ('Repeated', 123)
    #####
    ...#.
    ...#.
    ...#.
    #####
    
    ('Biodiversity (Part 1):', 32776479)
    #.#..
    .....
    .#.#.
    .##..
    .##.#
    
    ('Bugs after 200 minutes (recursive):', 2017)
    
    ########## Day 25
    ##### Answers:
    
    
    
    == Hull Breach ==
    You got in through a hole in the floor here. To keep your ship from also freezing, the hole has been sealed.
    
    Doors here lead:
    - north
    - south
    - west
    
    Command?
    
    north
    
    [.... a lot of lines later ..... ]
    
    Trying ('space law space brochure', 'astrolabe', 'prime number', 'mouse')
    
    east
    
    
    
    
    == Pressure-Sensitive Floor ==
    Analyzing...
    
    Doors here lead:
    - west
    
    A loud, robotic voice says "Analysis complete! You may proceed." and you enter the cockpit.
    Santa notices your small droid, looks puzzled for a moment, realizes what has happened, and radios your ship directly.
    "Oh, hello! You should be able to get in by typing 537165825 on the keypad at the main airlock."
    
    FINISHED
