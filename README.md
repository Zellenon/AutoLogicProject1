# AutoLogicProject1

## Usage

Below, we outline some steps to run the project, along with their associated terminal commands.

1. Clone the directory and cd into the project repo \
   `git clone https://github.com/Zellenon/AutoLogicProject1` \
   `cd AutoLogicProject1`
3. Switch to the `merged-solvers` branch \
    `git fetch` \
    `git switch merged-solvers`
4. Run the test script. The test script will iteratively run the solver on each test 
   file in the `project1-tests` directory. It imposes a timeout of 10 seconds for each test case. \
    `./run_tests.zsh`
5. Call the project on a single .cnf file \
    `python3 main.py <filename>`
6. Use pip to install any necessary dependencies  \
    `pip install <missing-package>` OR \
    `pip3 install <missing-package>`
