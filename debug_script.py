#!/usr/bin/python3
from models import storage
from models.state import State

print("Before query execution")
states = storage.all(State)
print("After query execution")

for state in states.values():
    print(state)
