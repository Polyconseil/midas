# MIDAS - MDS compliant mobility data service

[![Build Status](https://travis-ci.org/Polyconseil/midas.svg?branch=master)](https://travis-ci.org/Polyconseil/midas)

A [City of LA MDS Specification](https://github.com/CityOfLosAngeles/mobility-data-specification) (Mobility Data Specification) compliant implementation of the Agency API.


## Goals & non-goals

### Goals

* Ultimately MDS compliance
* A way to test MDS ideas on a real implementation as we believe it is hard to specify a quality API without a 
reference implementation alongside
* Developer-friendly to be able for all stakeholders to contribute

### Non-goals

* High-performance: we favor developer-friendliness over performance
* Full-featured UI: this is an API-first software and for a first iteration, the UI is not paramount
* Data-analysis: analysis should be done by other apps consuming the consumer API of this app

## Tech & requirements

* Python 3 with [Django](https://www.djangoproject.com/) and [GeoDjango](https://docs.djangoproject.com/en/2.1/ref/contrib/gis/)
* Postgresql with [PostGIS](https://postgis.net/)
* Swagger for interactive API documentation (available on /schema)

## How to run

### Backend

* Install and configure requirements (see above)
* In `midas/`, run `pip install .[dev]` to install dependencies
* You need following env variables: MIDAS_DB_NAME, MIDAS_DB_USER and MIDAS_DB_PASSWORD
* To initialize the database, run `python manage.py migrate`
* To start the backend, run `python manage.py runserver`

### Frontend

See dedicated README in [front/README.md](front/README.md)

![Test](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEYAAAAUCAAAAAAVAxSkAAABrUlEQVQ4y+3TPUvDQBgH8OdDOGa+oUMgk2MpdHIIgpSUiqC0OKirgxYX8QVFRQRpBRF8KShqLbgIYkUEteCgFVuqUEVxEIkvJFhae3m8S2KbSkcFBw9yHP88+eXucgH8kQZ/jSm4VDaIy9RKCpKac9NKgU4uEJNwhHhK3qvPBVO8rxRWmFXPF+NSM1KVMbwriAMwhDgVcrxeMZm85GR0PhvGJAAmyozJsbsxgNEir4iEjIK0SYqGd8sOR3rJAGN2BCEkOxhxMhpd8Mk0CXtZacxi1hr20mI/rzgnxayoidevcGuHXTC/q6QuYSMt1jC+gBIiMg12v2vb5NlklChiWnhmFZpwvxDGzuUzV8kOg+N8UUvNBp64vy9q3UN7gDXhwWLY2nMC3zRDibfsY7wjEkY79CdMZhrxSqqzxf4ZRPXwzWJirMicDa5KwiPeARygHXKNMQHEy3rMopDR20XNZGbJzUtrwDC/KshlLDWyqdmhxZzCsdYmf2fWZPoxCEDyfIvdtNQH0PRkH6Q51g8rFO3Qzxh2LbItcDCOpmuOsV7ntNaERe3v/lP/zO8yn4N+yNPrekmPAAAAAElFTkSuQmCC)


## TODO

- [ ] API: Testing a more restful approach
  - [ ] Add trips
  - [ ] Add multiple mobility modes
- [ ] Authentication
- [ ] Clarify if service_areas should be integrated in this app or in another one that would focus on zoning
- [ ] ...
