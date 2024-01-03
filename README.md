# Flask PDF Text Extraction and Query App (ScanFlow)

This Flask application allows users to upload PDF files, extract text from them, store the text in an Astra database, and query the database for answers using OpenAI's language model.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Uploading a File](#uploading-a-file)
  - [Querying](#querying)
- [Additional Information](#additional-information)
- [License](#license)

## Overview

The application uses Flask for the web framework, Astra DB for data storage, and OpenAI's language model for querying. It allows users to upload PDF files, extracts text from them, and stores the text in an Astra database. Users can then query the database for answers using the OpenAI language model.

## Prerequisites

Before running the application, ensure you have the following prerequisites:

- Python 3.x
- Flask
- Astra DB account and credentials
- OpenAI API key

