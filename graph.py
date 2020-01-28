import matplotlib.pyplot as plt
from collections import defaultdict


class BaseGraph:

    def __init__(self):
        self.title = "Your graph title"
        self.x_label = "X-axis label"
        self.y_label = "X-axis label"
        self.show_grid = True

    def show(self, zones):
        x_values, y_values = self.xy_values(zones)
        plt.plot(x_values, y_values, '.')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.show_grid)
        plt.show()

    def xy_values(self, zones):
        raise NotImplementedError


class AgreeablenessGraph(BaseGraph):

    def __init__(self):
        super().__init__()
        self.title = "Nice people live in the countryside"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.population_density() for zone in zones]
        y_values = [zone.average_agreeableness() for zone in zones]
        return x_values, y_values


class IncomeGraph(BaseGraph):
    # Inheritance, yay!

    def __init__(self):
        # Call base constructor
        super(IncomeGraph, self).__init__()

        self.title = "Older people have more money"
        self.x_label = "age"
        self.y_label = "income"

    def xy_values(self, zones):
        income_by_age = defaultdict(float)
        population_by_age = defaultdict(int)
        for zone in zones:
            for inhabitant in zone.inhabitants:
                income_by_age[inhabitant.age] += inhabitant.income
                population_by_age[inhabitant.age] += 1

        x_values = range(0, 100)
        # list comprehension (listcomps)
        y_values = [income_by_age[age] / (population_by_age[age] or 1) for age in range(0, 100)]
        return x_values, y_values
