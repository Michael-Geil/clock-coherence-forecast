"""
Master pipeline script

Reproduces all results for:
Emergent Causality and Unaligned Geometry:
Predictive Clock Phase Correlations
"""

import subprocess
import sys

def run(cmd):
    print("\n>>>", " ".join(cmd))
    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit("Command failed")

def main():

    # 1) Scrape Circular-T data
    run([sys.executable, "scrape_circularT_html.py"])

    # 2) Run phase extraction + forecasting + surrogate tests
    run([sys.executable, "analysis.py"])

    print("\nAll analyses complete.")
    print("Figures saved to figures/")
    print("Tables saved to tables/")

if __name__ == "__main__":
    main()
