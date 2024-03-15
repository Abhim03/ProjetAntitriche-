# antitriche

In the context of a new experimental project on the analysis of code produced by developers as well as candidates at Société Générale, we are looking to implement a code analysis tool that detects the code duplication rate:

- For SG developers in comparison to the code already present on our versioning tool
- For candidate applicants: In comparison to the code already submitted by past candidates In comparison to the code produced by GitHub Copilot In comparison to the code produced by OpenAI

Machine learning will help analyze the percentage of similarity among the produced codes. It will indicate the maximum observed correlation rate with respect to the specified data sources and serve as a point of comparison, providing a percentage of confidence regarding a potential suspicion of duplication concerning any of these data sources.

Run `pip install -r requirements.txt` to install the required packages.

Then run `streamlit run app.py` to launch the web app.

current endpoint link : https://952a-129-104-253-35.ngrok-free.app/