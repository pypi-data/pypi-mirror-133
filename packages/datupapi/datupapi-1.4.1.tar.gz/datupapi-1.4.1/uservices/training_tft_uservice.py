import os
import warnings
import pandas as pd
import featurewiz as FW
import numpy as np
import tensorflow as tf
import tensorboard as tb

import copy
from pathlib import Path
import warnings

import numpy as np
import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping, LearningRateMonitor, ModelCheckpoint
from pytorch_lightning.loggers import TensorBoardLogger
import torch

from pytorch_forecasting import Baseline, TemporalFusionTransformer, TimeSeriesDataSet, DeepAR, NBeats
from pytorch_forecasting.data import GroupNormalizer, EncoderNormalizer
from pytorch_forecasting.metrics import SMAPE, PoissonLoss, QuantileLoss, MASE, MAPE, MAE, NormalDistributionLoss
from pytorch_forecasting.models.temporal_fusion_transformer.tuning import optimize_hyperparameters

import os
import sys
import time
import gc
from tensorflow.keras import backend as K
from dateutil.relativedelta import relativedelta
from datetime import datetime

from datupapi.extract.io import IO
from datupapi.training.tft import Tft

def main():
    DOCKER_CONFIG_PATH = os.path.join('/opt/ml/processing/input', 'config.yml')
    io = IO(config_file=DOCKER_CONFIG_PATH, logfile='data_training', log_path='output/logs')
    trng =  Tft(config_file=DOCKER_CONFIG_PATH, logfile='data_training', log_path='output/logs')

    Qprep = io.download_object_csv(datalake_path=trng.dataset_import_path[0])
    Qprep["timestamp"]=pd.to_datetime(Qprep["timestamp"])
    
    Qprep = trng.fill_dates(Qprep, value=0, method=None)

    frequency=trng.dataset_frequency
    if frequency== "M":
        suffix= "S" if pd.to_datetime(Qprep.timestamp.min()).day==1 else ""
    elif frequency=="W":
        day=Qprep["timestamp"].min().day_name()
        days={"Monday":"-MON", "Tuesday":"-TUE", "Wednesday":"-WED", "Thursday":"-THU", "Friday":"-FRI","Saturday":"-SAT","Sunday":"-SUN"}
        suffix=days[day]

    data_range=pd.date_range(start=Qprep.timestamp.min(), end=Qprep.timestamp.max(), freq=frequency+suffix)

    warnings.filterwarnings("ignore")  # avoid printing out absolute paths
    data1=Qprep.copy()
    data1=data1.sort_values(by=["timestamp","item_id"])
    if frequency=="M":
        data1["time_idx"] = data1["timestamp"].dt.year * 12 + data1["timestamp"].dt.month
        data1["time_idx"] -= data1["time_idx"].min()
    elif frequency=="W":
        data1["time_idx"]=data1.apply(lambda row: trng.date_index_generator(row["timestamp"], data_range), axis=1)
 
    n_features=len(data1.groupby(["item_id","location"]).size()) if trng.use_location else data1.item_id.nunique()
    max_prediction_length = trng.forecast_horizon
    max_encoder_length = trng.input_window

    test_data=pd.DataFrame(np.tile(pd.date_range(start=Qprep.timestamp.max(), periods=max_prediction_length+1, freq=frequency+suffix)[1:], n_features), columns=["timestamp"])
    test_data.insert(0, "time_idx", np.tile(np.arange(data1.time_idx.max()+1,data1.time_idx.max()+1+max_prediction_length), n_features))
    if trng.use_location:
        item_location=data1.groupby(["item_id","location"]).size().reset_index()
        test_data.insert(2, "item_id", np.repeat(item_location.item_id.values ,max_prediction_length ))  
        test_data.insert(3, "location", np.repeat(item_location.location.values ,max_prediction_length ))  
    else:
        test_data.insert(2, "item_id", np.repeat(data1.item_id.unique() ,max_prediction_length ))

    ts_column = 'timestamp'
    test_data["timestamp"]=pd.to_datetime(test_data["timestamp"])
    test_data=test_data.assign(demand=0)
    data1=pd.concat([data1,test_data], axis=0)

    io.datalake="unimilitar-datalake"
    holidays = io.download_object_csv(datalake_path="as-is/opendata/Holidays.csv").loc[:, :"holidays_Colombia"]
    holidays.Date=pd.to_datetime(holidays.Date)
    holidays= holidays.set_index("Date").resample(frequency+suffix).sum().reset_index()
    holidays=holidays.rename(columns={"Date":"timestamp", "holidays_Colombia":"holidays_col"})
    data1=data1.merge(holidays, on="timestamp")
    io = IO(config_file=DOCKER_CONFIG_PATH, logfile='data_training', log_path='output/logs')

    timestamp=data1[["timestamp"]]
    ts_column = 'timestamp'
    data1["Mes"]=pd.to_datetime(data1[ts_column]).dt.month
    data1, ts_adds_in = FW.FE_create_time_series_features(data1, ts_column, ts_adds_in=[])
    data1=data1.drop(columns=["timestamp_month_typeofday_cross","timestamp_typeofday","timestamp_age_in_years","timestamp_month_dayofweek_cross","timestamp_is_warm","timestamp_is_cold","timestamp_is_festive","timestamp_month","timestamp_dayofweek_hour_cross","timestamp_dayofweek"])
    data1["timestamp"]=timestamp

    n_columns=0
    if len(trng.dataset_import_path)==2:
            Qdisc = io.download_object_csv(datalake_path=trng.dataset_import_path[1])
            Qdisc.item_id=Qdisc.item_id.astype("string")
            Qdisc["timestamp"]=pd.to_datetime(Qdisc["timestamp"])
            if trng.use_location:
              Qdisc.location=Qdisc.location.astype("string")
              n_columns=n_columns+len(Qdisc.columns)-3
              data1=pd.merge_ordered(data1, Qdisc, on=["timestamp","item_id", "location"], suffixes=["","-disc"], fill_method=0, how="left" )
            else:
              n_columns=n_columns+len(Qdisc.columns)-2
              data1=pd.merge_ordered(data1,Qdisc, on=["timestamp","item_id"], suffixes=["","-disc"], fill_method=0, how="left")

    if len(trng.dataset_import_path)==3:
            if trng.dataset_import_path[1] !="":
                Qdisc = io.download_object_csv(datalake_path=trng.dataset_import_path[1])
                Qdisc.item_id=Qdisc.item_id.astype("string")
                Qdisc["timestamp"]=pd.to_datetime(Qdisc["timestamp"])
                if trng.use_location:
                  Qdisc.location=Qdisc.location.astype("string")
                  n_columns=n_columns+len(Qdisc.columns)-3
                  data1=pd.merge_ordered(data1, Qdisc, on=["timestamp","item_id", "location"], suffixes=["","-disc"], fill_method=0, how="left")
                else:
                  n_columns=n_columns+len(Qdisc.columns)-2
                  data1=pd.merge_ordered(data1,Qdisc, on=["timestamp","item_id"], suffixes=["","-disc"], fill_method=0, how="left")
            if trng.dataset_import_path[2] !="":
                Qexo = io.download_object_csv(datalake_path=trng.dataset_import_path[2])
                n_columns=n_columns+len(Qexo.columns)-1
                Qexo["timestamp"]=pd.to_datetime(Qexo["timestamp"])
                data1=pd.merge_ordered(data1, Qexo, on=["timestamp"], fill_method=0, how="outer")
    
    data1=data1.fillna(0)
    data1=data1.drop(columns=["timestamp"])
    test_data=data1[data1.time_idx> (data1.time_idx.max()-max_prediction_length-max_encoder_length)]
    data1=data1[data1.time_idx<= (data1.time_idx.max()-max_prediction_length)]

    group_ids=["item_id","location"] if trng.use_location else ["item_id"] 
    unknown=["demand"]
    if n_columns != 0:
        for index in data1.columns[-n_columns:]:
            unknown.append(index)
    known=['time_idx', 'Mes','holidays_col', 'timestamp_quarter',
       'timestamp_is_summer', 'timestamp_is_winter', 'timestamp_year',
       'timestamp_dayofyear', 'timestamp_dayofmonth', 'timestamp_weekofyear'] 
    if frequency=="M":
        known.remove('timestamp_dayofmonth')    


    #Training loop
    tf.io.gfile = tb.compat.tensorflow_stub.io.gfile
    predict={}
    test_predictions={}
    for i in range(0,trng.backtests+1):
        print("Features: ", n_features)
        print("Unknown variables: ")
        print(*unknown, sep = ", ") 
        print("Forecast_horizon: ", max_prediction_length)
        print("Input_window: ", max_encoder_length)
        print("Backtest: ", i)
        training_cutoff = data1["time_idx"].max() - max_prediction_length*i
        training=trng.create_training_dataset(data1=data1, training_cutoff=training_cutoff, group_ids=group_ids,max_encoder_length= max_encoder_length, max_prediction_length=max_prediction_length, unknown= unknown,known=known)
        # create validation set (predict=True) which means to predict the last max_prediction_length points in time
        # for each series
        validation = TimeSeriesDataSet.from_dataset(training, data1[data1.time_idx <= (data1["time_idx"].max() - max_prediction_length*(i-1))], predict=True, stop_randomization=True) if i != 0 else None
        # create dataloaders for model
        train_dataloader = training.to_dataloader(train=True, batch_size=trng.batch_size_tft , num_workers=0)
        val_dataloader = validation.to_dataloader(train=False, batch_size=trng.batch_size_tft*10 , num_workers=0) if i != 0 else None 
        print("Training cutoff: ", training_cutoff)
        #Baseline error
        if i != 0:
            actuals = torch.cat([y for x, (y, weight) in iter(val_dataloader)])
            baseline_predictions = Baseline().predict(val_dataloader)
            print("Baseline error: ",(actuals - baseline_predictions).abs().mean().item())
        for j in range(trng.n_iter_tft):
        # configure network and trainer
            early_stop_callback = EarlyStopping(monitor="val_loss", min_delta=1e-4, patience=10, verbose=False, mode="min") if i != 0 else None
            lr_logger = LearningRateMonitor()  # log the learning rate
            logger = TensorBoardLogger("lightning_logs")  # logging results to a tensorboard
            checkpoint_callback_forecast = ModelCheckpoint(verbose=True, monitor="train_loss", mode="min" )
            checkpoint_callback = ModelCheckpoint(verbose=True, monitor="val_SMAPE", mode="min" )
            callbacks=[lr_logger, checkpoint_callback_forecast] if i == 0 else [lr_logger, early_stop_callback, checkpoint_callback]
            trainer = trng.create_trainer(callbacks, logger)

            #define TFT
            tft= trng.create_tft(training)
            #training
            if i != 0:
                trainer.fit(tft, train_dataloaders=train_dataloader, val_dataloaders=val_dataloader)
            else: 
                trainer.fit(tft, train_dataloaders=train_dataloader)
            best_model_path = trainer.checkpoint_callback.best_model_path
            best_tft = TemporalFusionTransformer.load_from_checkpoint(best_model_path)
            # raw predictions are a dictionary from which all kind of information including quantiles can be extracted
            if i != 0:
                # calcualte mean absolute error on validation set
                actuals = torch.cat([y[0] for x, y in iter(val_dataloader)])
                predictions = best_tft.predict(val_dataloader)
                print("Error: ",(actuals - predictions).abs().mean())
                raw_predictions, x = best_tft.predict(val_dataloader, mode="raw", return_x=True)
                del predictions, actuals
            else:
                raw_predictions, x = best_tft.predict(test_data, mode="raw", return_x=True)
            del x, tft
            aux=pd.DataFrame(raw_predictions.prediction.numpy().reshape(n_features*max_prediction_length , 7))
            a = aux.values
            a.sort(axis=1)  
            a = a[:, ::1]
            aux=pd.DataFrame(a, aux.index, aux.columns)    
            predict[i] = aux if j==0 else predict[i]+aux 

            aux2=best_tft.predict(test_data, mode="raw", return_x=False).prediction
            test_predictions[i] = aux2 if j==0 else test_predictions[i]+aux2 
            del a, aux, raw_predictions, trainer
            gc.collect()
        #Find intervals
        test_predictions[i]=test_predictions[i]/trng.n_iter_tft
        predict[i]=predict[i]/trng.n_iter_tft
        predict[i].columns=["p5","p20","p40","p50","p60","p80","p95"]
        if trng.use_location:
            predict[i].insert(7, "item_id", np.repeat(item_location.item_id.values ,max_prediction_length ))  
            predict[i].insert(8, "location", np.repeat(item_location.location.values ,max_prediction_length )) 
        else: 
            predict[i].insert(7, "item_id", np.repeat(data1.item_id.unique(), max_prediction_length))
        predict[i].insert(8, "time_idx", np.tile(np.arange(data1.time_idx.max()+1-max_prediction_length*i,data1.time_idx.max()+1+max_prediction_length*(1-i)), n_features))
        #predict[i].to_csv("p"+str(i)+".csv")

    predictions=test_predictions[0]
    for i in range(1, trng.backtests+1):
        predictions=predictions+test_predictions[i]
    predictions=predictions/(trng.backtests+1)
    aux=pd.DataFrame(predictions.numpy().reshape(n_features*max_prediction_length , 7))         
    a = aux.values
    a.sort(axis=1)  
    a = a[:, ::1]
    aux=pd.DataFrame(a, aux.index, aux.columns)    
    predict[0]=aux
    
    predict[0].columns=["p5","p20","p40","p50","p60","p80","p95"]
    if trng.use_location:
            predict[0].insert(7, "item_id", np.repeat(item_location.item_id.values ,max_prediction_length ))  
            predict[0].insert(8, "location", np.repeat(item_location.location.values ,max_prediction_length )) 
    else: 
            predict[0].insert(7, "item_id", np.repeat(data1.item_id.unique(), max_prediction_length))
    predict[0].insert(8, "time_idx", np.tile(np.arange(data1.time_idx.max()+1-max_prediction_length*0,data1.time_idx.max()+1+max_prediction_length*(1-0)), n_features))
    #predict[0].to_csv("p"+str(0)+".csv") 

    #predict={}
    #for j in range(trng.backtests+1):
    #    predict[j]=pd.read_csv("p"+str(j)+".csv").iloc[:,1:]
    predict=trng.add_dates(Qprep,data1, predict, suffix)
    predict=trng.clean_negatives(predict)
    forecast=predict[0]
 
    backtest=pd.DataFrame()
    for k in range(trng.backtests):
        backtest=pd.concat([backtest,predict[k+1]])
 
    io.upload_csv(backtest,q_name='forecasted-values', datalake_path=trng.backtest_export_path)
    io.upload_csv(forecast,q_name='forecast', datalake_path=trng.forecast_export_path)    

    io.logger.debug('Data Attup training completed...')
    io.upload_log()
    # Microservice response
    response = {
        'ConfigFileUri': os.path.join('s3://', io.datalake, io.config_path, 'config.yml')
    }
    io.upload_json_file(message=response, json_name='training_response', datalake_path=io.response_path)


if __name__ == '__main__':
    main()
    sys.exit(0)