import csv
import matplotlib.pyplot as plot
import os.path

from numpy import polyfit, arange

CSV_FILE_NAME = "data.csv"

current_directory = os.path.dirname(os.path.realpath(__file__))


def main():
    """The main function that is called when the program is run"""

    trials = parse_data_from_csv()

    for trial in trials:
        trial.graph_scatter_plot()

    show_graph(trials, file_path=f"{current_directory}\\scatter_plot.png")

    for trial in trials:
        trial.find_quadratic()
        trial.graph_quadratic()
        trial.find_acceleration()
        print(f"For mass of {trial.car_weight} pno, acceleration is: {trial.acceleration}")

    show_graph(trials, file_path=f"{current_directory}\\scatter_plot_with_line_of_best_fit.png")


class Trial:
    """Represents a trial run for the experiment"""

    def __init__(self, car_weight=None):
        self.car_weight = car_weight
        self.equation = None
        self.acceleration = None
        self.times = []
        self.displacements = []

    def get_max_time(self):
        return self.times[-1]

    def get_max_displacement(self):
        return self.displacements[-1]

    def graph_scatter_plot(self):
        """Creates a graph of just the individual position-time points"""

        # For each trial plot the points
        plot.scatter(
            self.times,
            self.displacements,
            marker=".",
            label=f"{self.car_weight} pno"
        )

    def find_quadratic(self):
        """Generates the quadratic equations for each trial"""
        self.equation = polyfit(self.times, self.displacements, deg=2)

    def graph_quadratic(self):
        """Graphs the quadratic equations with with opaque data points"""

        plot.scatter(self.times, self.displacements, marker=".", alpha=0.3)

        equation_times = arange(0, 10, 0.01)
        equation = self.equation
        equation_displacements = equation[0] * equation_times ** 2 + equation[1] * equation_times + equation[2]

        plot.plot(equation_times, equation_displacements, label=f"{self.car_weight} pno")

    def find_acceleration(self):
        """Calculates the accelerations"""

        self.acceleration = 2 * self.equation[0]


def parse_data_from_csv():
    """Takes a csv file and returns a list of trial objects"""

    trials = []
    times = []

    with open(current_directory + "\\" + CSV_FILE_NAME) as csv_file:
        file_reader = csv.reader(csv_file, delimiter=",")  # Create an object to read the csv_file

        # Loop through each row and measurement
        for row_index, row in enumerate(file_reader):
            for column_index, measurement in enumerate(row):

                # If it's the first column it's the displacement column
                if column_index == 0:
                    if measurement != "":
                        times.append(float(measurement))

                # If it's the first row create a trial object and add it to the list
                elif row_index == 0:
                    trials.append(Trial(car_weight=float(measurement)))

                # All other rows are time measurements to add to the trial
                elif measurement != "":
                    trials[column_index - 1].displacements.append(float(measurement))

    # Set the displacement for each trial
    for trial in trials:
        trial.times = times[:len(trial.displacements)]

    return trials


def show_graph(trials, file_path=None):
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
    plot.legend(title="Car's mass")

    if file_path is not None:
        plot.savefig(file_path, dpi=600)

    plot.show()


if __name__ == '__main__':
    main()
