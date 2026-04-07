# Register Allocation Program for a Simple Compiler

## Project Governance

### Project Mission and Vision

<small>This would really go well as instructions to an LLM</small>

**Mission**
>  Implementing register allocation for a simple compiler’s code generator


**Vision**
> To be able to reach all listed program requirements in a working, tested state. That is, all main functionality, intended behaviours, error handling, as well as optionally completing stretch goals if time permits. Implementing functionality in a well-formatted manner with structured documentation to our groups standard.

**Values**
> Consistent and clear communication between group members, indicating what should be worked on/discussed throughout the development process.


### Group Policies
>If any issues in implementation arises, civil discussion to resolve any conflicts should be done; escalating early on if problems persist. 

>Code should be created by the writer, clearly citing any outside resources when used; being added alongside the documentation.

> Code should be self-documenting, only detailing comments when code is complicated/overwhelming

> Features should be in their own branches, merged through pull requests through github

> Development environment should be easily reproducible and documented.

> Logic should be abstracted into classes and functions into separate files/functions; avoiding duplicate code or long blocks
>> Breaking functions into smaller chunks, related functions into their own files, related files into their own folders, etc.

<small>Last Updated: 1/21/2026</small>

**Meetings and Communication**

> Group communication should be held regularly through a discord chat with all members included. Additional meetings can also be discussed and held when members are available through the discord. Decisions and actions should be mutually agreed upon, finding workarounds or compromises. Responses should generally be returned in at least a day or two.

**Tools**

> Python is the main language of development, using python's built-in environment (.venv) to handle reproducible environments (also nix for OS-specific environments; don't worry about it). Packages should be listed in the requirements.txt file, adding/contributing to it as the documentation below states. Testing should be provided in its own file in a separate folder to easily re-run tests (subject to move to GitHub actions). Github to handle version control and collaborative development.

**Development Methodology**

> Readable, maintainable code. Proper documentation where needed. Docstrings on function headers as well as type hinting where applicable. As stated above, Logic should be abstracted into classes and functions into separate files/functions; avoiding duplicate code or long blocks; breaking functions into smaller chunks, related functions into their own files, related files into their own folders, etc.

**Division of Labour**

> Work will be divided by logic/features that need to be added. Group members will select a feature that needs to be added or one they are comfortable with, and begin working and implementing it. In order to prevent two members from working on the same feature accidentally we will be incorporating some form of project management (e.g., Trello). Group members working on feature that require completion from a different feature that has yet to be implemented will simply create fake data in order to test their logic in the meantime. There will be frequent meetings and check-ins to ensure everyone is on the same page and project development is proceeding smoothly.

**Code and Documentation Standards**

> Currently, PEP 8 will be used as the existing coding standard in Python for this project. For classes, functions docstrings will be created explaining the behaviour, arguments, what is returned, and any other important information. Detailed comments will be done throughout the code to explain why certain things are done. In addition, if outside resources are used citations will be explicitly stated in the comments.

**Quality Assurance and Review**

> There will be a test folder which will hold all the unit tests as well as hold sample data to use against the logic/features before integration to ensure they are working as intended. After a feature is created and tested it will be submitted through GitHub (pull requests), so that it requires the approval of at least one other group member (with them testing it and reviewing it as well)

**Development Logs**

> GitHub Issues will be the primary development log for known issues, bugs and/or limitations that are present within the program. When a bug is discovered, it will be documented by creating an issue within Github. After steps are taken to fix the bug, a description of the steps were taken to fix said bug will be noted and the issue will be marked as resolved.

**Team Member Responsibilities**

> Group members are expected to attend group meetings. If unable to, the member must notify the group. 

> Group members are expected to check Discord regularly and provide a reply within 48 hours.

> Group members must complete their work before deadlines. If unable to, the member must notify the group.

> Group members are expected to check GitHub regularly for any issues, Pull Requests, etc.

> Group members are expected to attend the group presentations with the instructor.

## Plan Approvals
### Week 3
<small>Last Updated: 12/02/2026</small>
- [x] Finalize project governance document
- [x] Finalize project management document
- [x] Develop data structures for input files and instructions
- [x] Develop file reading and validation
- [x] Create test functions for file reading, parsing, and scanning

### Week 4
<small>Last Updated: 12/02/2026</small>
- [x] Develop variable liveness algorithm
- [x] Develop interference graph for live variables

### Week 5
<small>Last Updated: 02/03/2026</small>
- [x] Develop and execute a graph colouring algorithm to assign registers to live variables

### Week 6
<small>Last Updated: 02/03/2026</small>
- [x] Complete initial test runs of assembly code generation
- [x] Go over tests from previous modules and add more coverage if needed. This is crucial before continuing to next step.

### Week 7
<small>Last Updated: 02/03/2026</small>
- [x] Ensure code generation is fully functional by this point
- [x] Begin planning Haskell solution

### Week 8
<small>Last Updated: 06/04/2026</small> <br>
**From here onwards, all reference to code modules is referring to the Haskell implementation unless otherwise stated.**
- [x] Prepare for project check-in meeting
- [x] Discuss next steps for imperative solution as Haskell solution begins

### Week 9
<small>Last Updated: 06/04/2026</small>
- [x] Complete finishing touches and ensure code generation is fully functional one last time before project check in
- [x] Project Check In

### Week 10
<small>Last Updated: 06/04/2026</small>
- [x] Develop representations for main data structures as well as supporting functions for the modules
  - `Token` - **Complete**
  - `Instruction` (Three-address instruction) - **Complete**
  - ~~`Assembly` (Assembly language instruction)~~
- [x] Write test plans and implement full-coverage tests for each implemented module (implement then test)
  - **Modules Tested**: `Token`, `Instruction` 

### Week 11
<small>Last Updated: 06/04/2026</small>
- [x] Develop modules:
  - `InterferenceGraph` - **Complete**
  - `Liveness` - **Complete**
  - `Assembly` (Assembly language instruction) - **Complete**
- [x] Implement graph colouring (register allocation) within the `InterferenceGraph` module
- [x] Write test plans and implement full-coverage tests for modules

### Week 12
<small>Last Updated: 06/04/2026</small>
- [x] Develop modules:
  - `AssemblyGenerator` module responsible for creating a sequence of `Assembly` language instructions - **Complete**
  - ~~`Assembly output` module that writes `AssemblyGenerator` result to output file~~
- ~~[] Write test plans and test the `AssemblyGenerator` module~~

### Week 13
<small>Last Updated: 06/04/2026</small>
- Continue writing tests and refining modules for readability
- Write proper test plans for Python modules; rewrite tests as needed & add tests for better coverage
- Complete a code review of Python (imperative) solution:
  - Find typos (in comments, function definitions, code, etc...)
  - Refactor for readability / efficiency
  - Remove redundant comments

### Week 14
<small>Last Updated: 06/04/2026</small>
- Develop modules:
  - `Assembly output` module that writes `AssemblyGenerator` result to output file
  - `Scanner` to read file input
  - `Parser` to parse file input into `Token` types

## Developing and Contributing
### Pull Requests
- Before doing any changes, make sure we pull newest changes from main
```sh
git checkout main
git pull origin main
```
- For any new feature/change, we create a new branch:
- We name the branch in the following format:
  - **category/name**
  - for example:
    - feat/graph-implementation
    - fix/linked-list-null-pointer
    - chore/scripts-function-documentation
```sh
# Take graph-implementation as an example
git checkout -b feat/graph-implementation
```

- Now, make any changes regarding this feature/area, only to its related branch
```sh
git add .
git commit -m "some commit message"
git push
```
- Once your changes are tested and finalized, go into the repository on github and into your branch
  - Here, you find a "contribute" button which will let you create a new pull request
- The pull request title should be in the format:
  - general-category(specific-category): description
  - in our example case, we can use something like the following:
    - feat(data-structure): graph implementation 
- Now, another member or yourself can approve or deny the pull request, as well as make any comments through the pull request menu.
- We can also delete the branch to keep things clean.


## Python Environment
### Initilization/Usage
1. Initialize a python virtual environment

```sh
python -m venv .venv
```

2. Enter the python environment


```sh
# macOS/Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (Powershell)
.venv\Scripts\Activate.ps1
```

3. Install Packages from requirements.txt

```sh
pip install -r requirements.txt
```
---
### Installing packages
1. Make sure you are in the virtual environment *(see [above](#initilizationusage))*
2. Install previously installed packages from requirements.txt *(also see [above](#initilizationusage))*
3. Install new package
```sh
pip install foo
```
4. Store any new packages in requirements.txt
```sh
pip freeze > requirements.txt
```
---