

# Introduction 

CloudPost is a tool which enables to construct your serverless infrastructure in Python code. 

You can define all needed resources in Python code and use them as normal Python objects. CloudPost will handle deployment and management of them on specified backend. 

For now, only Google Cloud Platform is supported but there is a plan to extend it to more backends like AWS.

# Installation

To install CloudPost, run the following 

```sh
pip install cloudpost
```

# Quick Start

First of all, you will need  specific directory structure. To create new project, run:

```sh
mkdir test-project
cd test-project
cloudpost init
```

Now you should see `src` directory where you will store your components. Example of structure would be:

```
src/
    component1/
        main.py
        ....
    component2/
        main.py
lib/
    mylibrary.py
```

Every component has to have `main.py` file where you define your serverless functions. 

Checkout [filestore example](./filestore_example) to see how you can use cloudpost API.

Before doing deployment, checkout section "Configuring environment"

to do deployment, you just need to execute the following:

```sh
cd test-project
cloudpost deploy
```

If you want to test your solution in local, run:

```sh
cd test-project
cloudpost run
```


# Configuring Environment

## GCP 

You will need to setup your `gcloud` CLI tool and export your credentials:

    export GOOGLE_APPLICATION_CREDENTIALS="/home/stefan/.gcloud/key.json"

Also, on GCP account, you will have to enable certain API permissions:

    roles/apigateway.serviceAgent
    roles/apigateway_management.serviceAgent
    roles/cloudbuild.builds.builder
    roles/cloudbuild.serviceAgent
    roles/cloudfunctions.serviceAgent
    roles/compute.serviceAgent
    roles/containerregistry.ServiceAgent
    roles/editor
    roles/eventarc.serviceAgent
    roles/firebaserules.system
    roles/firestore.serviceAgent
    roles/owner
    roles/pubsub.serviceAgent
    roles/run.serviceAgent

Also, since datastore cannot be created through any API, you will need to create it manually and enable it before you do any deployments.