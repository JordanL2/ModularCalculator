#!/usr/bin/python3


def defaultState(state, defaults):
	for k, v in defaults.items():
		if k not in state:
			state[k] = v
