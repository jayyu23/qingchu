import urllib.request
import requests
import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms, datasets, models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io


class InferenceModel:
    def __init__(self, pth_path):
        pth_dict = torch.load(pth_path)
        self.model_classes = pth_dict['classes']
        self.model = pth_dict['model']
        self.model.eval()
        self.device = torch.device("cpu")
        self.transforms = transforms.Compose([
                          transforms.Resize(256),
                          transforms.CenterCrop(224),
                          transforms.ToTensor(),
                          ])
        self.tensor_to_pil = transforms.ToPILImage()

    def test_single_image(self, image_path, is_url=True, display=False):
        if is_url:
            try:
                r = urllib.request.urlopen(image_path)
                pil_image = Image.open(r)
            except Exception:
                return "N/A"
        else:
            pil_image = Image.open(image_path)
        im_class = self.predict_PIL_image(pil_image)
        if display:
            plt.imshow(pil_image)
            plt.title(f"Class: {im_class}")
            plt.show()
        print(im_class)
        return im_class

    def predict_PIL_image(self, pil_image):
        image_tensor = self.transforms(pil_image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        input = input.to(self.device)
        output = self.model(input)
        index = output.data.cpu().numpy().argmax()
        im_class = self.model_classes[index]
        return im_class

    def test_random_from_folder(self, N, data_dir):
        data = datasets.ImageFolder(data_dir, transform=self.transforms)
        indices = list(range(len(data)))
        np.random.shuffle(indices)
        idx = indices[:N]
        from torch.utils.data.sampler import SubsetRandomSampler
        sampler = SubsetRandomSampler(idx)
        loader = torch.utils.data.DataLoader(data,
                                             sampler=sampler, batch_size=N)
        dataiter = iter(loader)
        images, labels = next(dataiter)
        fig = plt.figure(num=len(images), figsize=(20, 20))
        for ii in range(len(images)):
            image = self.tensor_to_pil(images[ii])
            im_class = self.predict_PIL_image(image)
            sub = fig.add_subplot(1 + (ii // 5), 5, ii + 1)
            # res = int(labels[ii]) == im_class
            sub.set_title(str(im_class  ))
            plt.axis('off')
            plt.imshow(image)
        plt.show()


if __name__ == "__main__":
    inf_model = InferenceModel('resnet18_transfer_full1624808047582392000.pth')
    # result = inf_model.test_single_image('data/small-clothing/qc_val/lachlanite564_yn8s51tp.png')
    folder = "data/small-clothing/qc_val/batch"
    # inf_model.test_random_from_folder(10, folder)
    # print(result)