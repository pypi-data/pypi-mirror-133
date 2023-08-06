# FMP Module for Target Prices

from ctypes import Union
import pandas as pd
import numpy as np
from typing import Type, Union

class Target_Price:

    def __init__(self,
                 target_ticker:str,
                 option:str,
                 price:float,
                 price_data:pd.DataFrame = None,
                 target_price:Union[float,str]= None,
                 var_price:float = 10,
                 high_channel:Union[float,str] = None,
                 low_channel:Union[float,str] = None,
                 moving_up_pct:float = None,
                 moving_down_pct:float = None):

        self._price_data = price_data
        self._price = price
        self._target_ticker = target_ticker
        self._option = option
        self._target_price = target_price
        self._var_price = var_price
        self._high_channel = high_channel
        self._low_channel = low_channel
        self._moving_up_pct = moving_up_pct
        self._moving_down_pct = moving_down_pct


    def set_prices(self,price_data):
      self._price_data = price_data

    def get_title(self):

      base = self._target_ticker + ' ' + self._option + ' '

      if self._option == 'Equals' or self._option == 'Greater Than' or self._option == 'Less Than':

        title = base + str(self._target_price)

      elif self._option == 'Inside Channel' or self._option == 'Outside Channel':

        title = base + str(self._low_channel) + ' and ' + str(self._high_channel)

      elif self._option == 'Moving Up %':
        title = base + str(self._moving_up_pct) + '%'

      elif self._option == 'Moving Down %':
        title = base + str(self._moving_down_pct) + '%'
      else:
        title = base

      return title

    
    def set_expired_alert(self):
        self._expired = True

    def reset_expiration(self):
      self._expired = False

    def get_price_df(self) -> pd.Series:

        if isinstance(self._price_data,tuple):
            return self._price_data[0]

        elif isinstance(self._price_data, pd.DataFrame):
            return self._price_data
        else:
            return self._price_data

    def get_target_price(self) -> pd.Series:

        """ 
        Return Target Price Series, if the target price is just a number,
        it will create a pd.Series the size of the given dataframe
        
        """

        price_data = self.get_price_df()

        if isinstance(self._target_price,float):

            tseries = pd.Series([self._target_price] * price_data.shape[0])

            tseries.index = price_data.index

            return tseries

        elif isinstance(self._target_price, pd.Series):

            return self._target_price

        elif isinstance(self._target_price, str):

            nseries = price_data[self._target_price]

            return nseries

        else:

            raise TypeError(f'Target Price must be either a float or a Pandas Series, its a ',type(self._target_price))



    def get_current_price(self) -> float:

        return self.get_price_df()[self._price]

        

    # Options Logic

    
    def equals(self):
        

        current_price = self.get_current_price()

        target_price = self.get_target_price()

        low_range = target_price - self._var_price

        high_range = target_price + self._var_price

        nseries = pd.Series(np.where((current_price <= high_range) & (current_price >= low_range),1,0))
        nseries.index = self.get_price_df().index 

        return nseries

    def greater_less_than(self,option:str = 'Greater Than'):

        current_price = self.get_current_price()

        target_price = self.get_target_price()

        if option == 'Greater Than':

            nseries = pd.Series(np.where(current_price > target_price,1,0))

            nseries.index = self.get_price_df().index

            return nseries
        
        elif option == 'Less Than':


            nseries = pd.Series(np.where(current_price > target_price,0,1))

            nseries.index = self.get_price_df().index

            return nseries

            
        else:
            raise ValueError(f'{option} as an option is  not supported. Must be either Greater Than or Less Than')
        
    def inside_outside_channel(self,option:str = 'Inside Channel'):

        price_df = self.get_price_df()

        if isinstance(self._high_channel,float):

            high_channel = self._high_channel
        
        elif isinstance(self._high_channel, str):

            high_channel = price_df[self._high_channel]

        else:
            raise TypeError('High Channel must be either a col name or a float, its',type(self._high_channel))

        
        if isinstance(self._low_channel,float):


            low_channel = self._low_channel
        elif isinstance(self._low_channel, str):

            low_channel = price_df[self._low_channel]

        else:
            raise TypeError('Low Channel must be either a col name or a float, its', type(self._low_channel))

        
        prices = self.get_current_price()


        if option == 'Inside Channel':

            nseries = pd.Series(np.where((prices <= high_channel) & (prices >= low_channel),1,0))

        elif option == 'Outside Channel':

            nseries = pd.Series(np.where((prices <= high_channel) & (prices >= low_channel),0,1))

        else:
            raise TypeError('Unsupported option, must be either Inside Channel or Outside Channel')

        nseries.index = price_df.index

        return nseries


    def moving_up_down_pct(self,option='Moving Up %'):

        current_price = self.get_current_price()

        target_price = self.get_target_price()

        change = (current_price / target_price - 1) * 100

        prices_df = self.get_price_df()

        if option == 'Moving Up %':

            target_change = self._moving_up_pct

            nseries = pd.Series(np.where(change >= target_change,1,0))

        elif option == 'Moving Down %':

            target_change = self._moving_down_pct

            nseries = pd.Series(np.where(change <= target_change,1,0))

        else:

            raise TypeError('Unsupported option, must be either Moving Up % or Moving Down %')

        nseries.index = prices_df.index

        return nseries

        






    



        
        

    

    
