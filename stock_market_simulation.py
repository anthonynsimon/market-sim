import numpy as np
import matplotlib.pyplot as plt

def run(years=25, companies=4):

    # Setup vars
    verbose = False
    simulation_years = years
    end_tick = 24 * 365 * simulation_years
    display_interval = 1
    display_year_marks = True
    display_range = (0, end_tick)

    # Number of times to run simulation
    for company_index in range(0, companies):
        # Company vars
        company_value = 100.0
        initial_value = company_value
        mean = company_value
        sigma = 0.01
        inflation_interval = 24 * 365
        inflation = 0.025
        min_inflation_per_interval = 0.00
        max_inflation_per_interval = 0.05

        # Collection Setup
        value_history = []
        choice_history = [0, 0, 0]

        # Misc setup
        seed = np.random.randint(100000)
        np.random.seed(seed)
        markov_chain_samples = 100000

        # Compute Markov Chain for probability of Neutral, Positive and Negative movements
        P = np.matrix([[0.99, 0.005, 0.005],
                       [0.6, 0.3, 0.1],
                       [0.6, 0.1, 0.3]])

        v = np.matrix([[1.0, 0.0, 0.0]])

        probabilities = np.array(v * P**markov_chain_samples).flatten()

        if verbose:
            print("Using seed: {}".format(seed))
            print("Starting simulation, will run for {} ticks ({} years)".format(end_tick, end_tick / (24 * 365)))

        # Run simulation for current company
        for tick in range(end_tick):
            if verbose:
                print("Tick #{}/{}".format(tick, end_tick))
            
            # If it's time to change inflation, recalculate it based on min and max params
            if tick % inflation_interval == 0:
                inflation = min_inflation_per_interval + ((max_inflation_per_interval - min_inflation_per_interval) * np.random.rand())

            # Inflate mean progressively each run
            mean += (initial_value * inflation) / inflation_interval
            
            """
            Markov Chain Monte Carlo
            Pick one of the Markov chain states with pseudo random,
            if it's accepted then shift the mean up or down correspondingly.
            This simulates what good news and bad news for the company.
            """
            rand = np.random.random()
            choice = np.random.randint(0, len(probabilities))
            acceptance = probabilities[choice]
            if rand < acceptance:
                choice_history[choice] += 1
                mean = mean * (1.0 + np.random.random() * [0.0, sigma, sigma * -1][choice])
            
            # Calculate next company value each iteration and add to historical values
            company_value = np.random.normal(mean, mean * sigma)
            value_history.append(company_value)

            if verbose:
                print("Tick #{}/{}\t\tCompany Value: ${}".format(tick, end_tick, company_value))

        if verbose:
            print("Distribution of probabilities after {} samples".format(markov_chain_samples))
            count = sum(choice_history)
            print(["{0:.3f}".format(x / count) for x in choice_history])

        # Setup chart
        plt.style.use('ggplot')
        plt.title('Simulation for {} years at {} ticks per sample'.format(int(end_tick / (24 * 365)), display_interval))

        if display_year_marks:
            plt.xticks(range(0, end_tick + 1, 24*365), ["{}".format(x) for x in range(0, simulation_years + 1)])
        
        plt.plot(value_history[display_range[0]:display_range[1]:display_interval])

    plt.show()

run()
