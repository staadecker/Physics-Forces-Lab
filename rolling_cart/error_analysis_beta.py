from rolling_cart.analyser import *

from numpy import random

INACCURACY = 0.1

GRAVITATIONAL_ACCELERATION = 9.81

SAMPLES = 1000


def main():
    """The main function that is run first"""
    trials = parse_data_from_csv()

    for trial in trials:
        trial.find_quadratic()
        trial.find_acceleration()

        plot.axvline(trial.acceleration, linewidth=2, color="red")
        plot.axvline(get_expected_acceleration(trial), linewidth=2, color="pink")

        accelerations = []

        for i in range(SAMPLES):
            modified_trial = generate_modified_trial(trial)
            modified_trial.find_quadratic()
            modified_trial.find_acceleration()
            accelerations.append(modified_trial.acceleration)

        plot.hist(accelerations, bins=100)
        plot.title(f"{trial.hanging_weight} to {trial.cart_weight}")

        plot.show()


def generate_modified_trial(trial):
    new_trial = Trial(cart_weight=trial.cart_weight, hanging_weight=trial.hanging_weight)

    for time in trial.times:
        new_trial.times.append(time + random.normal(loc=0, scale=INACCURACY))

    new_trial.displacements = trial.displacements

    return new_trial


def get_expected_acceleration(trial):
    return trial.hanging_weight / (trial.hanging_weight + trial.cart_weight) * GRAVITATIONAL_ACCELERATION


if __name__ == '__main__':
    main()
