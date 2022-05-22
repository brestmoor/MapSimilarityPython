# MapSimilarityPython
An app for calculating parameters for cities such as "average street length" or "average distance between buildings", and then allowing to calculate similarity 
for cities and whole regions. For assessing similarity Euclidean distance is used. For presentation on charts, data dimentionality is reduced using the PCA algorithm.

![example_calculations](https://user-images.githubusercontent.com/17832444/169710293-2e5ab6df-a1ad-439d-af13-66f89c5eed00.png)


- functions.py and graphFunctions.py - contain functions for calculating parameters for a given city
- experiments.py - groups functions into "profiles" that can be used to better understand similarities or differences between cities
- scores.py - calculates parameters for given cities and citeria using multiple threads. Output is returned as a DataFrame
- pca.py - contains functions for PCA algorithm
- svm.py - contains functions for SVM algorithm. It was used to validate if SVM algorithm would be able to distinguish compared regions.
- similarity.py - contains functions for calculating similarity based on different metrics and for calculating silhouette score.
- cities_similarity_app.ipynb - Jupyter file for running comparison experiments
- docker-compose.yml - docker compose file for setting up local OpenStreetMap database, Overpass API and the app.

![england_france_plot](https://user-images.githubusercontent.com/17832444/169710296-de40c519-2ad2-4fbc-8531-a72627c6b971.png)
![england_france_map](https://user-images.githubusercontent.com/17832444/169710300-fcab91c1-ed89-4557-abd0-48f4264634df.png)
