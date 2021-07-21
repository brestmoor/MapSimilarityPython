# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

# Set the working directory 
WORKDIR /app

COPY ./environment.yml .

# Copy the current directory contents into the container
RUN apt-get update
RUN conda env create --file environment.yml

COPY . .

SHELL ["conda", "run", "-n", "MapSimilarityPython", "/bin/bash", "-c"]

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "MapSimilarityPython", "voila", "cities_similarity_app.ipynb", "--port", "80"]