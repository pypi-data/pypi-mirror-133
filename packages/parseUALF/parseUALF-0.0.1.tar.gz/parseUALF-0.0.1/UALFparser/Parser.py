import pandas as pd
import numpy as np
import plotly.express as px
import datetime


class parser():
    '''
    The purpose of the ualf_dataframe_parser is to parse a python requests response recieved in the
    universal ascii lightning format (ualf).

    A visual representation of the format can be found at the following link from the Norwegian
    Metrological Institute (MET Norway):

        -> https://frost.met.no/dataclarifications.html#ualf

    The class recieves a request response from the python requests package and parses the content response
    to a pandas dataframe object. Ensure that the requests package is correctly installed on you
    environment:

            -> https://docs.python-requests.org/
    '''

    def __init__(self, response):

        '''
        Creating class instance with attributes:

            self.response; request respons needed to instigate class object
            self.error; call raise_for_status method for the input response, erroneus response code
                        will cause 404 error to be raised.
        '''

        self.response = response
        self.error = response.raise_for_status()

    def parse_text_to_numpy(self):

        '''
        Method returns parsed numpy array of the request response text content
        '''

        try:
            return np.array([[float(x) if '.' in x else int(x) for x in [x.replace(' ', ',')][0].split(',')] \
                             for x in str(self.response.content)[2:-3].split('\\n')])
        except ValueError:
            print('Response could not be parsed to a numpy array. \nReview input data')

    def dataframe(self):

        '''
        Returns a pandas dataframe object from the parsed numpy array created with the
        parse_text_to_numpy method.
        '''

        columns = ['Version', 'Year', 'Month', 'Day of Month', 'Hour', 'Minute', 'Seconds',
                   'Nanoseconds', 'Latitude', 'Longitude', 'Peak Current', 'Multiplicity',
                   'Number of Sensors', 'Degrees of Freedom', 'Ellipse Angle', 'Semi-major Axis',
                   'Semi-minor Axis', 'Chi-square Value', 'Rise Time', 'Peak-to-zero Time',
                   'Max Rate-of-Rise', 'Cloud Indicator', 'Angle Indicator', 'Signal Indicator',
                   'Timing Indicator']

        int_columns = ['Version', 'Year', 'Month', 'Day of Month', 'Hour', 'Minute', 'Seconds',
                       'Nanoseconds', 'Peak Current', 'Multiplicity', 'Number of Sensors',
                       'Degrees of Freedom', 'Cloud Indicator', 'Angle Indicator', 'Signal Indicator',
                       'Timing Indicator']

        try:
            df = pd.DataFrame(self.parse_text_to_numpy(), columns=columns)

            for col in int_columns:
                df[col] = df[col].astype(int)

            return df
        except ValueError:
            print('Could not create pandas dataframe object from the input numpy array')

    def _select_animation_frame(self):

        '''
        Helper function for self.plot returning a mapbox density map of collected lightning strikes

        :return: animation frame interval for the collected dataset, lowest non unique time interval of date,
        hour or minute
        '''

        if len(self.dataframe()[['Year', 'Month', 'Day of Month']].drop_duplicates()) == 1:
            if len(self.dataframe()['Hour'].unique()) == 1:
                return 'Minute'
            else:
                return 'Hour'
        else:
            return 'Date'

    def plot(self, animate=True, return_fig=False):

        '''
        Function to plot the collected lightning dataset using a plotly mapbox density map.
        The function accepts two parameters; animate (defaults to True) and return_fig (defaults to False)

            animate adds an animation frame to the map figure, with the first non unique time interval level in the
            dataset set as the animation frame value (either date, hour or minute).
            The appropriate animation frame value is determined by the _select_animation_frame function.

            return_fig allows for the plotly figure itself to be returned from the function so it can be used as the
            user sees fit.

        A reference for the mapbox density plot can be found at:

            https://plotly.com/python/mapbox-density-heatmaps/

        :param animate: defaults to true, adds a time frame animation to the plot.
        :param return_fig: defaults to False, when set to true the plotly figure object will be returned instead of
        fig.show() being called from the plot function.
        :return:
        '''

        fig = px.density_mapbox(
            self.dataframe().sort_values(by=['Year', 'Month', 'Day of Month'], ascending=True),
            lat='Latitude', lon='Longitude',
            animation_frame=(self.dataframe() \
                             .sort_values(by=['Year', 'Month', 'Day of Month'], ascending=True) \
                             .sort_values(by='Hour', ascending=True)[self._select_animation_frame()]
                             if self._select_animation_frame() is not 'Date' \
                                 else self.dataframe().sort_values(by=['Year', 'Month', 'Day of Month'], ascending=True) \
                             .apply(lambda row: datetime.datetime(int(row['Year']),
                                                                  int(row['Month']),
                                                                  int(row['Day of Month'])).date(), axis=1)) \
                if animate is True else None,
            zoom=5,
            radius=3,
            mapbox_style="stamen-terrain",
            height=700,
            title="Lightning strikes for time period %s to %s " % \
                  (str(self.dataframe().sort_values(by=['Year', 'Month', 'Day of Month'], ascending=True) \
                       .apply(lambda row: datetime.datetime(int(row['Year']),
                                                            int(row['Month']),
                                                            int(row['Day of Month'])).date(),
                              axis=1).min()),
                   str(self.dataframe().sort_values(by=['Year', 'Month', 'Day of Month'], ascending=True) \
                       .apply(lambda row: datetime.datetime(int(row['Year']),
                                                            int(row['Month']),
                                                            int(row['Day of Month'])).date(),
                              axis=1).max()) +
                   ("<br>Animation interval: %s" % self._select_animation_frame() if animate else '')
                   )
        )

        if return_fig:
            return fig
        else:
            fig.show()
