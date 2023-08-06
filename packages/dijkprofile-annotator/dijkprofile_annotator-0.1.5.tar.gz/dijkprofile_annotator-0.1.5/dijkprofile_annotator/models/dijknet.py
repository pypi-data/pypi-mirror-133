import torch
import torch.nn as nn
from dijkprofile_annotator.utils import extract_img


class Double_conv(nn.Module):
    '''(conv => ReLU) * 2 => MaxPool2d'''
    def __init__(self, in_ch, out_ch, p):
        """
        Args:
            in_ch(int) : input channel
            out_ch(int) : output channel
        """
        super(Double_conv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(in_ch, out_ch, 3, padding=1, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv1d(out_ch, out_ch, 5, padding=2, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv1d(out_ch, out_ch, 7, padding=3, stride=1),
            nn.ReLU(inplace=True),
            nn.Dropout(p=p)
        )
    def forward(self, x):
        x = self.conv(x)
        return x


class Conv_down(nn.Module):
    '''(conv => ReLU) * 2 => MaxPool2d'''
    
    def __init__(self, in_ch, out_ch, p):
        """
        Args:
            in_ch(int) : input channel
            out_ch(int) : output channel
        """
        super(Conv_down, self).__init__()
        self.conv = Double_conv(in_ch, out_ch, p)
        self.pool = nn.MaxPool1d(kernel_size=2, stride=2, padding=0)

    def forward(self, x):
        x = self.conv(x)
        pool_x = self.pool(x)
        return pool_x, x


class Conv_up(nn.Module):
    '''(conv => ReLU) * 2 => MaxPool2d'''
    
    def __init__(self, in_ch, out_ch, p):
        """
        Args:
            in_ch(int) : input channel
            out_ch(int) : output channel
        """
        super(Conv_up, self).__init__()
        self.up = nn.ConvTranspose1d(in_ch, out_ch, kernel_size=2, stride=2)
        self.conv = Double_conv(in_ch, out_ch, p)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        x1_dim = x1.size()[2]
        x2 = extract_img(x1_dim, x2)
        x1 = torch.cat((x1, x2), dim=1)
        x1 = self.conv(x1)
        return x1


class Dijknet(nn.Module):
    """Dijknet convolutional neural network. 1D Unet variant."""

    def __init__(self, in_channels, out_channels, p=0.25):
        """Dijknet convlutional neural network, 1D Unet Variant. Model is probably a bit too big
        for what it needs to do, but it seems to work just fine.

        Args:
            in_channels (int): number of input channels, should be 1
            out_channels (int): number of output channels/classes
            p (float, optional): dropout chance for the dropout layers. Defaults to 0.25.
        """
        super(Dijknet, self).__init__()
        self.Conv_down1 = Conv_down(in_channels, 64, p)
        self.Conv_down2 = Conv_down(64, 128, p)
        self.Conv_down3 = Conv_down(128, 256, p)
        self.Conv_down4 = Conv_down(256, 512, p)
        self.Conv_down5 = Conv_down(512, 1024, p)
        self.Conv_up1 = Conv_up(1024, 512, p)
        self.Conv_up2 = Conv_up(512, 256, p)
        self.Conv_up3 = Conv_up(256, 128, p)
        self.Conv_up4 = Conv_up(128, 64, p)
        self.Conv_up5 = Conv_up(128, 64, p)
        self.Conv_out = nn.Conv1d(64, out_channels, 1, padding=0, stride=1)
        self.Conv_final = nn.Conv1d(out_channels, out_channels, 1, padding=0, stride=1)

    def forward(self, x):
        x, conv1 = self.Conv_down1(x)
        x, conv2 = self.Conv_down2(x)
        x, conv3 = self.Conv_down3(x)
        x, conv4 = self.Conv_down4(x)
        _, x = self.Conv_down5(x)
        x = self.Conv_up1(x, conv4)
        x = self.Conv_up2(x, conv3)
        x = self.Conv_up3(x, conv2)
        x = self.Conv_up4(x, conv1)
        # final upscale to true size
        x = self.Conv_out(x)
        x = self.Conv_final(x)
        return x
