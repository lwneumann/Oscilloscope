# Variables
CXX = g++
CXXFLAGS = -Wall -O2 -std=c++17
BUILD_DIR = build
SRC_DIR = src
SHAPES_DIR = $(SRC_DIR)/shapes

# PortAudio-specific flags
PORTAUDIO_LIBS = -lportaudio
PORTAUDIO_INCLUDES = -I/usr/include/include
PORTAUDIO_LIB_DIRS = -L/usr/lib/x86_64-linux-gnu/

# Targets
all: build

# Build the executable from all .cpp files in src/ and src/shapes/
build: $(BUILD_DIR)/main

$(BUILD_DIR)/main: $(wildcard $(SRC_DIR)/*.cpp) $(wildcard $(SHAPES_DIR)/*.cpp)
	mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(PORTAUDIO_LIB_DIRS) -o $@ $^ $(PORTAUDIO_LIBS) $(PORTAUDIO_INCLUDES) -lm

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

.PHONY: all build clean