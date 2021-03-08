import pandas as pd
from matplotlib import pyplot as plt
from tabulate import tabulate
import numpy as np

#TODO Create a pprint function

class Player:
    '''
    Establishes a player class, defined by a players name and the season.
    '''
    def __init__(self, name, season):
        '''
        :param name: str, Player's full name in proper(title) case, seperated by a space. Example: "Tom Brady"
        :param season: int, Year of the season of interest
        :param data: dataframe, Weekly performance of specified player for designated season
        '''
        self.name=name.strip()
        self.season=season

        try:
            data=pd.read_csv("./data/Player Data {}.csv".format(self.season), index_col=0)
        except:
            raise Exception('No data available for {} season.'\
                            'Update data cache via data_caching.py'.format(self.season))

        self.data=data[data["Player"]==self.name]

        if self.data.empty:
            raise Exception('No player listed with name "{}". Please ensure this name is spelt correctly'\
                            'and is in your league.'.format(self.name))

    def pprint(self):
        '''
        Prints a formatted table within the terminal, displays all columns and rows
        :return: None
        '''
        print('\n {} Fantasy Performance for {}'\
              '=================================='\
              '=================================='.format(self.name, self.season))
        print(tabulate(self.data, headers="keys", tablefmt="simple"), end='\n'*2)

    def plot_weekly_performance(self):
        '''
        Used to generate a line graph of actual and estimated player performance for a specific player and season
        :return: None, presents pyplot graph
        '''

        weeks=self.data["Week"]
        actuals=self.data["Actual"]
        projected=self.data["Proj"]

        plt.plot(weeks, actuals, color="green", marker='o', linestyle='solid', label="Actual")
        plt.plot(weeks, projected, color="blue", marker='o', linestyle='solid', label="Projected")

        plt.xlabel("Week")
        plt.ylabel("Points")
        plt.legend()
        plt.title("{} {}".format(self.name, self.season))
        plt.show()


class Position:
    def __init__(self, position, season):
        '''
        :param position: str; two letter abbreviation for player position. Please note this is the position at which
            they were placed in their respective fantasy team. E.G. If a RB is placed in the flex on a particular week,
            they will be listed as flex for that week.
        :param season:
        '''
        self.position=position
        self.season=season
        try:
            data = pd.read_csv("./data/Player Data {}.csv".format(self.season), index_col=0)
        except:
            raise Exception('No data available for {} season.'\
                            'Update data cache via data_caching.py'.format(self.season))

        self.data = data[data["Pos"] == self.position]

        if self.data.empty:
            raise Exception('No data listed for position "{}".'\
                            'Please reference position codes in the doc string.'.format(self.position))

    def top(self, week, n=5):
        '''
        Returns a dataframe of the top players in the specified position for a given week, by actuals.
        :param week: Int, the week of interest
        :param n: Int, how many rows you would like returned
        :return: Dataframe of top players for that week
        '''
        assert type(week)==int
        assert type(n)==int

        week_data = self.data[self.data["Week"]==week]

        return week_data.sort_values("Actual", ascending=False)

    def pprint_top(self, week, n=5):
        '''
        Prints a complete, formatted table of the top players in the specified position for a given week, by actuals.
        :param week: Int, the week of interest
        :param n: Int, how many rows you would like returned
        :return: None, prints table
        '''
        assert type(week)==int
        assert type(n)==int

        week_data = self.data[self.data["Week"]==week]

        week_data=week_data.sort_values("Actual", ascending=False)

        print('\n {} Fantasy Performance for Week {} {}' \
              '==================================' \
              '=================================='.format(self.position, week, self.season))
        print(tabulate(week_data.head(n), headers="keys", tablefmt="simple"), end='\n' * 2)

    def plot_weekly_distribution(self):
        '''
        Creates a boxchart of position performance by week for a given season
        :return: None, generate box chart
        '''
        weekly_data=[]

        for n in range(1,17):
            weekly_data.append(self.data[self.data["Week"]==n]["Actual"])

        plt.axis([0, 17, -1, 60])
        plt.xticks([_ for _ in range(1,17)])
        plt.boxplot(weekly_data)
        plt.xlabel("Week")
        plt.ylabel("Actuals")
        plt.title("{} Performance for {}".format(self.position, self.season))

        plt.show()

    def summarize(self):
        '''
        Generates a summary of central tendencies of all player's performance for a specified position
        :return: Dataframe object containing mean, median, 25th percentile, 75th percentile, etc.
        '''
        summary=self.data.groupby(["Player","Professional Team"]).agg(
            min_actual=('Actual','min'),
            p25_actual=('Actual',lambda x: np.percentile(x, q=25)),
            median_actual=('Actual', lambda x: np.percentile(x, q=50)),
            mean_actual=('Actual', 'mean'),
            p75_actual=('Actual', lambda x: np.percentile(x, q=75)),
            max_actual=('Actual','max'),
            std_actual=('Actual', lambda x: np.std(x)),
            mean_proj=('Proj','mean'),
            median_proj=('Proj','median'),
            weeks_played=('Week', 'count')
        ).sort_values('mean_actual', ascending=False)

        return summary

    def pprint_summarize(self):
        summary=self.data.groupby(["Player","Professional Team"]).agg(
            min_actual=('Actual','min'),
            p25_actual=('Actual',lambda x: np.percentile(x, q=25)),
            median_actual=('Actual', lambda x: np.percentile(x, q=50)),
            mean_actual=('Actual', 'mean'),
            p75_actual=('Actual', lambda x: np.percentile(x, q=75)),
            max_actual=('Actual','max'),
            std_actual=('Actual', lambda x: np.std(x)),
            mean_proj=('Proj','mean'),
            median_proj=('Proj','median'),
            weeks_played=('Week', 'count')
        ).sort_values('mean_actual', ascending=False)

        print('\n Top {} Fantasy Performance for {}' \
              '==================================' \
              '=================================='\
              '===================================='\
              '======================================'.format(self.position, self.season))

        print(tabulate(summary, headers="keys", tablefmt="simple"), end='\n' * 2)

#TODO Create Players Class for comparison

Player(name="Drew Lock", season=2020).pprint()
#Player(name="Patrick Mahomes", season=2020).plot_weekly_performance()

#pos=Position(position="WR", season=2020)
#pos.pprint_summarize()

# print(type(pos.data))
# pos.plot_weekly_distribution()


