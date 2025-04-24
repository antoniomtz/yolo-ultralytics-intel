# Use DLStreamer as base image with GPU and NPU support
FROM intel/dlstreamer:2025.0.1.3-dev-ubuntu22

user root


WORKDIR /app

# Install system dependencies required by OpenCV, Qt, and X11 forwarding
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    # Add libraries needed for Qt/XCB plugin
    libxkbcommon-x11-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb1 \
    # Qt platform plugin dependencies (might vary slightly based on base image/Qt version)
    libqt5x11extras5 \
    libxcb-cursor0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

