# Ball

Ball is a simple class that extends Pythons's standard [set](https://docs.python.org/3.6/library/stdtypes.html#set). It is used in order to collect [events](https://github.com/robzenn92/EpTODocker/tree/master/event) and it can be serialized in json thanks to the `to_json` method so that it can be broadcasted. Moreover, it provides the method `increase_events_ttl` that allows a fast way to increase the `ttl` of each [events](https://github.com/robzenn92/EpTODocker/tree/master/event) contained in the set.
