# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:16:52 2021

@author: lauta
"""

from eod.request_handler_class import RequestHandler

class SplitsDividendsShort(RequestHandler):
    def __init__(self, api_key:str, timeout:int):
        # base URL's of the API
        self.URL_DIVIDENDS = 'https://eodhistoricaldata.com/api/div/'
        self.URL_SPLITS_ = 'https://eodhistoricaldata.com/api/splits/'
        self.URL_SHORT_INTEREST = 'https://eodhistoricaldata.com/api/shorts/'
        super().__init__(api_key, timeout)
        
    def get_dividends(self, symbol:str, **query_params):
        """
        Get dividends for any supported ticker.

        Parameters
        ----------
        symbol : str
            name of the stock to analyse, consists of two parts: {SYMBOL_NAME}.{EXCHANGE_ID}.
        **query_params :
            query parameters.
        
        Returns
        -------
        list
            historical dividends for the selected company.

        """
        self.endpoint = self.URL_DIVIDENDS + symbol.upper()
        return super().handle_request(self.endpoint, query_params)
    
    def get_splits(self, symbol:str, **query_params):
        """
        Get splits for any supported ticker.

        Parameters
        ----------
        symbol : str
            name of the stock to analyse, consists of two parts: {SYMBOL_NAME}.{EXCHANGE_ID}..
        **query_params : TYPE
            query parameters.

        Returns
        -------
        list
            historical splits for the selected company.

        """
        self.endpoint = self.URL_SPLITS_ + symbol.upper()
        return super().handle_request(self.endpoint, query_params)
    
    def get_short_interest(self, symbol:str, **query_params):
        """
        Historical short interest data for major stocks for the Nasdaq exchange.
        Non-US exchanges are not supported at the moment.

        Parameters
        ----------
        symbol : str
            name of the stock to analyse, consists of two parts: {SYMBOL_NAME}.{EXCHANGE_ID}..
        **query_params : TYPE
            query parameters.

        Returns
        -------
        list
            historical short interest for the selected company.

        """
        self.endpoint = self.URL_SHORT_INTEREST + symbol.upper()
        return super().handle_request(self.endpoint, query_params)