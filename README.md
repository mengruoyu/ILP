## About The Project

This project is used to numerically compute the feasibility of the ILP in the paper. 


## Prerequisites

Before installing and using this project, please make sure you have the following prerequisites installed on your machine:

- Anaconda 3
- Python 3 (The author used version 3.10)
- Gurobi Conda Package (The author used version 10.01)
- Gurobi License
- Numpy Package

## Installation


### Windows
#### Anaconda 3
Download the exe file and install it. Download link and installation instruction can be found at [Anaconda3 Installation](https://www.anaconda.com/products/distribution)

#### Python 3:
  Anaconda 3 should have python 3.10 installed if you installed it from the link above. 

In the case that Anaconda 3 is using a python version that is not supported, create an new environment for verision 3.7-3.11. We use the procedure is at [Conda Manage Environments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).
Here, we show the example of creating an environment with python 3.10.

Open a terminal:
![open anaconda prompt](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_create_evn_0.png)

Create new python 3.10 environment with name py3_10:
```bash
conda create --name py3_10 python=3.10
```
When conda asks you to proceed, type y:
```bash
$ proceed ([y]/n)?
```
To activate this environment, use
```bash
conda activate py3_10
```
To deactivate this environment, use
```bash
conda deactivate py3_10
```

#### Gurobi conda package
We use the procedure at [How do I install Gurobi for Python?](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python-)

Open an Anaconda Prompt, type:
```bash
conda install -c gurobi gurobi=10.0.1
```

#### Gurobi License
We use Gurobi as the ILP solver of our problem. We use the free Academic Named-User License. We follow [this guide](https://www.gurobi.com/features/academic-named-user-license/) to generate and activete the license.

#### Numpy package
Open an Anaconda Prompt, type:
```bash
conda install numpy
```
The documentation of installing Numpy can be found at [Installing Numpy](https://numpy.org/install/)



### Linux
#### Anaconda 3
We use the precedure at [Installing on Linux](https://docs.anaconda.com/anaconda/install/linux/)


#### Python 3:
Open a terminal and create new python 3.10 environment with name py3_10:
```bash
conda create --name py3_10 python=3.10
```
When conda asks you to proceed, type y:
```bash
$ proceed ([y]/n)?
```
To activate this environment, use
```bash
conda activate py3_10
```
To deactivate this environment, use
```bash
conda deactivate py3_10
```


#### Gurobi conda package
We use the procedure at [How do I install Gurobi for Python?](https://support.gurobi.com/hc/en-us/articles/360044290292-How-do-I-install-Gurobi-for-Python-)

Open an Anaconda Prompt, type:
```bash
conda install -c gurobi gurobi=10.0.1
```

#### Gurobi License
We use Gurobi as the ILP solver of our problem. We use the free Academic Named-User License. We follow [this guide](https://www.gurobi.com/features/academic-named-user-license/) to generate and activete the license.

#### Numpy package
Open an Anaconda Prompt, type:
```bash
conda install numpy
```
The documentation of installing Numpy can be found at [Installing Numpy](https://numpy.org/install/)

### Some errors the author encountered and how the author fix them
#### Conda command not found
Error description: Suppose Conda is installed on a Linux system. In the terminal, typing
```bash
conda
```
returns
```bash
$ conda: command not found
```

Solution: We need to ad PATH environment variable to .bashrc file, i.e. add this to .bashrc
```bash
export PATH="/home/username/miniconda/bin:$PATH"
```
One way of doing this is the following using vim. Type
```bash
vim ~/.bashrc
```
and press "i" to switch to insert mode, move to the end of this file and insert
```bash
export PATH="/home/username/miniconda/bin:$PATH"
```
Press Esc key. Then, enter :wq to save and quit vim. Then activate the modified .bashrc by running
```bash
source ~/.bashrc
```

#### conda takes forever at solving environment when installing packages
Description: When running "conda install xxx-packge", it takes forever or fail to solve the environment.

Solution: The author fixed this by running
```bash
conda config --set channel_priority flexible
```

## Usage

Our project contains two py files, the "generate_collision.py" and the "ILP_gurobi.py". 

### Instruction on generate_collision.py
The "generate_collision.py" file generate an npy file named collision_n. The collision_n.npy stores all pairs (b1,c1,b2,c2) s.t. (b1,c1)~_{GIP}(b2,c2) where n is the length of each vector.
To generate a file to store pairs of vector length k, replace the row "n=4" below by "n=k" and run this file. 
We use the case k=1 for example. 
#### Step 1: replace "n=4" by "n=k"
![step1](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_create_collision_0.png)
#### Step 2: run the file
##### Windows
Open Spyder in Anaconda.Navigator.
![step1.5](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_create_collision_2.png)
Run the file.
![step2](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_create_collision_2.png)
##### Linux
Type (making sure the py3_10 environment is activated)
```bash
python3 generate_collision.py
```
Next, we wait patiently for the program to terminate. Even when n=4, this took around 10 hours. 

As an example, we have already calculated cases n=1-4 and uploaded the files collision_1.npy-collision_4.npy respectively.

### Instruction on ILP_gurobi.py
ILP_gurobi.py run the ILP and store the result in the "log.txt" file.
To run ILP_gurobi.py, we need to set 3 parameters in the file. They are the following:
- n, the variable representing the length of each vector
- lb, the variable representing the number of labels used by Bob
- lc, the variable representing the number of labels used by Carol
Also, if we set n=k, then we must have the file collision_k.npy prepared. 

Once these are ready, we can run the file. Depending on the choice of n, lb, lc, the amount of time for the program to terminate varys, because the number of constrains and variables increases exponentialy w.r.t our parameters n,lb,lc.

After the program is terminated, we can check the result in the following way.
Open log.txt file and scroll down to the bottom. 
If the ILP is infeasible, then we will see that 

```bach
Solution count 0

Model is infeasible
```
If the ILP is feasible, then we will see that 
```bash
Solution count 1: 0

Optimal solution found (tolerance 1.00e-04)
```
The following is an example to run the file.

#### Step 1: set up n,lb,lc
We set n=2,lb=1,lc=27
![Step1_ILP](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_run_IL_0.png)

#### Step 2: Run the code
##### Windows
Open Spyder in Anaconda.Navigator.
![step1.5](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_create_collision_2.png)
Run the file.
![Step2_ILP](https://github.com/mengruoyu/ILP/blob/master/readme_img/img_run_IL_1.png)
##### Linux
Type (making sure the py3_10 environment is activated)
```bash
python3 ILP_gurobi.py
```
Next, we wait for the program to terminate. Since the size of ILP increases exponentially w.r.t. our parameters n,lb,lc, it may take very long time for the program to terminate when n,lb,lc are large.

After the program is terminated, open the log.txt file and we are expected to see the following
![result](https://github.com/mengruoyu/ILP/blob/master/readme_img/result.png)
At the bottom, we can find 
```bash
Solution count 1: 0

Optimal solution found (tolerance 1.00e-04)
```
Therefore, under this setting, the ILP is feasible. (Carol can just send her vectors to Alice since she has 27 labels. Alice can calculate Bob's vector from the promise. Therefore, Alice can calculate the function value.)

If we set n=3,lb=1,lc=17 and run the file, we are expected to see the following in the log.txt
![result1](https://github.com/mengruoyu/ILP/blob/master/readme_img/result1.png)
```bash
Solution count 0

Model is infeasible
```
Therefore, under this setting, the ILP is infeasible.

The log.txt file is stored in this project at [log_2_1_27.txt](https://github.com/mengruoyu/ILP/blob/master/readme_log_example/log_2_1_27.txt) and [log_3_1_17.txt](https://github.com/mengruoyu/ILP/blob/master/readme_log_example/log_3_1_17.txt).


















