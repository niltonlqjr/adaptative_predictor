CONTAINER_CMD="docker"             # Container application to be used
CONTAINER_IMAGE="adaptative"       # Name of image to be generated
VOLUME_DIR="$(realpath $(pwd))/.." # Mappped volume
WORK_DIR="$(realpath $(pwd))/.."   # Work dir