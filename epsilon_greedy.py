import numpy as np

class EpsilonGreedy(object):
    """
    A very simple machine learning algorithm to solve the Multi-Armed Bandit problem.
    80% of the time go for the lever with the biggest chance of reward.
    The remaining 20% pick a random option as an 'exploration' of alternatives.
    """

    def __init__(self, number_of_options):
        self.number_of_options = number_of_options
        # Init everything with 100% chance of being shown
        self.times_clicked = [1 for x in range(number_of_options)]
        self.times_shown = [1 for x in range(number_of_options)]

    def choose(self, option, clicked):
        if clicked:
            self.times_clicked[option] += 1

    def show(self):
        # Initialize best option as first element
        best_index = 0
        best_rate = self.times_clicked[best_index] / self.times_shown[best_index]
        # 20% of the time, explore random options
        if np.random.random() < 0.2:
            best_index = np.random.randint(self.number_of_options)
        else:
            # The other 80% calculate the best choice based on clicks per times shown
            for candidate_index in range(self.number_of_options):
                candidate_rate = self.times_clicked[candidate_index] / self.times_shown[candidate_index]
                if candidate_rate > best_rate:
                    best_index = candidate_index
                    best_rate = candidate_rate
        self.times_shown[best_index] += 1
        return best_index

    def display_stats(self):
        for i in range(self.number_of_options):
            option = self.times_clicked[i] / self.times_shown[i]
            print("{0}\t\t{1}/{2}\t\t{3:0.4f}".format(i, self.times_clicked[i], self.times_shown[i], option))


eg = EpsilonGreedy(10)

while True:
    option = eg.show()
    selection = input("Click option '{}'? (y/n):\n".format(option))
    eg.choose(option, selection == 'y')
    eg.display_stats()
