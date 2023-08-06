# Copyright (c) 2021-2022, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import annotations

import asyncio
import logging
import traceback
import typing as t
from collections import defaultdict
from collections.abc import Awaitable
from dataclasses import dataclass

from chatto.errors import NoEventQueue
from chatto.message import Message
from chatto.secrets import Secrets
from chatto.stream import Stream

log = logging.getLogger(__name__)


@dataclass(eq=True, frozen=True)
class Event:
    def __str__(self) -> str:
        return self.__class__.__name__


@dataclass(eq=True, frozen=True)
class ReadyEvent(Event):
    ...


@dataclass(eq=True, frozen=True)
class MessageCreatedEvent(Event):
    message: Message


@dataclass(eq=True, frozen=True)
class StreamFetchedEvent(Event):
    stream: Stream


@dataclass(eq=True, frozen=True)
class ChatPolledEvent(Event):
    data: dict[str, t.Any]


@dataclass(eq=True, frozen=True)
class MessageSentEvent(Event):
    message: Message


@dataclass(eq=True, frozen=True)
class AuthorisedEvent(Event):
    secrets: Secrets
    oauth_tokens: dict[str, t.Any]


if t.TYPE_CHECKING:
    CallbacksT = dict[t.Type[Event], list[t.Callable[[Event], Awaitable[t.Any]]]]
    ListenerT = t.Callable[[t.Callable[[t.Any], t.Any]], None]


class EventHandler:
    __slots__ = ("_queue", "callbacks")

    def __init__(self) -> None:
        self.callbacks: CallbacksT = defaultdict(list)

    @property
    def queue(self) -> asyncio.Queue[Event] | None:
        return getattr(self, "_queue", None)

    @property
    def queue_size(self) -> int:
        if not self.queue:
            return 0

        return self._queue.qsize()

    async def create_queue(self) -> None:
        if self.queue:
            log.warning("The event handler already has an event queue")
        self._queue: asyncio.Queue[Event] = asyncio.Queue()

    async def process(self) -> None:
        if not self.queue:
            raise NoEventQueue("there is no event queue")

        while True:
            try:
                event = await self._queue.get()
                log.debug(f"Retrieved {event} event")
                for cb in self.callbacks[event.__class__]:
                    log.debug(f"Running callback '{cb.__name__}' for event...")
                    await cb(event)

            except Exception:
                log.error(f"Ignoring error processing {event} event:")
                traceback.print_exc()

    async def dispatch(self, event_type: t.Type[Event], *args: t.Any) -> Event:
        if not self.queue:
            raise NoEventQueue("there is no event queue")

        event = event_type(*args)
        await self._queue.put(event)
        log.debug(f"Dispatched {event_type.__name__} event")
        return event

    def subscribe(
        self, event_type: t.Type[Event], *callbacks: t.Callable[[t.Any], t.Any]
    ) -> None:
        for cb in callbacks:
            self.callbacks[event_type].append(cb)
            log.info(
                f"Subscribed to {event_type.__name__} events "
                f"with callback '{cb.__name__}'"
            )

    def listen(self, event_type: type[Event]) -> ListenerT:
        return lambda callback: self.subscribe(event_type, callback)
