import streamlit as st

"""
# How Does it Work

- `Jupyter` notebooks and python scripts for experimentation and model building
    - We track our experiments to `Mlflow`, local tracking server
    - Using custom wrapper class to interface `Mlflow` with `sktime` estimator
- Data files and model artifacts are tracked with `DVC`, synced to remote `S3` storage
- `Github actions` for **Continuous Deployment** on merge to Main
    - Build `Docker` image for `Lambda function`
        - Multi-stage build keeps image size <300Mb
        - Model artifacts are baked into `Docker` image (see todo list)
        - Image is pushed to `ECR`
    - Run `Terraform` scripts to spin up cloud infrastructure
        - `Lambda function`
        - `IAM` roles
        - `Cloudwatch` for monitoring
- `Lambda` function acts as **serverless abstraction** for all inference requests
    - Model predictions requested through `boto3` lambda invocation
    - Authentication to `Lambda` requires `IAM` credentials
    - Logs activity to `Cloudwatch` for monitoring usage
- This `Streamlit` app provides an interactive way
    - Uses `DVC` to access versioned data files for plotting etc
    - `Lambda` communication logic abstracted away in custom `energy_forecast` package


"""
