# naive
from Analyzer import Analyzer
import time
import pandas as pd
from Custom_Logger import logger
import numpy as np

class Monitor():
    def __init__(self):
        self.analyzer_obj = Analyzer()
        self.monitor_dict = {}

    def continous_monitoring(self):
        # indicates monitoring has started
        logger.info(    {'Component': "Monitor" , "Action": "Started the adaptation effector module" }  ) 
 
        st = time.time()
        while (1):

            # we monitor every 1 second.
            if (time.time() - st > 1):
                try:
                    # retriev the input rate from monitor.csv file
                    df = pd.read_csv('monitor.csv', header=None)
                    array = df.to_numpy()

                    self.monitor_dict["input_rate"] = array[0][0]
                    print("Monitor input rate", self.monitor_dict["input_rate"])

                    # retriev current model from model.csv file
                    df = pd.read_csv('model.csv', header=None)

                    array = df.to_numpy()
                    model_name = array[0][0]
                    self.monitor_dict["model"] = model_name

                    # Read data from data.csv
                    df_data = pd.read_csv('data.csv')
                    latest_data = df_data.iloc[-1].to_dict()  # Get the last row as a dictionary
                    self.monitor_dict.update(latest_data)

                    if (model_name != 'yolov5n' and model_name != 'yolov5s' and model_name != 'yolov5l' and model_name != 'yolov5m' and model_name != 'yolov5x'):
                        continue

                    logger.data(self.monitor_dict)
                    
                    self.analyzer_obj.perform_analysis(self.monitor_dict)
                    st = time.time()

                except Exception as e:
                    logger.error(e)

    def get_current_monitor_data(self):
        # convert numpy.int64 into int for jsonable_encoder to process
        return {key: int(value) if isinstance(value, (np.integer, np.int64)) else value 
                for key, value in self.monitor_dict.items()}


if __name__ == '__main__':
    monitor_obj = Monitor()
    monitor_obj.continous_monitoring()
