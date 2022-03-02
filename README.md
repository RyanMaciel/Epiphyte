# Epiphyte
### Background
During my last semester of undergrad at the University of Rochester I am doing an Independent Study in Generative Art advised by [Professor Ashenfelder](https://www.sas.rochester.edu/dms/people/director.html), Director of the Digital Media Studies department. This repo houses the software for the first project of the study.

### Concept
Epiphyte will be a installation piece involving projection on the ceiling of the space it is placed in. Viewers will be able to interact with the projection by moving their bodies below it. A high-mounted camera will use object detection algorithms (probably) based on deep neural net architectures to track viewers and project their positions onto the cieling.

### What's in this repo?
- Some jupyter notebooks testing different CV approaches for the tracking (but only locally because I'm testing it on videos of me and notebooks results are tedious to clean for the internet)
- A [visualization](https://editor.p5js.org/rmaciel2/sketches/UPYOP6oRZ) implemented in [p5.js](https://p5js.org/)
- Early attempts to connect the two. Right now, creating a simple websockets server in python and serving to js running locally in browser.
