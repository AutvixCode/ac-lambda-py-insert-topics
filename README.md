# ac-lambda-py-template
Template created to serve as the default start point of all lambda function in Autvix Code.

### Directory structure
```
.
├── .github
│   └── workflows
│       └── workflow.yml // Github Actions cI/CD workflow
├── .gitignore // gitignore file pre-loaded with python gitignore references
├── infra  
│   ├── samconfig.toml // Configurations used in "sam deploy"  
│   └── template.yaml  // Configuration used in "sam build"
├── README.md  // Readme of Repo
└── src  
    ├── cicd_requirements.txt  // Libs installed that will be downloaded in the ci/cd step of Github Actions
    ├── code  
    │   ├── app.py  // main code of the lambda function
    │   └── __init__.py  
    ├── __init__.py  
    ├── requirements.txt  // Libs installed in the momment of build (unused, use existing layers in the AWS Organization instead)
    └── tests  
        ├── conftest.py  // File with fixtures of some AWS services like DynamoDB, Cognito and SSM Parameter Store
        ├── __init__.py  
        └── test_dummy.py // File with a dummy test to see if pytest is working properly
```

### CI/CD Workflow
The Github Actions CI/CD workflow is used to deploy the lambda to AWS CloudFormation and will be triggered in three cases:
- Manual dispatch
- Push to main branch
- Pull request to main branch

The CI/CD workflow have also three serialized jobs:
- Setting Python Machine: Downloads the libraries specified in the two requirements.txt files.
- Testing and linting: Runs pytest and pylint in src folder to ensure that the code styling and
  functioning is okay, if not, the workflow will be stopped with an error.
- Deploy to AWS: Runs "sam build" and "sam deploy" commands to send the function to CloudFormation, if
  something goes wrong, will be stopped with an error

Obs: if the source code and template are equal current template and code to be commited (if you change only readme, for example), 
the sam deploy will stop in a error saying that the code is already up-to-date, so desconsider this. 
