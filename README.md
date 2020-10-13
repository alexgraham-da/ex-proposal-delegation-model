### About
POC of a DAML model for the scenario of an employee making a proposal to a company on the behalf of their employer, with the employees of the other company accepting or rejecting the proposal. It is designed to be an example of how DAML can separate the company party from the employee parties who can act on behalf of it, without having to rely on an external IAM/RBAC.

Included in this repo is a DAML model as well as a DAML Trigger that is run as each company party.

Each company has a public and a private contract. A company can have any number of employees who are completely private to other companies. Employees are given access from the company to perform various actions on, or on behalf of the company. After bootstrapping, the company party does not need to be used to perform any action.

The proposal workflow:
-   An employee of a  **Company A**  can make a proposal to  **Company B**
-   Employees of  **Company B**  can then accept or reject the proposal
-   When the proposal is accepted or rejected, a notification is sent to the employees of  **Company A**.

This workflow is interesting in that it is the parties of the _employees_ of a company that are making and accepting the proposals. Under a single party model, the company's party would have to make and accept the proposals themselves - this would require employees to have to share access to the company's party, without any way for the company to give employees different levels of access and responsibility.

#### What’s going on under the hood:
-   Each Company has a public `Company` contract (that is shown through the `Public` party) with public info like the company’s name, and a private `CompanyInternal` contract that has information such as the list of employees as well as any internal choices an employee can make. As an example, a manager can change the company’s name.
-   When an Employee of  **Company A**  makes a `Proposal` to  **Company B**, the trigger running as  **Company B** will create a private `DelegatedProposal` contract for each employee at  **Company B**, who can then accept or reject the proposal.
-   Since the employee can’t see the original proposal, when the choice is exercised on a `DelegatedProposal`, it will create a `DelegatedProposalAction`. based on that, the  **Company B’s**  trigger will automatically resolve the original `Proposal` (the `Proposal` accept/reject choices create the `Notification`) and clean up any remaining `DelegatedProposal`s
-   **Company A’s** trigger will create  `Notification`s for each of their employees (the original  `Notification`  is only seen by the company party)

#### The model
The model separates the public space where information about the companies live, and the private space, where internal company information lives. The company’s private space is then split between the company and the employees, who can be authorized or delegated to perform different actions based on who the employee is. For example, the trigger currently delegates all proposals to all employees, but it could also delegate to different groups of employees (who might then delegate to other employees individually/manually).

#### Running
The model can be run on DABL, or to test it out locally with the bootstrapped data in `daml/Setup.daml`, you can run `make start_daml_server`. When the DAML Navigator tab pops up, run `make start_triggers` to start the triggers.

Alternatively, you can run `daml start` in the root directory, then `./run_trigger.sh CompanyA` and `./run_trigger.sh CompanyB` in separate bash sessions from the `triggers` folder.
