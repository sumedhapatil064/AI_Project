import torch, torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

class EncoderCNN(nn.Module):
    def __init__(self, embed_size=256):
        super().__init__()
        resnet = models.resnet18(weights=None)
        modules = list(resnet.children())[:-1]
        self.resnet = nn.Sequential(*modules)
        self.linear = nn.Linear(resnet.fc.in_features, embed_size)
        self.bn = nn.BatchNorm1d(embed_size, momentum=0.01)
    def forward(self, images):
        with torch.no_grad():
            features = self.resnet(images).reshape(images.size(0), -1)
        features = self.bn(self.linear(features))
        return features

class DecoderRNN(nn.Module):
    def __init__(self, embed_size, hidden_size, vocab_size=5000, num_layers=1):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_size)
        self.lstm = nn.LSTM(embed_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, vocab_size)
    def forward(self, features, captions):
        embeddings = torch.cat((features.unsqueeze(1), self.embed(captions)), 1)
        h, _ = self.lstm(embeddings)
        outputs = self.linear(h)
        return outputs

if __name__ == "__main__":
    # Demo shapes only
    encoder = EncoderCNN()
    decoder = DecoderRNN(embed_size=256, hidden_size=512)
    images = torch.randn(2,3,224,224)
    feats = encoder(images)
    caps = torch.randint(0, 4999, (2, 10))
    out = decoder(feats, caps)
    print("Shapes:", feats.shape, out.shape)
