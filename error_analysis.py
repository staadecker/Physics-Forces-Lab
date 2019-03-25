import csv

from numpy import polyfit, arange
import matplotlib.pyplot as plot

CSV_FILE_NAME = "Forces lab - Rolling Car - CSV DATA.csv"

GRAVITATIONAL_ACCELERATION = 9.81


def main():
    """The main function that is run first"""
    trials = parse_data_from_csv()

    graph_scatter_plots(trials)

    find_quadratics(trials)

    graph_quadratics(trials)

    find_accelerations(trials)

    calculate_errors(trials)

    for trial in trials:
        print(f"{trial.error * 100 :5.2f}%")


class Trial:
    """Represents a trial run for the experiment"""

    def __init__(self, cart_weight=None, hanging_weight=None):
        self.cart_weight = cart_weight
        self.hanging_weight = hanging_weight
        self.equation = None
        self.acceleration = None
        self.displacements = []
        self.times = []
        self.error = None

    def get_max_time(self):
        return self.times[-1]

    def get_max_displacement(self):
        return self.displacements[-1]

    def get_expected_acceleration(self):
        return self.hanging_weight / (self.hanging_weight + self.cart_weight) * GRAVITATIONAL_ACCELERATION


def parse_data_from_csv():
    """Takes a csv file and returns a list of trial objects"""

    trials = []
    displacements = []

    with open(CSV_FILE_NAME) as csv_file:
        file_reader = csv.reader(csv_file, delimiter=",")  # Create an object to read the csv_file

        # Loop through each row and measurement
        for row_index, row in enumerate(file_reader):
            for column_index, measurement in enumerate(row):

                # If it's the first column it's the displacement column
                if column_index == 0:
                    if measurement != "":
                        displacements.append(float(measurement))

                # If it's the first row create a trial object and add it to the list
                elif row_index == 0:
                    trials.append(Trial(cart_weight=float(measurement)))

                # If it's the second row the measurement represents the trial's hanging weight
                elif row_index == 1:
                    trials[column_index - 1].hanging_weight = float(measurement)

                # All other rows are time measurements to add to the trial
                elif measurement != "":
                    trials[column_index - 1].times.append(float(measurement))

    # Set the displacement for each trial
    for trial in trials:
        trial.displacements = displacements[:len(trial.times)]

    return trials


def prepare_graph(trials):
    max_displacement = 0
    max_time = 0

    for trial in trials:
        max_displacement = max(max_displacement, trial.get_max_displacement())
        max_time = max(max_time, trial.get_max_time())

    plot.ylim(0, max_displacement)
    plot.xlim(0, max_time)
    plot.ylabel("Displacement (m)")
    plot.xlabel("Time (s)")
    plot.title("Position - Time Graph")
    plot.legend(title="(Hanging Mass, Cart Mass)\n(in edhruvs)")


def graph_scatter_plots(trials):
    """Creates a graph of just the individual position-time points"""

    # For each trial plot the points
    for trial in trials:
        plot.scatter(
            trial.times,
            trial.displacements,
            marker=".",
            label=f"({trial.hanging_weight}, {trial.cart_weight})"
        )

    prepare_graph(trials)
    plot.savefig("position_time_graph_scatter.png", dpi=600)
    plot.show()


def find_quadratics(trials):
    """Generates the quadratic equations for each trial"""
    for trial in trials:
        trial.equation = polyfit(trial.times, trial.displacements, deg=2)


def graph_quadratics(trials):
    """Graphs the quadratic equations with with opaque data points"""

    for trial in trials:
        plot.scatter(trial.times, trial.displacements, marker=".", alpha=0.3)

        equation_times = arange(0, 5, 0.01)
        equation_displacements = trial.equation[0] * equation_times ** 2 + trial.equation[1] * equation_times + trial.equation[2]

        plot.plot(equation_times, equation_displacements, label=f"({trial.hanging_weight}, {trial.cart_weight})")

    prepare_graph(trials)
    plot.savefig("position_time_graph_quadratics.png", dpi=600)
    plot.show()


def find_accelerations(trials):
    """Calculates the accelerations"""

    for trial in trials:
        trial.acceleration = 2 * trial.equation[0]
        print(trial.acceleration)


def calculate_errors(trials):
    """Calculates the errors for each trial"""

    for trial in trials:
        expected = trial.get_expected_acceleration()
        trial.error = abs((expected - trial.acceleration) / expected)


if __name__ == '__main__':
    main()
