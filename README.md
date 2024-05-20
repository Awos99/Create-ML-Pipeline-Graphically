# Streamlit Scikit-Learn Pipeline Builder

![Demo GIF](/static/demo.gif)

## Overview
This repository contains a Streamlit application that provides a graphical interface for building and customizing Scikit-Learn pipelines. Designed as a learning tool, it bridges the gap between complex coding requirements and fully automated systems, offering a hands-on approach to understanding machine learning workflows.

## How It Works
The application allows users to construct a machine learning pipeline using a user-friendly drag-and-drop interface:

1. **Data Upload**: Users start by uploading a CSV file.
2. **Column Selection**: Users specify which columns to use as predictors and which as the target.
3. **Pipeline Construction**:
   - A graphical interface displays the available steps of a machine learning pipeline.
   - Users drag and drop different pipeline blocks into place to construct their workflow.
4. **Execution and Customization**:
   - Clicking 'Execute' initializes the customization phase where users can configure the settings of individual blocks, especially the Column Transformers.
5. **Model Training**:
   - After customization, users can 'Fit' their model to the data, evaluate its performance, and see the test error.
6. **Model Export**:
   - The trained model can be downloaded as a `.joblib` file.

## Development Notes
- **Error Handling**: Minimal error handling is currently implemented.
- **Unique Naming**: Each pipeline block must have a unique name to avoid conflicts.

## Challenges
- **Code Generation**: Converting the visual pipeline representation into executable code was challenging and required developing a complex recursive algorithm.
- **UI Personalization**: Enhancing the customization options for blocks to improve user interface flexibility remains a challenge.

## Potential with LLMs
While currently not implemented, integrating Large Language Models (LLMs) could further enhance this application by guiding users in the development of the pipeline.



Please, try the app here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mlcreator.streamlit.app/)



