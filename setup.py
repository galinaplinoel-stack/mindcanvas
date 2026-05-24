from setuptools import setup, find_packages

setup(
    name="mindcanvas",
    version="1.0.0",
    description="AI-powered mind mapping — visualize and organize ideas",
    author="MindCanvas Team",
    packages=find_packages(exclude=["tests", "api", "web"]),
    python_requires=">=3.10",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
