import numpy as np
import pandas as pd
from kolibri.core.component import Component

class WindowGenerator(Component):
    """Base class for sliding and expanding window splitter."""

    defaults ={
        "fixed":{
            "targets": None,
            "dropnan": True,
            "shuffle": False,
            "seed": None,
            "shift": 1,
            "step_length": 1,
            "sampling_rate": 1,
            "start_index": 0,
            "groups": [],
            "time_features":[]
        },
        "tunable":{
            "window_length": {
                "value": None,
            }
        }

    }

    def __init__( self,  data, configs={}):
        super(WindowGenerator, self).__init__(parameters=configs)
        self.data=data

        self.step_length = self.get_parameter("step_length")

        self.sampling_rate =self.get_parameter ("sampling_rate")

        self.window_length=self.get_parameter("window_length")

        self.shift=self.get_parameter("shift")

        self.targets=self.get_parameter("targets")

        self.shuffle=self.get_parameter("shuffle")

        self.seed = self.get_parameter("seed")

    def _series_to_timeseries(self, data, targets):
        end_index = len(data)
        num_seqs = end_index - (self.window_length * self.sampling_rate) - self.shift + 1

        # Generate start positions
        start_positions = np.arange(self.shift, num_seqs+self.shift, self.step_length)
        target_values=[]
        if self.targets is not None:
            target_values = [data[i-self.shift][targets] for i in start_positions]

        if self.shuffle:
            if self.seed is None:
                self.seed = np.random.randint(1e6)
            rng = np.random.RandomState(self.seed)
            rng.shuffle(start_positions)

        indices_map = lambda i, positions: range(  # pylint: disable=g-long-lambda
            positions[i-self.shift],
            positions[i-self.shift] + self.window_length * self.sampling_rate,
            self.sampling_rate)
        features = [data[i] for i in [indices_map(i, start_positions) for i in start_positions]]
        if self.targets is not None:
            return zip(features, target_values)
        else:
            return iter(features)

    def __iter__(self):

        for group in self.data[1]:
            group = group.drop(columns=self.get_parameter("groups")).sort_values(by=self.get_parameter("time_features"), ascending=False).drop(columns=self.get_parameter("time_features"))

            targets = [group.columns.get_loc(c) for c in self.targets if c in group]
#            self.features= [group.columns.get_loc(c) for c in group.columns if c not in self.get_parameter("time_features")]
            for (feature, label) in self._series_to_timeseries(group.values, targets):
                yield np.array(feature), np.array(label)
