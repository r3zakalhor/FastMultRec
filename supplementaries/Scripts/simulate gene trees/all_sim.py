import os


#2WGD
params = [ 
            ["sim_2WGD_D7", "f:1e-7"],
            ["sim_2WGD_D10", "f:1e-10"],
            ["sim_2WGD_D15", "f:1e-15"],
            ["sim_2WGD_D18", "f:1e-18"],
            ["sim_2WGD_LN0.3", "ln:gb,0.3"], 
            ["sim_2WGD_LN0.1", "ln:gb,0.1"]
         ]
for p in params:
    command = "bash simualte_2WGD_simphy.sh \"" + p[0] + "\" \"" + p[1] + "\""
    print("running: " + command)
    #os.system(command)




#1WGD
params = [ 
            ["sim_1WGD_D7", "f:1e-7"],
            ["sim_1WGD_D10", "f:1e-10"],
            ["sim_1WGD_D15", "f:1e-15"],
            ["sim_1WGD_D18", "f:1e-18"],
            ["sim_1WGD_LN0.3", "ln:gb,0.3"], 
            ["sim_1WGD_LN0.1", "ln:gb,0.1"]
         ]
for p in params:
    command = "./simualte_1WGD_simphy.sh \"" + p[0] + "\" \"" + p[1] + "\""
    print("running: " + command)
    #os.system(command)
         
         
#0WGD
params = [ 
            ["sim_0WGD_D7", "f:1e-7"],
            ["sim_0WGD_D10", "f:1e-10"],
            ["sim_0WGD_D15", "f:1e-15"],
            ["sim_0WGD_D18", "f:1e-18"],
            ["sim_0WGD_LN0.3", "ln:gb,0.3"], 
            ["sim_0WGD_LN0.1", "ln:gb,0.1"]
         ]
         
for p in params:
    command = "bash simualte_0WGD_simphy.sh \"" + p[0] + "\" \"" + p[1] + "\""
    print("running: " + command)
    os.system(command)
         
