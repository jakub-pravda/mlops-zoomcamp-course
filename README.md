# My journey through MLOps Zoomcamp

## Useful links

* Dataset used in experiments [NY taxi dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

# Notes

TODO: move me to a separate `.md`

## Week #1 - MLOps intro

> MLOps is a set of practices for automating your machine learning workflow and effectively working in a team during all phases of machine learning development.

Each machine learning project has 3 phases: 

* **Design**
* **Train**
* **Operate**

### MLOps maturity model

Maturity model has 4 levels (0 - no MLOps, 4 - fully automation)

- LEVEL 0. **NO MLOPS**
    - All code in Jupyter notebooks
    - No automation
    - Typically data scientist works alone
- LEVEL 1. **DevOps only**
    - Releases are automated
    - CI/CD pipeline exists
    - Tests exists
    - OPS metrics
    - Contains best practices from DevOps, but any ML related stuff still missing 
    - No experiment tracking, No reproducibility, Data scientists are separated from engineering team
- LEVEL 2. **Automated training**
    - Training pipeline
    - Experiment tracking exists
    - Model registry exists
    - Low friction deployment
    - Data scientists are working with engineering team
- LEVEL 3. **Automated deployment**
    - Easy to deploy model in this phase (preferable through some API)
    - A/B tests exists (model performance tests)
    - Model monitoring exists
- LEVEL 4. **Full MLOps automation**
    - Everything is automated as much as possible, engineers works only on pipeline improvements, but there aren't part of the pipeline process


## Week #2 - Experiment tracking

Experiment tracking is the process of keeping track of all the **relevant information** from an ML experiment, which includes:

* Source code
* Environment
* Data
* Model
* Hyper-parameters
* Metrics
* ...

Why is the experiment tracking importnant?

* Reproducibility
* Organization
* Optimization

### MLflow

> An open source platform for the machine learning lifecycle. It focuses on experiment tracking and model management.

Contains four modules:

* Tracking
* Models
* Model Registry
* Projects

The MLflow tracking module allows you to organize your experiments into runs, and to keep track of:

* Parameters
* Metrics
* Metadata
* Artifacts
* Models

### Model management

Part of the MLOps pipeline, model management contains following sections:

* **Experiment tracking**
* **Model versioning**
* **Model deployment**

### Model registry server

The model registry component is the centralized model store, set of APIs and UI, to collaboratively manage the full lifecycle of MLflow model. It provides: 

* Model lineage
* Model versioning
* Stage transitions
* Annotations

### Remote tracking server

Remote tracking server can be easily deployed to the cloud. Some benefits of it: 

* Share experiments with other data scientists
* Collaborate with others to build and deploy the models
* Give more visibility of the data science efforts

## Week #4 - Deployment

> How to deploy trained model?

* Do we want to predictions immediately? **Online deployment**
  * *Run all the time*
  * **Web services** or **Streaming**
* Can we wait for the predictions? **Offline (batch) deployment**
  * *Run regularly*

### Offline deployment (Batch mode)

> We run model regularly (hourly, daily, monthly, ...)

* A typical example is customer churn predictions. We can run these predictions on a daily basis, as churn typically takes some time for a customer to decide to switch to a competitor

### Online deployment

> We run predictions immediately

#### Web service

* Typically we have some UI frontend, that's communicating with backend
* Example could be ride duration service for taxi companies. Customer needs to know how long the trip will take before the service ordering

#### Streaming service

* Producer, consumer architecture