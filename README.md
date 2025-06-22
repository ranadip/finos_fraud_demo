# Running the Application

This document outlines the steps to run the FastAPI service and the Streamlit application.

## 1. Start the FastAPI Service

To start the FastAPI service, navigate to the project directory and run the following command:

```bash
uvicorn runner:app --port 8601
```

This will start the service on the default port (usually 8000). You can access the API endpoints at `http://localhost:8601`.

**Optional: Hot Reload Mode**

For development purposes, you can enable hot reload mode, which automatically restarts the server when you make changes to the code. To do this, use the following command:

```bash
uvicorn runner:app --reload --port 8601
```

## 2. Start the Streamlit Application

To start the Streamlit application, run the following command:

```bash
streamlit run demo-ui.py
```

This will open the application in your web browser.

## Debug Mode in `runner.py`

To control the amount of logging information printed to the FastAPI console, you can modify the debug mode in the `runner.py` file.  Look for the line where debug mode is set (e.g., `debug = True` or `debug = False`) and change the value accordingly.  `debug = True` will print more detailed logs, while `debug = False` will reduce the amount of output.