#!/bin/bash
cd ~/maedongyee_ws
rm -rf build install log
colcon build --packages-select aicar_msgs && \
source install/setup.bash && \
colcon build --packages-skip aicar_msgs --symlink-install && \
source install/setup.bash && \
echo "✅ Build complete."
