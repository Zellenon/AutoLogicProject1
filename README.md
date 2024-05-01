# AutoLogicProject1

## Usage

Our solver is implemented in Python 3.11.7, but we anticipate it should be compatible with any version >= 3.5.
Below, we outline some steps to run the project, along with their associated terminal commands. 

1. Clone the directory and navigate into the project repo. \
   `git clone https://github.com/Zellenon/AutoLogicProject1` \
   `cd AutoLogicProject1`
3. Switch to the `merged-solvers` branch. \
    `git fetch` \
    `git switch merged-solvers`
4. You may need to use `pip` to install missing dependencies. In particular, the `typing` package is required. Skip this step for now, but come back after step 5 or 6 if necessary.  \
    `pip install <missing-package>` OR \
    `pip3 install <missing-package>`
5. Run the test script. The test script will iteratively run the solver on each test 
   file in the `project1-tests` directory. It imposes a timeout of 10 seconds for each test case. \
    `./run_tests.zsh`
6. You can also call the solver on a single `.cnf` file. \
    `python3 main.py <filename>`
