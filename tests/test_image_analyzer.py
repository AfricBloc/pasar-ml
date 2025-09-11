import pytest
from resolute.analyzers import image_analyzer

def test_ssim_with_nonexistent_files():
    score = image_analyzer.ssim_compare_images("no_file1.png", "no_file2.png")
    assert score == 0.0

def test_resnet_cosine_with_invalid_input():
    score = image_analyzer.resnet_cosine_pair("no_file1.png", "no_file2.png")
    assert isinstance(score, float)

def test_color_hist_with_invalid_input():
    score = image_analyzer.compare_color_histograms("fake1.png", "fake2.png")
    assert score == 0.0
