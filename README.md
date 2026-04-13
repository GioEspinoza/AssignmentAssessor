    # AssignmentAssessor: the smart planner for Students!!
    ## Video Demo:
    ## Description: 
    ###AssignmentAssessor is a python program that will work through the command line to help students maintain order in their assignments by keeping track of tasks and there due dates, accounting for difficulty and estimated study time. AssignmentAssessor will calculate task priorities and help students by providing recommended study plans so students can get the most important assignments off the table! The goal is to help students stop procrastinating and have an assistant to the side that keeps track of the assignments we all lose track of by identifying how important which tasks are. AssignmentAssessor calculates this through a priority score for each task by multiplying the difficulty by hours needed divided by days remaining before due date. The program offers user friendly menus with all the options.
    
    ##assignment addition
    ### when adding an incomplete assignment Assignment Assessor will need a few things, such as course name, assignment name, due date, difficulty rating(1-5), and the estimated hours needed to complete. My input validation functions make sure all input given is correct and maintain order in AssignmentAssessor. 

    ##Priority calculation
    ###As stated previosly, assignment assessor will determine how important tasks are using the following formula: Priority = (difficulty x hours req)/days left. Ensuring that the assignments that are the hardest and most time consuming, but also with the closest due dates, are given the most priority helping Assignment Assessor provide the user with the most important reliably!

    ##Study plans
    ### AssignmentAssessor will generate study plans by listing all assignments based off priority score and then using the formula: Hours per day = total hours req / days remaining. Assignment Assessor will also suggest how many hours a day the student should put aside for the assignment and will also account for whether or not the assignment is overdue or not. Marking them as OVERDUE.

    ##Task completions
    ###in assignment assessor students can also mark tasks that were due and are now completed to maintain organization. ASsignment assessor will not only mark them as completed but will also record the date the student completed them. in future updates the program may analyze this data and further personalize study plans for the student.

    ##tests
    ###alongside the assignment assessor program, this project includes several automated tests using pytest which helps confirm that assignment assessor is properly validating range for the difficulty values, validating the integers given for any numeric input, validating due dates based off format and whether or not its in the future or not as vice versa for completion dates, and validating if the decimal rounding used for study plan is valid logic. These thorough automated tests have helped ensure that important parts of Assignment Assessor are working or not! 

    ##Libraries
    ###assignment assessors only requires 2 libraries which can be found in the requirements.txt file.

    ##Note: tasks.json and user_prof.json are not included. They will be created automatically when you run the program.