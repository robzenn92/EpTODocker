# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Introduced Elasticsearch, Fluentd, Kibana to collect and analyze container logs. [#4](https://github.com/robzenn92/EpTODocker/issues/4).

### Fixed
- All classes inherit from the Object class. [#6](https://github.com/robzenn92/EpTODocker/issues/6).
- Cyclon's exchange_view()` should not return a PartialView containing the source's IP.  [#3](https://github.com/robzenn92/EpTODocker/issues/3).
- PartialView's `merge()` should not allow self.ip in peer_list. [#2](https://github.com/robzenn92/EpTODocker/issues/2).

### Changed
- Cyclon's `get_k_view()` returns a list of IPs rather than a list of PodDescriptor. [#7](https://github.com/robzenn92/EpTODocker/issues/7).