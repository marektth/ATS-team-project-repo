# Database Files

1. If you want to enter a new job into the database, you have to edit the jobs_table.json, the code block is explained in README.md
2. If you want to enter a new employee into the database, you have to edit the employees_table.json, the code block is explained in README.md
3. If you want to enter a new rule into the database, you have to edit the rules_table.json, the code block is explained in README.md
4. If you want to enter a new team into the database, you have to edit the teams_table.json, the code block is explained in README.md

# Deployment of the system

The whole architecture is written in Terraform, every single block of code is explained inside the README.md file.


# Usage of the system - Employee view

1. Once you have the website opened, you will see the current employee with his ID.
If you want to switch to a different employee (fe. from 62 to 69), you enter the ID 69 and hit the ENTER key to confirm the change.

2. In order to create a new entry you choose the FROM and UNTIL date and select your desired absence type and enter the reason.

3. Once you click submit, the changes should show up immediately.

4. In order to delete your request you have to click on the "X" symbol of the given row and follow the onscreen instructions.

# Usage of the system - Manager view

1. The manager will see all of the requests of the teams assigned to him.

2. For presentations sake there is a "Decide" button present which triggers the decision algorithm (this can take up to 5seconds.)

3. Once the decision is done the manager will see the output immediately.

4. The decision algorithm is also triggered daily at 18:00 and a mail notification system is triggered at 18:01.

