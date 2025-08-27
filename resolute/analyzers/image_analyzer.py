import cv2
import torch
import torchvision.models as models
import torchvision.transforms as T
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image

# Pretrained ResNet18 for feature extraction
_resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
# Remove classifier by replacing with identity function (not changing the layer type)
_resnet.fc = torch.nn.Linear(_resnet.fc.in_features, _resnet.fc.in_features)
_resnet.fc.weight.data = torch.eye(_resnet.fc.in_features)
_resnet.fc.bias.data = torch.zeros(_resnet.fc.in_features)
_resnet.eval()

_transform: T.Compose = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

def ssim_compare_images(path1: str, path2: str) -> float:
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        return 0.0
    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))
    score = ssim(img1, img2, full=True)[0]
    return float(score)

def resnet_cosine_pair(path1: str, path2: str) -> float:
    try:
        # Load and transform images to tensors
        img1_tensor = _transform(Image.open(path1).convert("RGB"))
        img2_tensor = _transform(Image.open(path2).convert("RGB"))
        
        # Add batch dimension using torch.unsqueeze with explicit type casting
        img1_batch = torch.unsqueeze(img1_tensor, 0)  # type: ignore
        img2_batch = torch.unsqueeze(img2_tensor, 0)  # type: ignore
    except Exception:
        return 0.0

    with torch.no_grad():
        feat1 = _resnet(img1_batch).numpy().flatten()
        feat2 = _resnet(img2_batch).numpy().flatten()

    cos = np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))
    return float(cos)
