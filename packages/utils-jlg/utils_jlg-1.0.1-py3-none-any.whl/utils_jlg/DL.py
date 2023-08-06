import os
import torch
from torch import nn
import pytorch_lightning as pl
from torch.utils.data import DataLoader,Dataset
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from pytorch_lightning.callbacks import Callback
import torch.nn.functional as F
import matplotlib.pyplot as plt
import operator
from functools import reduce
from functools import partial
import scipy.io



"""
from pytorch_lightning.callbacks import EarlyStopping
from section_1_models import SimEvalCallback
from pytorch_lightning.loggers import CSVLogger, TensorBoardLogger
from section_1_models import DataModule
import fire


    logger_csv = CSVLogger(logs_dir, name= name_experiment)
    logger_tensorboard = TensorBoardLogger(logs_dir, name= name_experiment)


    callback = SimEvalCallback(datamod, results_dir,save_every = 10)
    early_stopping = EarlyStopping('val_loss', patience = 10, min_delta = 1e-4)

    trainer = pl.Trainer(max_epochs = mc["max_epochs"], callbacks = [early_stopping, callback],gpus=ic["gpus"],flush_logs_every_n_steps = 20, log_every_n_steps= 20,
                    logger = [logger_csv,logger_tensorboard],default_root_dir = models_checkpoints_dir)

    trainer.fit(model, datamod.train_dataloader(), datamod.val_dataloader())


"""

class TemplateCallbackPL(Callback):

    def __init__(self ):
        pass

    def on_epoch_end(self,trainer, model):
        #epoch = trainer.current_epoch
        self._epoch+=1
        epoch = int(self._epoch/2) #dirty fix

        if epoch%self._save_every == 0:

            pass
class TemplateModelPL(pl.LightningModule):

    def __init__(self,):
        super().__init__()

        self._model = model(*args_model, **kwargs_model)
        self.criterion = torch.nn.L1Loss()
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    def forward(self,x):

        x = self._model(x)

        return x

    def training_step(self, batch, batch_idx):



        return loss

    def training_epoch_end(self, train_step_results):


        lr = self.optimizers().param_groups[0].get("lr")

        self.log("lr", lr)

        return {"log": {"epoch_training_loss": epoch_training_loss } }

    def validation_epoch_end(self, validation_step_outputs):

        """

        validation_step_outputs list of whatever val step returns
        """


        self.log("val_loss", val_loss)


        return val_loss


    def validation_step(self, batch, batch_idx):

        pass

        return None




    def test_step(self, batch, batch_idx):

        pass

        return None



    def configure_optimizers(self):

        optimizer = torch.optim.Adam(self.parameters(), lr = self._lr)

        lr_scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5, factor=0.5, threshold = 1e-3 ,verbose = True, eps = 1e-6)


        scheduler = {
            'scheduler': lr_scheduler,
            'reduce_on_plateau': True,
            # val_checkpoint_on is val_loss passed in as checkpoint_on
            'monitor': 'loss_s1'
        }

        return [optimizer], [scheduler]



class TemplateDataModulePL(pl.LightningDataModule):#problemdatamoduele import

    def __init__(self):

        super().__init__()

        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    def prepare_data(self):
        """
        load data etc
        """

        pass
    def setup(self):

        """
        Split create train/test datasets

        """
        self.train_dataset = -1
        self.test_dataset = -1
    def train_dataloader(self):

        return DataLoader(self.train_dataset, batch_size = self._batch_size, shuffle = True)

    def val_dataloader(self):

        return DataLoader(self.test_dataset, batch_size = self._batch_size, shuffle = True)



class SineLayer(nn.Module):


    def __init__(self, in_features, out_features,
                 is_first=False, omega_0=30):
        super().__init__()
        self.omega_0 = omega_0
        self.is_first = is_first

        self.in_features = in_features
        self.linear = nn.Linear(in_features, out_features)

        self.init_weights()

    def init_weights(self):
        with torch.no_grad():
            if self.is_first:
                self.linear.weight.uniform_(-1 / self.in_features,
                                             1 / self.in_features)
            else:
                self.linear.weight.uniform_(-np.sqrt(6 / self.in_features) / self.omega_0,
                                             np.sqrt(6 / self.in_features) / self.omega_0)

    def forward(self, input):
        return torch.sin(self.omega_0 * self.linear(input))



class Siren(nn.Module):
    def __init__(self, in_features, out_features , hidden_layers = 5 ,  hidden_features = 50,
                 first_omega_0=30, hidden_omega_0=1., final_linear = False):
        super().__init__()

        self.net = []
        self.net.append(SineLayer(in_features, hidden_features,
                                  is_first=True, omega_0=first_omega_0))

        for i in range(hidden_layers):
            self.net.append(SineLayer(hidden_features, hidden_features,
                                      is_first=False, omega_0=hidden_omega_0))

        if final_linear:
            final_linear = nn.Linear(hidden_features, out_features)

            with torch.no_grad():
                final_linear.weight.uniform_(-np.sqrt(6 / hidden_features) / hidden_omega_0,
                                                np.sqrt(6 / hidden_features) / hidden_omega_0)

            self.net.append(final_linear)


        self.net = nn.Sequential(*self.net)

    def forward(self, coords):

        output = self.net(coords)

        return output





class ResidualDownBlock(nn.Module):

    def __init__(self, in_channels, out_channels , n_layers = 2, stride = 1, padding = 1, normalization = True):

        super().__init__()

        layers = []

        for i in range(n_layers):

            if i == 0:
                _in_channels = in_channels
                _stride = stride
            else:
                _in_channels = out_channels
                _stride = 1

            layer = nn.Conv2d(_in_channels, out_channels, kernel_size=3, stride = _stride,
                     padding=padding, bias=True) #Bias can be set to false if using batch_norm ( is present there)

            torch.nn.init.kaiming_uniform_(layer.weight, a=0, mode='fan_in', nonlinearity='leaky_relu')

            layers.append(layer)

        if normalization:
            self.norm = torch.nn.BatchNorm2d(out_channels)
        else:
            self.norm = nn.Identity()

        self._layers = nn.ModuleList(layers)

        if (in_channels != out_channels) or (stride>1):

            self._shortcut = nn.Conv2d(in_channels, out_channels, kernel_size = 3, stride = stride, padding = padding)

        else:

            self._shortcut = nn.Identity()

        self._activation = torch.nn.ReLU()

    def forward(self, x):

        _x = x

        for layer in self._layers:

            _x = self._activation(layer(_x))

        out = self.norm(self._shortcut(x) + _x)#WRONG BATCH NORM WRONGLY APP

        return out

class BasicResNet(nn.Module):

    def __init__(self, in_channels, hidden_channels, out_channels, blocks = [2, 2, 2, 2, 2], add_input_output = False, normalization = True):

        super().__init__()

        layers = []

        for i,_block in enumerate(blocks):


            if i == 0:
                _in_channels = in_channels
            else:
                _in_channels = hidden_channels


            layer = ResidualDownBlock(_in_channels, hidden_channels, stride = 1, padding=1, normalization = normalization)

            layers.append(layer)



        self._hidden_layers = nn.ModuleList(layers)


        self._out_layer = nn.Conv2d( hidden_channels , out_channels, kernel_size=1, stride = 1,
             padding=0, bias=True)

        self._add_input_output = add_input_output


        self.act_out = torch.nn.Tanh()


    def forward(self, x):

        _x = x

        for layer in self._hidden_layers:

            _x = layer(_x)

        if self._add_input_output:

            _x = self._out_layer(_x) + x

        else:

            _x = self._out_layer(_x)

        #_x = self.act_out(_x)
        return _x






############################################# Fourier neural operator with annotations, copied from ###############################
#https://github.com/zongyi-li/fourier_neural_operator/blob/master/fourier_2d_time.py
########################################### ####################################
#Complex multiplication
def compl_mul2d(a, b):
    op = partial(torch.einsum, "bctq,dctq->bdtq") #sum over channels
    return torch.stack([
        op(a[..., 0], b[..., 0]) - op(a[..., 1], b[..., 1]),
        op(a[..., 1], b[..., 0]) + op(a[..., 0], b[..., 1])
    ], dim=-1)

################################################################
# fourier layer
################################################################

class SpectralConv2d_fast(nn.Module):
    def __init__(self, in_channels, out_channels, modes1, modes2):
        super(SpectralConv2d_fast, self).__init__()

        """
        2D Fourier layer. It does FFT, linear transform, and Inverse FFT.
        """

        self.in_channels = in_channels
        self.out_channels = out_channels
        self.modes1 = modes1 #Number of Fourier modes to multiply, at most floor(N/2) + 1
        self.modes2 = modes2

        self.scale = (1 / (in_channels * out_channels))
        self.weights1 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, 2))
        self.weights2 = nn.Parameter(self.scale * torch.rand(in_channels, out_channels, self.modes1, self.modes2, 2))

    def forward(self, x):
        batchsize = x.shape[0]
        #Compute Fourier coeffcients up to factor of e^(- something constant)
        x_ft = torch.rfft(x, 2, normalized=True, onesided=True)

        # Multiply relevant Fourier modes
        out_ft = torch.zeros(batchsize, self.in_channels, x.size(-2), x.size(-1)//2 + 1, 2, device=x.device)
        out_ft[:, :, :self.modes1, :self.modes2] = \
            compl_mul2d(x_ft[:, :, :self.modes1, :self.modes2], self.weights1)
        out_ft[:, :, -self.modes1:, :self.modes2] = \
            compl_mul2d(x_ft[:, :, -self.modes1:, :self.modes2], self.weights2)

        #Return to physical space
        x = torch.irfft(out_ft, 2, normalized=True, onesided=True, signal_sizes=(x.size(-2), x.size(-1)))
        return x

class SimpleBlock2d(nn.Module):
    def __init__(self, modes1, modes2, width, input_channel = 3):

        super(SimpleBlock2d, self).__init__()

        """
        The overall network. It contains 4 layers of the Fourier layer.
        1. Lift the input to the desire channel dimension by self.fc0 .
        2. 4 layers of the integral operators u' = (W + K)(u).
            W defined by self.w; K defined by self.conv .
        3. Project from the channel space to the output space by self.fc1 and self.fc2 .

        input: the solution of the previous 10 timesteps + 2 locations (u(t-10, x, y), ..., u(t-1, x, y),  x, y)
        input shape: (batchsize, x=64, y=64, c=12)
        output: the solution of the next timestep
        output shape: (batchsize, x=64, y=64, c=1)
        """

        self.modes1 = modes1
        self.modes2 = modes2
        self.width = width
        self.fc0 = nn.Linear(input_channel, self.width)### linear layer applied to multi dim input, operates on the last dim --> output  B,S,S,width
        # input channel is 3: previous time step + 2 locations (u(t-1, x, y),  x, y)

        self.conv0 = SpectralConv2d_fast(self.width, self.width, self.modes1, self.modes2)
        self.conv1 = SpectralConv2d_fast(self.width, self.width, self.modes1, self.modes2)
        self.conv2 = SpectralConv2d_fast(self.width, self.width, self.modes1, self.modes2)
        self.conv3 = SpectralConv2d_fast(self.width, self.width, self.modes1, self.modes2)
        self.w0 = nn.Conv1d(self.width, self.width, 1)
        self.w1 = nn.Conv1d(self.width, self.width, 1)
        self.w2 = nn.Conv1d(self.width, self.width, 1)
        self.w3 = nn.Conv1d(self.width, self.width, 1)
        self.bn0 = torch.nn.BatchNorm2d(self.width)
        self.bn1 = torch.nn.BatchNorm2d(self.width)
        self.bn2 = torch.nn.BatchNorm2d(self.width)
        self.bn3 = torch.nn.BatchNorm2d(self.width)


        self.fc1 = nn.Linear(self.width, 128)
        self.fc2 = nn.Linear(128, 1)

    def forward(self, x):
        batchsize = x.shape[0]
        size_x, size_y = x.shape[1], x.shape[2]
        x = self.fc0(x)
        x = x.permute(0, 3, 1, 2) ## to standard torch batch channel X,Y

        x1 = self.conv0(x)
        x2 = self.w0(x.view(batchsize, self.width, -1)).view(batchsize, self.width, size_x, size_y) #why 1D? just parameter saving?
        x = self.bn0(x1 + x2)
        x = F.relu(x)
        x1 = self.conv1(x)
        x2 = self.w1(x.view(batchsize, self.width, -1)).view(batchsize, self.width, size_x, size_y)
        x = self.bn1(x1 + x2)
        x = F.relu(x)
        x1 = self.conv2(x)
        x2 = self.w2(x.view(batchsize, self.width, -1)).view(batchsize, self.width, size_x, size_y)
        x = self.bn2(x1 + x2)
        x = F.relu(x)
        x1 = self.conv3(x)
        x2 = self.w3(x.view(batchsize, self.width, -1)).view(batchsize, self.width, size_x, size_y)
        x = self.bn3(x1 + x2)


        x = x.permute(0, 2, 3, 1)  ## from standard torch batch channel X,Y back to batch X,Y channel
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x

class FourierNet(nn.Module):
    def __init__(self, modes, width, position_grid = False):
        super().__init__()

        """
        A wrapper function
        """
        self._grid = position_grid
        self._device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if self._grid:
            input_channel = 3
        else:
            input_channel = 1

        self.conv1 = SimpleBlock2d(modes, modes, width, input_channel = input_channel)
        self._first = True #for lazy grid making with input shape


    def forward(self, x):


        if self._grid: ### Concatenating position encoding grid if true

            batch = x.shape[0]


            if self._first:
                S = x.shape[2]
                batch = x.shape[0]
                self._batch = batch
                gridx = torch.tensor(np.linspace(0, 1, S), dtype=torch.float)
                gridx = gridx.reshape(1, 1, S, 1).repeat([1, 1, 1, S])
                gridy = torch.tensor(np.linspace(0, 1, S), dtype=torch.float)
                gridy = gridy.reshape(1, 1, 1, S).repeat([1, 1, S, 1])
                self._grid_no_rep = torch.cat((gridx, gridy), dim = 1)
                self._grid = self._grid_no_rep.repeat(self._batch,1,1,1).to(self._device)
                self._first = False

            if not(batch == self._batch):
                self._grid = self._grid_no_rep.repeat(batch,1,1,1).to(self._device)
                self._batch = batch
            x = torch.cat((x,self._grid), dim = 1)



        x = x.permute(0, 2, 3, 1) #to adapt to code implementation
        x = self.conv1(x)
        x = x.permute(0, 3, 1, 2)

        return x


    def count_params(self):
        c = 0
        for p in self.parameters():
            c += reduce(operator.mul, list(p.size()))

        return c





#################################################
