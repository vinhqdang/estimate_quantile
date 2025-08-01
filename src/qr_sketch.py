
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

class QRSketch:
    def __init__(self, q, batch_size=100):
        if not 0 < q < 1:
            raise ValueError("Quantile q must be in (0, 1)")
        self.q = q
        self.batch_size = batch_size
        self.buffer = []
        self.model = None
        self.data = pd.DataFrame(columns=['x', 'y'])

    def add(self, value):
        self.buffer.append(value)
        if len(self.buffer) >= self.batch_size:
            self._train()

    def _train(self):
        if not self.buffer:
            return

        new_data = pd.DataFrame({'x': np.arange(len(self.buffer)), 'y': self.buffer})
        
        if self.data.empty:
            self.data = new_data
        else:
            self.data = pd.concat([self.data, new_data], ignore_index=True)

        # We need to have some variation in x for the regression to work.
        # The intercept-only model is what we want here.
        self.model = smf.quantreg('y ~ 1', self.data).fit(q=self.q)
        
        self.buffer = []

    def quantile(self):
        if self.model is None:
            if not self.buffer:
                return np.nan
            else:
                return np.percentile(self.buffer, self.q * 100)
        
        # For an intercept-only model, the quantile is the intercept.
        return self.model.params['Intercept']
