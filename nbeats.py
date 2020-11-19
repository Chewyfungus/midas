import numpy as np
import pandas as pd
import torch
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_forecasting import TimeSeriesDataSet, NBeats, Baseline
from pytorch_forecasting.data import NaNLabelEncoder
from pytorch_forecasting.metrics import SMAPE
import ta

import time
import bybit
import multiprocessing
import os
import shutil

def net(x, k):
    max_encoder_length = k*10
    max_prediction_length = k

    training_cutoff = x["index"].max() - max_prediction_length

    context_length = max_encoder_length
    prediction_length = max_prediction_length

    training = TimeSeriesDataSet(
        x[lambda x: x.index <= training_cutoff],
        time_idx="index",
        target="price",
        categorical_encoders={"series": NaNLabelEncoder().fit(x.series)},
        group_ids=["series"],
        # only unknown variable is "value" - and N-Beats can also not take any additional variables
        time_varying_unknown_reals=["price"],
        max_encoder_length=context_length,
        max_prediction_length=prediction_length,
    )

    validation = TimeSeriesDataSet.from_dataset(training, x, min_prediction_idx=training_cutoff+1)
    batch_size = 32
    train_dataloader = training.to_dataloader(train=True, batch_size=batch_size, num_workers=0)
    val_dataloader = validation.to_dataloader(train=False, batch_size=batch_size, num_workers=0)

    chkpt_callback = ModelCheckpoint('C:\\Users\\Administrator\\Documents\\Garbage\\chk.ckpt')
    trainer = pl.Trainer(
                        max_epochs=10,
                        gpus=0,
                        gradient_clip_val=0.1,
                        checkpoint_callback=chkpt_callback,


                    )


    net = NBeats.from_dataset(training, stack_types=["trend", "seasonality"], num_blocks=[3, 3], num_block_layers=[3, 3]
                              , dropout = 0.2, sharing=[True, True], expansion_coefficient_lengths=[7,7]
                              , prediction_length = k, context_length=k*10, learning_rate=4e-4,
                              log_interval=10, loss=SMAPE(), widths=[32, 512])

    trainer.fit(
        net, train_dataloader=train_dataloader, val_dataloaders=val_dataloader,
    )

    best_model_path = trainer.checkpoint_callback.best_model_path
    best_model = NBeats.load_from_checkpoint(best_model_path)
    return best_model


def z(k):
    z = pd.read_csv('C:\\Users\\Administrator\\Documents\\nbeat.csv')
    z = z[-80000:]
    del z['Unnamed: 0']

    z['price'] = ta.trend.sma_indicator(z['price'], n=10, fillna=False)
    z = z.dropna()
    z = z.iloc[::10]
    df = pd.DataFrame([z['price'].iloc[-1]] * k)
    df=df.rename(columns = {0:'price'})
    z = z.append(df)
    z['series'] = 1
    z = z.reset_index()
    z['index'] = z.index

    return z

def f(k):
    z = pd.read_csv('C:\\Users\\Administrator\\Documents\\hbeat.csv')
    z = z[-80000:]
    del z['Unnamed: 0']

    z['price'] = ta.trend.sma_indicator(z['price'], n=10, fillna=False)
    z = z.dropna()
    z = z.iloc[::10]
    df = pd.DataFrame([z['price'].iloc[-1]] * k)
    df=df.rename(columns = {0:'price'})
    z = z.append(df)
    z['series'] = 1
    z = z.reset_index()
    z['index'] = z.index

    return z

def prediction(best_model, x, k):
    pre = best_model.predict(x, mode="prediction", return_x=True)
    i = 0
    while i < k:
        pred = pd.DataFrame({'price': [float(pre[0][0][i])]})

        if i == 0:
            future = pred

        else:
            future = future.append(pred)

        i += 1

    dir = 'C:\\Users\\Administrator\\Documents\\Garbage'
    if os.path.exists(dir):
        shutil.rmtree(dir)

    dir = 'C:\\Users\\Administrator\\PycharmProjects\\BHAT\\lightning_logs'
    if os.path.exists(dir):
        shutil.rmtree(dir)


    return future


def barketbaker():

    h = 0
    v = 0
    while h < 300:
        s = 0
        k = 20


        if v <= h:

            u = z(k)
            best_model = net(u, k)
            v += 30

        h += 1

        client = bybit.bybit(test=False, api_key="SCviN7OuJAu6bwDCoQ", api_secret="HUHfyryjb4oWw7soBgp1ajZV4IGQq5Zvhywi")
        sym = (client.Market.Market_symbolInfo(symbol="BTCUSD").result())
        bid = float(sym[0]["result"][0]["bid_price"])
        ask = float(sym[0]["result"][0]["ask_price"])

        pos = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
        side = str(pos[0]["result"]["side"])
        size = float(pos[0]["result"]["size"])

        active = client.Order.Order_getOrders(symbol="BTCUSD").result()
        lastorder = active[0]["result"]["data"][0]["order_status"]
        orderid = active[0]["result"]["data"][0]["order_id"]

        lastorder2 = active[0]["result"]["data"][1]["order_status"]
        orderid2 = active[0]["result"]["data"][1]["order_id"]

        print(side, size, lastorder)

        price = (bid + ask) / 2

        x = z(k)
        print("pre")
        future = prediction(best_model, x, k)
        print("post")


        meanl = future['price'].mean()
        maxl = int(future['price'].max())
        minl = int(future['price'].min())

        if lastorder != "Filled":
            client.Order.Order_cancel(symbol="BTCUSD", order_id=orderid).result()

        if lastorder2 != "Filled":
            client.Order.Order_cancel(symbol="BTCUSD", order_id=orderid2).result()

        if size > 0:
            q = size

        if size == 0:
            q = 420

            if (minl > price):
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q*5, price=bid,
                                       time_in_force="PostOnly").result()

            else:
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl + 5,
                                       time_in_force="PostOnly").result()

                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 15,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 35,
                                       time_in_force="PostOnly").result()

            if (maxl < price):
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q*5, price=ask,
                                       time_in_force="PostOnly").result()

            else:
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl - 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 15,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 35,
                                       time_in_force="PostOnly").result()

        elif size > 0 and side == "Sell" and ((future['price'].iloc[-1] > minl + 0.25*(maxl - minl)) or (minl > price)):

            if (minl > price):
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q*5, price=bid,
                                       time_in_force="PostOnly").result()

            else:
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl + 5,
                                       time_in_force="PostOnly").result()

                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 15,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Buy", symbol="BTCUSD", order_type="Limit", qty=q, price=minl - 35,
                                       time_in_force="PostOnly").result()

        elif size > 0 and side == "Buy" and ((future['price'].iloc[-1] < maxl - 0.75*(maxl - minl)) or (maxl < price)):

            if (maxl < price):
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q*5, price=ask, time_in_force="PostOnly").result()

            else:
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl - 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 5,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 15,
                                       time_in_force="PostOnly").result()
                client.Order.Order_new(side="Sell", symbol="BTCUSD", order_type="Limit", qty=q, price=maxl + 35,
                                       time_in_force="PostOnly").result()

        else:
            print("pass")




        print(x['price'].iloc[-1], meanl, maxl, minl)

        while s < 600:
            s += 1
            time.sleep(1)



if __name__ == "__main__":

    t = 0

    while(True):


        print("helo")

        bhat = multiprocessing.Process(target=barketbaker)
        bhat.start()
        bhat.join()
        bhat.terminate()