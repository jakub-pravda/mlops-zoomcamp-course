# My journey through MLOps Zoomcamp

## Useful links

* Dataset used in experiments [NY taxi dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

# Notes

TODO: move me to a separate `.md`

## Week #1 notes

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
