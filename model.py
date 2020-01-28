import argparse
import json

from agent import Agent
from graph import AgreeablenessGraph, IncomeGraph
from position import Position
from zone import Zone


def main():
    # Load agents
    for agent_properties in json.load(open("agents-100k.json")):
        longitude = agent_properties.pop('longitude')
        latitude = agent_properties.pop('latitude')
        # store agent position in radians
        position = Position(longitude, latitude)

        zone = Zone.find_zone_that_contains(position)
        agent = Agent(position, **agent_properties)
        zone.add_inhabitant(agent)

    agreeableness_graph = AgreeablenessGraph()
    agreeableness_graph.show(Zone.ZONES)

    income_graph = IncomeGraph()
    income_graph.show(Zone.ZONES)


if __name__ == '__main__':
    main()
