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
<small>Last Updated: 22/01/2026</small>

- [x] Finalize project governance document
- [ ] Finalize project management document
- [ ] Develop data structures for input files and instructions
- [ ] Develop file reading and validation
- [ ] Create test functions for file reading, parsing, and scanning

### Week 4
<small>Last Updated: 22/01/2026</small>

- [ ] Develop interference graph for live variables

### Week 5
<small>Last Updated: 22/01/2026</small>

- [ ] Develop and execute a graph colouring algorithm to assign registers to live variables

### Week 6
<small>Last Updated: 22/01/2026</small>

- [ ] Complete initial test runs of assembly code generation

### Week 7
<small>Last Updated: 22/01/2026</small>

- [ ] Ensure code generation is fully functional by this point
- [ ] Begin planning Haskell solution


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