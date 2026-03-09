# Set Qt to use offscreen platform so pytest-qt tests run without a display.
# FOR TESTING ONLY !!!!!!!
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
