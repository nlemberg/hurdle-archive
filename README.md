# Hurdle Archive

Are you familiar with Wordle? Of course you are. Hurdle is its nerdier sibling. [Try it out!](https://hurdlegame.io/)

I'll admit I was hooked. One game a day was not enough, and so I created Hurdle Archive.

## Overview

Hurdle Archive is a web application that lets registered users play and track their Hurdle games. It extends the single daily game experience of Hurdle to an archive of thousands of games.

## Tech Stack

- **Backend**: Flask
- **Database**: MySQL
- **Reverse Proxy**: Nginx

## Architecture

Here's an overall look at the architecture:

![dockerized_app.png](./docs/dockerized_app.png "App Architecture")

## Context

This app is part of my DevOps portfolio, showcasing my skills and training. My aim is to improve it over time. The other parts of this portfolio can be found here:

- [Infrastructure repo](https://github.com/nlemberg/hurdle-archive-infra): Contains Terraform code for provisioning the necessary AWS resources and deploying the app on an EKS cluster.
- [GitOps repo](https://github.com/nlemberg/hurdle-archive-gitops): Contains configuration files and manifests responsible for the continuous deployment of the apps in the cluster.

## Project Workflow

Here's an overview of the entire project's components:

![general_workflow.png](./docs/general_workflow.png "Project Workflow")
