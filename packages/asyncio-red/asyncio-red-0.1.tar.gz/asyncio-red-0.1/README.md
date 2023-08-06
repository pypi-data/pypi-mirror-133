asyncio-RED (Redis Event Driven)
================================

Powers your microservices with event driven approach built on top of redis.
Support publishing and subscribing via lists, channels and redis streams.

Installation
------------

- `pip install asyncio-red`

Event schema registry
---------------------

There is a possibility to keep a single event schemas registry on the S3 and share 
the definitions across different services. You'll need an AWS account and keys with S3 access.

- Go to app root dir and initialize asyncio-red:

```shell
asyncio_red init --app-name=<app name> --s3-bucket=<bucket name>
```

This will create an initial structure.
Define your events at `red/registry/<app name>.py`:

```python
from pydantic import Field
from asyncio_red.events import BaseEvent


class EventViaList(BaseEvent):
    key_0: str = Field(...)
    key_1: str


class EventViaChannel(BaseEvent):
    key_0: str = Field(...)
    key_1: str


class EventViaStream(BaseEvent):
    key_0: str = Field(...)
    key_1: str
```

- push this schema to a registry: `asyncio-red push`
- In a different service - do the same steps, e.g. init structure and run `asyncio-red pull`

Setup producer
--------------


```python
from aioredis import Redis
from asyncio_red import RED, Via
from examples.service_1.red.registry.service_1 import EventViaList, EventViaChannel, EventViaStream


redis_client = Redis()
red = RED(app_name=str('test_app_1'), redis_client=redis_client)

# define how this particular event will be dispatched, e.g. using the redis list or
# via the redis channels or streams
red.add_out(
    EventViaList,
    via=Via.LIST,
    target_name=str("list_events")
)


red.add_out(
    EventViaChannel,
    via=Via.CHANNELS,
    target_name="channel_events"
)

red.add_out(
    EventViaStream,
    via=Via.STREAMS,
    target_name="stream_events"
)


async def your_awesome_function():
    ...  # do work
    # dispatch event in the code according to a router setup
    await EventViaList(key_0=0, key_1=1).dispatch()  # this one will be put to a list
    await EventViaChannel(key_0=0, key_1=1).dispatch()  # this one will be pushed to a channel
    await EventViaStream(key_0=0, key_1=1).dispatch()  # this one will be pushed to a stream

```


Setup consumer
--------------

Assuming that you've already pulled the events from service_0

```python
from aioredis import Redis
from asyncio_red import RED, Via
from examples.service_2.red.registry.service_1 import EventViaList, EventViaChannel, EventViaStream


redis_client = Redis()
red = RED(app_name=str('service_2'), redis_client=redis_client)


async def event_handler(event):
    print(event)


red.add_in(
    EventViaList,
    via=Via.LIST,
    handler=event_handler,
    list_name="list_events",
)

red.add_in(
    EventViaChannel,
    via=Via.LIST,
    handler=event_handler,
    error_handler=event_handler,
    channel_name="channel_events"
)

red.add_in(
    EventViaStream,
    via=Via.STREAMS,
    handler=event_handler,
    stream_name="stream_events",
    group_name="group_events",
    consumer_name="consumer_name"
)

await red.run()
```
