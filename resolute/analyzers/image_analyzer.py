import cv2
import torch
import torchvision.models as models
import torchvision.transforms as T
import numpy as np
from skimage.metrics import structural_similarity as ssim
from PIL import Image

# ---------- ResNet Feature Extractor ----------
_resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
_resnet = torch.nn.Sequential(*list(_resnet.children())[:-1])  # cut classifier
_resnet.eval()

_transform: T.Compose = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225])
])

# ---------- SSIM ----------
def ssim_compare_images(path1: str, path2: str) -> float:
    img1 = cv2.imread(path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path2, cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        return 0.0

    img1 = cv2.resize(img1, (256, 256))
    img2 = cv2.resize(img2, (256, 256))

    result = ssim(img1, img2, full=True)
    if isinstance(result, tuple):
        score, _ = result  # newer versions return (score, diff)
    else:
        score = result     # fallback if only a float is returned

    return float(score)


# ---------- ResNet Cosine ----------
def resnet_cosine_pair(path1: str, path2: str) -> float:
    try:
        def _extract(path: str):
            img = Image.open(path).convert("RGB")
            tensor = _transform(img).unsqueeze(0)
            with torch.no_grad():
                feat = _resnet(tensor).squeeze().numpy()
            return feat / np.linalg.norm(feat)

        v1 = _extract(path1)
        v2 = _extract(path2)
        return float(np.dot(v1, v2))
    except Exception:
        return 0.0

# ---------- Color Histogram ----------
def compare_color_histograms(path1: str, path2: str) -> float:
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None or img2 is None:
        return 0.0

    hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    hist1 = cv2.calcHist([hsv1], [0, 1], None, [50, 60], [0, 180, 0, 256])
    hist2 = cv2.calcHist([hsv2], [0, 1], None, [50, 60], [0, 180, 0, 256])

    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return float(score)
