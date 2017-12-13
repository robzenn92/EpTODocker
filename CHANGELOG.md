# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Added
- Minikube checks before executing some bash scripts. [#10](https://github.com/robzenn92/EpTODocker/issues/10)
- `MY_POD_UID` exposed as EpTO's env variable in `deployment.yml`. [#9](https://github.com/robzenn92/EpTODocker/issues/9)

### Changed
- Cyclon and EpTO have been migrated from Python 2.7 with Flask 0.12 to Python 3.6 with Django 2.0. [#1](https://github.com/robzenn92/EpTODocker/issues/1)

## [v0.1.0](https://github.com/robzenn92/EpTODocker/releases/tag/v0.1.0)

### Added
- Introduced Elasticsearch, Fluentd, Kibana to collect and analyze container logs. [#4](https://github.com/robzenn92/EpTODocker/issues/4).

### Fixed
- All classes inherit from the Object class. [#6](https://github.com/robzenn92/EpTODocker/issues/6).
- Cyclon's exchange_view()` should not return a PartialView containing the source's IP.  [#3](https://github.com/robzenn92/EpTODocker/issues/3).
- PartialView's `merge()` should not allow self.ip in peer_list. [#2](https://github.com/robzenn92/EpTODocker/issues/2).

### Changed
- Cyclon's `get_k_view()` returns a list of IPs rather than a list of PodDescriptor. [#7](https://github.com/robzenn92/EpTODocker/issues/7).