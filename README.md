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

>Code should be created by the writer, clearly citing any outside resources whe used; being added alonside the documentation.

> Code should be self-documenting, only detailing comments when code is complicated/overwhelming

> Features should be in their own branches, merged through pull requests through github

> Development environment should be easily reproducible and documented.

> Logic should be abstracted into classes and functions into seperate files/functions; avoiding duplicate code or long blocks
>> Breaking functions into smaller chunks, related functions into their own files, related files into their own folders, etc.

<small>Last Updated: 1/21/2026</small>

**Meetings and Communication**

> Group communication should be held regularily through a discord chat with all members included. Additional meetings can also be discussed and held when members are available through the discord. Decisions and actions should be mutually agreeed upon, finding workarounds or compromises. Responses should generally be returned in at least a day or two.

**Tools**

> Python is the main language of development, using python's built-in environment (.venv) to handle reproducible environments (also nix for OS-specific environments; don't worry about it). Packages should be listed in the requirements.txt file, adding/contributing to it as the documentation below states. Testing should be provided in its own file in a seperate folder to easily re-run tests (subject to move to github actions). Github to handle version control and collaborative development.

**Development Methology**

> Readable, maintainable code. Proper documentation where needed. Docstrings on function headers as well as type hinting where applicable. As stated above, Logic should be abstracted into classes and functions into seperate files/functions; avoiding duplicate code or long blocks; breaking functions into smaller chunks, related functions into their own files, related files into their own folders, etc.


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