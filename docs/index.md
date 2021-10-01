# SDR-projects

These projects are a portfolio of software defined radio (SDR) related work done for academic (degree-related) or amateur interest.  All projects were done in GNURadio (GR), an SDR framework written in Python, with the help of the included GUI GNURadio Companion (GRC). 

## Usage

### Download and Execution

1. `git clone git@github.com:EasyElectrons/SDR-projects.git`
2. `cd SDR-projects`
3. Open the project of your choosing in GNURadio Companion.
4. Hit the "generate flowgraph" button at the top.
5. Press run.

### Running in GNURadio Companion

These projects were developed in GR 3.8.  Certain release candidates of GR 3.8 are rather finnicky, with some of the common default blocks becoming broken.  It is advised to check that you are using a full released version of GR.  If there are issues with the flowgraph directly from download, I recommend deleting the offending blocks and reconfiguring them yourself using the instructions in the paper.

For the flowgraphs that output to /dev/pts/1, you must have two terminal windows open; the data will appear in the second window.

## Paper

Please visit the paper [ECE1898_SDR_Projects.pdf](./ECE1898_SDR_Projects.pdf).  It provides in-depth explanation on each component of the projects covered.

DISCLAIMER: This paper was completed as part of an undergraduate-level independent study for credit at the University of Pittsburgh.  The logo on the front page is owned by the University of Pittsburgh (Pitt).  Its presence does not imply Pitt's ownership of any part of the project, or the contents of this repository, but merely represents the author's association with Pitt at the time of writing.