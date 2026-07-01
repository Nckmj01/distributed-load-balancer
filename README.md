# Distributed Systems Programming Project
## Group Members
| Name              | Addmission Number |
| ----------------- | ----------------- |
| Nicole Agufana    | 169786            |
| Amy Ojuka         | 162396            |
| Ray Lukorito      | 168110            |   
| Matthew Nguithi   | 162156            |

# Distributed Load Balancer

## Overview

This project implements a scalable distributed load balancer using **consistent hashing** and **Docker**. The system distributes incoming client requests across multiple server replicas while supporting dynamic addition and removal of servers with minimal redistribution of requests.

The project demonstrates concepts in distributed systems, including load balancing, replica management, fault tolerance through heartbeat monitoring, and containerized deployment.

## Features

- Consistent hashing with virtual servers
- Dynamic load balancing
- Multiple server replicas
- Heartbeat monitoring for replica health
- Dynamic server addition and removal
- Docker-based deployment
- Automated unit tests

## Project Structure
```
distributed-load-balancer/
│
├── server/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── README.md
│   └── tests/
│
├── hashing/
│   ├── consistent_hash.py
│   ├── README.md
│   └── tests/
│
├── load_balancer/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── README.md
│   └── tests/
│
├── docs/
│   ├── diagrams/
│   └── screenshots/
│
├── docker-compose.yml
├── Makefile
├── README.md
├── .gitignore
└── LICENSE
```

## Technologies Used

- Python 3
- Flask
- Docker
- Docker Compose
- Pytest
- Git & GitHub


## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/distributed-load-balancer.git
cd distributed-load-balancer
```

## Running the Project

Each component contains its own README with detailed setup instructions.

### Server

```bash
cd server
pip install -r requirements.txt
python app.py
```

### Load Balancer

```bash
cd load_balancer
pip install -r requirements.txt
python app.py
```

## Running with Docker

Build the containers:

```bash
docker compose build
```

Start the system:

```bash
docker compose up
```

Stop the system:

```bash
docker compose down
```

## Running Tests

Each module includes its own test suite.

Example:

```bash
cd server
pytest
```

Similarly:

```bash
cd hashing
pytest
```

```bash
cd load_balancer
pytest
```

## Team Responsibilities

| Member | Responsibility |
|---------|----------------|
| Nicole Agufana | Replica Server |
| Person 2 | Consistent Hashing |
| Person 3 | Load Balancer |
| Person 4 | Deployment, Testing & Documentation |


## Documentation

Additional project documentation, diagrams, screenshots, and experimental results are available in the `docs/` directory.


## License

This project is developed for educational purposes as part of a Distributed Systems programming assignment.