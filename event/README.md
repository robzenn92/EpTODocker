# Event

An Event is an object that can be generated at any point in time by every [EpTO](https://github.com/robzenn92/EpTODocker/tree/master/epto_project) application. Events can only be contained into [Balls](https://github.com/robzenn92/EpTODocker/tree/master/ball) that can be broadcasted to other [EpTO](https://github.com/robzenn92/EpTODocker/tree/master/epto_project) applications via [Messages](https://github.com/robzenn92/EpTODocker/tree/master/messages). An Event consists of the following fields:

- `event_id`: an unique [uuid](https://docs.python.org/3.6/library/uuid.html)
- `source_id`: the id of the source who generated the event (we use the source's IP)
- `ttl`: a time-to-live
- `ts`: a simple timestamp that is the point in time in which the event is generated

An Event can be serialized into json thanks to the `to_json` method while the `increase_ttl` method allows to increase its `ttl` by one.