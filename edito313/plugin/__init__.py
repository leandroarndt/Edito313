import os, sys

# Stores the path to the downloaded plugins directory.
PLUGINSPATH = os.path.join(os.environ.get('SITEPATH', '.'), 'plugin')

sys.path.append(PLUGINSPATH)
