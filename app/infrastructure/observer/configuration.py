from app.infrastructure.observer.event import Event
from app.infrastructure.observer.listener import Listener

event = Event()

listener = Listener()
event.subscribe(listener)
