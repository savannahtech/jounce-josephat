## About

A tool that benchmarks the performance of various Language Learning Models (LLMs) against the quality metrics provided.

## Features

- [x] Metric Simulator
- [x] Metric Benchmarking


## Architecture

The project implements the `Hexagonal Architecture` 

### This project has 3 layers:

#### 1. Application 
This layer contains the core of the application, including domain models, interfaces (ports), services and use cases.

#### 2. Adapters

This contains implementations of the interfaces defined in the application core, as well as any framework-specific code.
They are concrete implementations that interact with external systems like databases, APIs, or UI components.

#### 3. Infrastructure
This contains code that supports the application but isn't part of the core business logic, such as configuration, database session management, and dependency injection setup

## Patterns

#### 1. Repository Pattern
The `MetricUseCases` class delegates fetching data to the repository through the `UnitOfWork`. The Repository pattern abstracts the data access layer, allowing for separation of database logic from the business logic.

#### 3. 12 Factor App
The project has also been structured as a 12 factor app. For more details see https://12factor.net/

#### 4. UnitOfWork
The `UnitOfWork` class encapsulates the database transaction. This pattern ensures that when a business operation (such as fetching a metric) occurs, the transaction is managed consistently (i.e., commit or rollback).

#### 5. Separation of Concerns
Separation of Concerns is well implemented. Each class has a specific responsibility:
`MetricUseCases` focuses on the business logic.
`UnitOfWork` manages transactions.
`Repository` handles database operations.

#### 6. Dependency Injection
The `MetricUseCases` class depends on the `UnitOfWork` to access the repository and manage the transaction.
The `UnitOfWork` depends on the `session` and `repository`, and both dependencies are injected via the `inject` decorator from `Flask-Injector`.
This approach allows the components (like the `session`, `repository`, or `UnitOfWork`) to be swapped with other implementations without changing the core business logic.

## SOLID Principles
Several SOLID principles are evident in this codebase:

#### Single Responsibility Principle (SRP):

Each class has a clear and singular responsibility:
`MetricUseCases` handles business logic.
`UnitOfWork` handles transaction management.
The `Repository` class handles data persistence.

#### Open/Closed Principle (OCP):

The system is open for extension but closed for modification. For instance, the     `MetricUseCases` class can be extended with new use cases without modifying existing ones. Similarly, the repository can be swapped with another implementation by changing the `configure` function without modifying the `MetricUseCases` class.

#### Liskov Substitution Principle (LSP):

The `IUseCases` interface can be substituted with any class that implements the `fetch_metric_by_name` method without affecting the behavior of the `LLMMetricsByName` view. This follows LSP as the concrete implementation `(MetricUseCases)` adheres to the contract defined by the `IUseCases` interface.

#### Dependency Inversion Principle (DIP):

The `MetricUseCases` class depends on abstractions (the `IUnitOfWork`) rather than concrete implementations (the `Repository` or `Session`). The `MetricUseCases` only knows about the interface it interacts with (`IUnitOfWork`), promoting flexibility.

## Tech stack used

-  Python 3.12
-  Flask
-  SQLAlchemy
-  Celery
-  Redis
-  Docker
-  Kubernetes
-  [Helm](https://helm.sh/)
  

## Local development [Docker Compose]
1. Create a file  `.env.dev` and paste the below

   ```sh
   FLASK_APP=app.py
   FLASK_DEBUG=1
   DATABASE_URL=postgresql://llm_user:llm_pass@db:5432/llm_db
   PORT=5000
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   JOUNCE_ENV="Local"
   RUN_SERVER=true
   ```

2. Build the image:

   ```sh
   $ docker compose build
   ```

3. Run the image:

   ```sh
   $ docker compose up -d
   ```

4. Make requests:

   ```sh
    $ curl --location 'http://127.0.0.1:5001/metrics/?metric_name=TTFT' \
    --header 'api-key: 8b864ef3319545403bf7cc15b97e522dc46624780fbd6c1e9c92270d2d97c843'
   ```

5. Visit
   1. [all metrics rankings](http://127.0.0.1:5001/visualize/all)
   2. [metrics ranking by name](http://127.0.0.1:5001/visualize)

## Local development [Manual setup]

1. Create and activate a virtual environment:

   ```sh
   $ python3 -m venv venv && source venv/bin/activate
   ```

2. Install the requirements:

   ```sh
   (venv)$ pip install -r requirements/dev.txt
   ```
3. Configure the below environment variables below in an env.sh
file:
 
   ```sh
   export FLASK_DEBUG=1
   export FLASK_ENV=development
   export DATABASE_URL=postgresql://jounce:jounce@localhost/jounce
   export GUNICORN_WORKERS=1
   export LOG_LEVEL=debug
   export SECRET_KEY=not-so-secret
   export JOUNCE_ENV="Local"

   ```

4. Source the environment variables
   ```sh
   (venv)$ source env.sh
   ```

5. Apply the database migrations
   ```sh
   (venv)$ flask db upgrade
   ```
6. Run the applicatiom
   ```sh
   (venv)$ flask run
   ```
7. Run celery worker: open a separate terminal activate the virtual environment and run
   ```sh
    celery -A src.celery worker --loglevel=INFO
   ```
8. Run celery beat: open another separate terminal activate the virtual environment and run
   ```sh
    celery -A src.celery beat --loglevel=INFO
   ```

Note: for step 7 and 8 you must install redis on your local machine 

9. Register and login: navigate to 
   ```sh
   http://localhost:5000
   ```

## Infrastructure Setup

1. Create the cluster:
    NB: see link to install [eksctl](https://eksctl.io/installation/)

   ```sh
   $ eksctl create cluster --name my-cluster --region region-code --fargate --node 1
   ```

2. Install the ingress controller:
    NB: see link to install [ingressController](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/deploy/installation/)


3. Create the app secrets:

   ```sh
   $ kubectl create secret generic app-secrets --from-literal=database-url='postgresql://dev_user:dev_pass@db_host/db_name' 
   ```

4. Apply the helm charts:
    Re-Run the CI/CD pipeline job OR 

   ```sh
   $ helm upgrade --install  app-release ./deployment/k8s-chart/
   ```

## Deployment

Image shows how the current setup has been deployed. 
![image info](./static/arch.png)

The application has been deployed to a kubernetes cluster in [EKS](https://aws.amazon.com/eks/).

The deployment has been set and scaled via CI/CD with the flexibility of [helm](https://helm.sh/) values to set default configurations, just overriding the configs that differ from one environment to the other.

The helm charts can be found under the `deployment` folder of this repo.

##### Steps
- The deployment is defined in `.gitlab-ci.yml`.
- It has 3 jobs which include `build`, `code_tests`  and `deploy_to_testing`
- The application is built from the Docker image and pushed to [aws container registry](https://aws.amazon.com/ecr/).
- see [pipelines](https://gitlab.com/joemash/jounce/-/pipelines)


## VISUALIZATION 
   1. [all metrics rankings](https://api-eks.ratiba.io/visualize/all)
   2. [metrics ranking by name](https://api-eks.ratiba.io/visualize)


## API LLM Simulation Sample Results
 1. Ranking llm metrics by metric name
   ```sh
      curl --location 'https://api-eks.ratiba.io/metrics/?metric_name=TTFT' \
      --header 'api-key: 8b864ef3319545403bf7cc15b97e522dc46624780fbd6c1e9c92270d2d97c843'
   ```

   ```sh
   {
    "results": [
        {
            "llm": "Gemini 1.5 Pro",
            "mean_value": 1.0631957234399112
        },
        {
            "llm": "amba 1.5Large",
            "mean_value": 1.0523991274852684
        },
        {
            "llm": "Gemini 1.5Flash",
            "mean_value": 1.0517713967532298
        },
        {
            "llm": "Llama 3.1 70B",
            "mean_value": 1.0512662510598165
        },
        {
            "llm": "Mixtral 8x22B",
            "mean_value": 1.0502959007503991
        },
        {
            "llm": "Claude 3.5 Sonnet",
            "mean_value": 1.050014449472202
        }
    ]
    }
   ```

 2. Ranking all llm metrics

   ```sh
      curl --location 'https://api-eks.ratiba.io/metrics/all' \
      --header 'api-key: 8b864ef3319545403bf7cc15b97e522dc46624780fbd6c1e9c92270d2d97c843'
   ```

   ```sh
   {
    "results": [
        {
            "llm": "Claude 3 Haiku",
            "mean_value": 21.240541316493342
        },
        {
            "llm": "amba 1.5Large",
            "mean_value": 21.179999311833363
        },
        {
            "llm": "Gemini 1.5Flash",
            "mean_value": 21.11147498166773
        },
        {
            "llm": "Claude 3.5 Sonnet",
            "mean_value": 21.074378225442928
        },
        {
            "llm": "Llama 3.1 8B",
            "mean_value": 21.06541125047705
        },
        {
            "llm": "Mixtral 8x22B",
            "mean_value": 21.064634584577835
        },
        {
            "llm": "GPT-4o",
            "mean_value": 21.043268859921522
        },
        {
            "llm": "Mistral Large2",
            "mean_value": 21.000221253653944
        },
        {
            "llm": "Llama 3.1 70B",
            "mean_value": 20.9609844812733
        },
        {
            "llm": "Gemini 1.5 Pro",
            "mean_value": 20.95842773666323
        },
        {
            "llm": "GPT-4o mini",
            "mean_value": 20.880586337167504
        },
        {
            "llm": "Llama 3.1 405",
            "mean_value": 20.80993432283504
        }
    ]
   }
   ```

## Others
- **Caching**: redis has been used as the cache backend.
- **Multi-stage builds**: implemented to reduce the size of the Docker image.
- **Authentication**: api key authentication.

 ## Todo
- [ ] Finalize on more testcases and enable CI.
- [ ] Add observerbility.
- [ ] Finalize on project packaging and lock dependencies.
- [ ] Automate infrastructure provisioning.

###### Crafted with ❤️ by Macharia Kariuki
