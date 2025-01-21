# EthiMart: Amharic NER System

## Project Setup
1. Clone the repository.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Initialize DVC:
    ```bash
    dvc init
    ```

## Project Overview
EthiMart aims to centralize e-commerce data from Telegram channels using an Amharic NER system.

## Folder Structure
```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── unittests.yml
├── .dvc/
├── data/
│   ├── preprocessed/
│   └── raw/
├── .gitignore
├── requirements.txt
├── README.md
├── dvc.yml
├── src/
│   └── __init__.py
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   └── __init__.py
└── scripts/
     ├── __init__.py
     └── README.md
```