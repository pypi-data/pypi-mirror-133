import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="cvplayer",
    version="1.0.0",
    description="a simple video player written in python using ffpyplayer and OpenCV",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/addyett/video-player",
    author="addyett",
    author_email="g.aditya2048@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["video_player"],
    include_package_data=True,
    install_requires=["cv2", "ffpyplayer", 'numpy', 'pillow'],
    entry_points={
        "console_scripts": [
            "videoplayer=video_player.__main__:main",
        ]
    },
)
