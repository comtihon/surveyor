# Surveyor [![Build Status](https://travis-ci.org/comtihon/surveyor.svg?branch=master)](https://travis-ci.org/comtihon/surveyor)
Service that allows survey creation, questions answering and statistics calculation.  
## Architecture
Surveyor service contains 4 microservices and 3 third-party services:
1. [Manager](https://github.com/comtihon/survey_manager) - is responsible for creating/editing surveys, questions and 
answers configuration. Writes surveys to `PostgreSQL`.
2. [Requests](https://github.com/comtihon/survey_requests) service - is responsible for gathering survey's answers from
users. Reads surveys configuration from the same `PostgreSQL` as `Manager`. Writes all answers to `Kafka`.
3. [Collector](https://github.com/comtihon/survey_collector) service. Reads answers from `Kafka` and aggregates statistics
to `MongoDB`.
4. [Statistics](https://github.com/comtihon/survey_statistics) service. Returns answers statistics for question. Reads
the same `MongoDB` as `Collector`.
5. [PostgreSQL](https://www.postgresql.org) for storing surveys, questions and answers configuration created with 
`Manager`.
6. [Kafka](https://kafka.apache.org/) for streaming answers data.
7. [MongoDB](https://www.mongodb.com/) for online statistics. It doesn't store full statistics, instead is increments 
counters for every answer in question. Dynamic documents are used.

```
    Survey/Question/Answer CRUD --> Manager -->  Postgres
    & Step-by-step attach                           ||
                                                    || Surveys, Questions, Answers configuration
                                                    ||
                                                    \/
                            Answered Survey --->  Requests  ---------> Kafka --------> Collector --------> MongoDB
                                                             answers          answers            aggregated   ||
                                                                                                 statistics   || statistics
                                                                                                              ||
                                                                                                              \/
                                                        Get statistics request (question) -------->       Statistics
```
## Waiting for a highload
1. index `question_id` in `MongoDB`
2. switch to [avro](https://avro.apache.org/) or [msgpack](http://msgpack.org/index.html) in `Kafka`
3. `Requests` read from `PostgreSQL` slave
4. add caching Surveys configuration from `Postgres` for `Requests`
5. `Statistics` read from `MongoDB` slave
6. `Kafka` and `Requests` to autoscale groups
7. Put answers in different topics (by Survey's country code) and start more `Collector`

## Limitations
1. old questions are not deleted.
In current version statistics with old (deleted) questions is also fetched from statistics backend. 
It is frontend's job to filter deleted questions. It can be done with information, fetched from manager backend.  
In future we can make sending notifications with schema changes to collector.
2. statistics in database is not full (only counters).
It was made to allow real time (live on frontend) statistics showing. It would be impossible if we saved all statistics 
to sql database and query it with joins. If we will need whole statistics in future - we can easily add kafka to 
postgres stream.

## Run

    make run
Will clone and build Docker images of services (if not built) and start all services via docker-compose.   
__Important__: Avoid port conflicts with your running services.  
See `docker-compose.yml` for details.  
__Requirements__:  
* [docker](https://www.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)

## Integration testing
Run integrations tests for surveyor microservises.
### Full test
1. create survey in `manager`
2. check created survey in `postgres`
3. get survey from `manager`
4. compare surveys
5. send answers to `requests`
6. check `kafka` for answers
7. check answer statistics in `mongodb` (sometimes test is too fast and fails here. Just re-run)
8. check answer statistics via `statistics`
### Travis test
Same as full test but without kafka step, as there are some problems with docker, kafka, TravisCI and python-kafka.
### Run

    make test_build && make test_install && survey_tester
or simple:

    make test
__Important__: Services should be accessible for tests. Running `make run && make test` will do all the job.   
__Requirements__:
* [python3.6](https://www.python.org/downloads/release/python-360/). Service is not compatible with python2.7. 
Compatibility with 3.0-3.5 versions was not tested.
* [pip](https://pypi.python.org/pypi/pip). If your os provide `pip3` instead - you should modify Makefile to use pip3.
* [wheel](https://pypi.python.org/pypi/wheel)
All other dependencies should be resolved automatically by wheel. 
If not - see them in `setup.py` `install_requires` section and use `sudo pip install <require>`.

__Configuration__:
System configuration is available in `tester/resources/services.yml`

### Adding your test
Add your test in two steps:
 * create module in `tester.test` package implementing `Test` module or any of its children.
 * and... that's all. Now second step  

System configuration is passed to your `init` method as dict.
