#!/bin/bash --login
# The --login ensures the bash configuration is loaded,
# enabling Conda.
set -euo pipefail
conda activate MapSimilarityPython
exec voila cities_similarity_app.ipynb --port 80 --allow-root