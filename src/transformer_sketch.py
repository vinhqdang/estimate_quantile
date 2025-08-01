
import torch
import torch.nn as nn
import numpy as np

class TransformerModel(nn.Module):
    def __init__(self, input_dim, model_dim, nhead, num_layers, output_dim):
        super(TransformerModel, self).__init__()
        self.encoder = nn.Linear(input_dim, model_dim)
        self.transformer_encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=model_dim, nhead=nhead),
            num_layers=num_layers
        )
        self.decoder = nn.Linear(model_dim, output_dim)

    def forward(self, src):
        src = self.encoder(src)
        output = self.transformer_encoder(src)
        output = output.mean(dim=1) # Average over the sequence length
        output = self.decoder(output)
        return output

class TransformerSketch:
    def __init__(self, q, batch_size=100, model_dim=128, nhead=4, num_layers=2):
        if not 0 < q < 1:
            raise ValueError("Quantile q must be in (0, 1)")
        self.q = q
        self.batch_size = batch_size
        self.buffer = []
        self.data = []
        self.model = TransformerModel(input_dim=1, model_dim=model_dim, nhead=nhead, num_layers=num_layers, output_dim=11) # Output dim is 11 for 11 quantiles
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.L1Loss() # Quantile regression loss
        self._is_trained = False

    def add(self, value):
        self.buffer.append(value)
        if len(self.buffer) >= self.batch_size:
            self._train()

    def _train(self):
        if not self.buffer:
            return

        self.data.extend(self.buffer)
        self.data = self.data[-1000:]
        x_train = torch.FloatTensor(self.data).unsqueeze(-1)
        
        # Generate multiple quantile targets for better training
        qs = np.linspace(0, 1, 11)
        y_train = torch.FloatTensor([np.percentile(self.data, q * 100) for q in qs]).unsqueeze(0)

        # Reshape x_train to be a single sequence
        x_train = x_train.unsqueeze(0)
        y_train = y_train.repeat(x_train.size(0), 1)


        # Training loop
        self.model.train()
        for _ in range(100): # Increased epochs
            self.optimizer.zero_grad()
            output = self.model(x_train)
            
            loss = self.quantile_loss(output, y_train, torch.FloatTensor(qs))
            loss.backward()
            self.optimizer.step()

        self.last_x = x_train
        self.buffer = []
        self._is_trained = True

    def quantile(self):
        if not self._is_trained:
            if not self.buffer:
                return np.nan
            else:
                return np.percentile(self.buffer, self.q * 100)

        self.model.eval()
        if len(self.buffer) > 0:
            x_test = torch.FloatTensor(self.buffer).unsqueeze(-1).unsqueeze(0)
            with torch.no_grad():
                predictions = self.model(x_test).squeeze(0)
                # Interpolate to find the desired quantile
                qs = np.linspace(0, 1, 11)
                return np.interp(self.q, qs, predictions.numpy())
        elif hasattr(self, 'last_x'):
             with torch.no_grad():
                predictions = self.model(self.last_x).squeeze(0)
                # Interpolate to find the desired quantile
                qs = np.linspace(0, 1, 11)
                return np.interp(self.q, qs, predictions.numpy())
        else:
            return np.nan


    def quantile_loss(self, y_pred, y_true, q):
        e = y_true - y_pred
        q = q.unsqueeze(0)
        return torch.mean(torch.max(q * e, (q - 1) * e))
