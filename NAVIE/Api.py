from fastapi import FastAPI, HTTPException
from monitor import Monitor
from Execute import Executor
import pandas as pd
import uvicorn
import threading
import json
import os


app = FastAPI()
monitor = Monitor()
executor = Executor()

# run continous_monitoring in a different thread to get data
monitor_thread = threading.Thread(target=monitor.continous_monitoring, daemon=True)
monitor_thread.start()

def load_schema(schema_name):
    schema_folder = "schemas"
    schema_path = os.path.join(schema_folder, schema_name)
    
    with open(schema_path, "r") as schema_file:
        return json.load(schema_file)

@app.get("/monitor")
def get_monitor_data():
    try:
        data = monitor.get_current_monitor_data()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/monitor_schema")
def get_monitor_schema():
    schema = load_schema("monitor_schema.json")
    return schema


def load_adaptation_options():
    df = pd.read_csv('knowledge.csv', header=None)
    options = {
        "yolov5n_rate_min": float(df.iloc[0, 1]),
        "yolov5n_rate_max": float(df.iloc[0, 2]),
        "yolov5s_rate_min": float(df.iloc[1, 1]),
        "yolov5s_rate_max": float(df.iloc[1, 2]),
        "yolov5m_rate_min": float(df.iloc[2, 1]),
        "yolov5m_rate_max": float(df.iloc[2, 2]),
        "yolov5l_rate_min": float(df.iloc[3, 1]),
        "yolov5l_rate_max": float(df.iloc[3, 2]),
        "yolov5x_rate_min": float(df.iloc[4, 1]),
        "yolov5x_rate_max": float(df.iloc[4, 2]),
    }
    return options


@app.get("/adaptation_options")
def get_adaptation_options():
    try:
        options = load_adaptation_options()
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load adaptation options: {e}")


@app.get("/adaptation_options_schema")
def get_adaptation_options_schema():
    schema = load_schema("adaptation_options_schema.json")
    return schema


@app.get("/execute_schema")
def get_execute_schema():
    schema = load_schema("execute_schema.json")
    return schema


@app.put("/execute")
def execute_action(option: str, new_value: float):
    try:
        df = pd.read_csv('knowledge.csv', header=None)
        option_map = {
            "yolov5n_rate_min": (0, 1), "yolov5n_rate_max": (0, 2),
            "yolov5s_rate_min": (1, 1), "yolov5s_rate_max": (1, 2),
            "yolov5m_rate_min": (2, 1), "yolov5m_rate_max": (2, 2),
            "yolov5l_rate_min": (3, 1), "yolov5l_rate_max": (3, 2),
            "yolov5x_rate_min": (4, 1), "yolov5x_rate_max": (4, 2)
        }
        
        if option not in option_map:
            raise HTTPException(status_code=400, detail="Invalid adaptation option")
        
        row, col = option_map[option]
        df.iat[row, col] = new_value
        df.to_csv('knowledge.csv', header=None, index=False)
        
        return {"message": f"Adaptation option '{option}' updated to {new_value}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute adaptation action: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
