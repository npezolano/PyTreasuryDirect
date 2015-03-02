import datetime
import requests

class TDException(Exception):
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return self.error

error_400 = TDException('Bad request')
error_401 = TDException('Unauthorized')
error_404 = TDException('Treasury data not found')
error_429 = TDException('Too many requests')
error_500 = TDException('Internal server error')
error_503 = TDException('Service unavailable')

class TreasuryDirect(object):
    def __init__(self):
        self.base_url = 'http://www.treasurydirect.gov'
        self.securities_endpoint = '/TA_WS/securities/'
        self.debt_endpoint = '/NP_WS/debt/'

    def _raise_status(self, response):
        if response.status_code == 400:
            raise error_400
        elif response.status_code == 401:
            raise error_401
        elif response.status_code == 404:
            raise error_404
        elif response.status_code == 429:
            raise error_429
        elif response.status_code == 500:
            raise error_500
        elif response.status_code == 503:
            raise error_503
        else:
            response.raise_for_status()

    def _check_cusip(self, cusip):
        if len(cusip) != 9:
            raise Exception('CUSIP is not length 9')

    def _check_date(self, date):
        if isinstance(date, str):
            try:
                datetime.datetime.strptime(date, '%m/%d/%Y')
            except ValueError:
                raise ValueError('Incorrect data format, should be MM/DD/YYYY')
            return date
        if isinstance(date, datetime.date):
            return date.strftime('%m/%d/%Y')

        # http://www.treasurydirect.gov/NP_WS/

    def security_info(self, cusip, date):
        self._check_cusip(cusip)
        date = self._check_date(date)
        s = self.base_url + self.securities_endpoint + '{}/{}?format=json'.format(cusip, date)
        r = requests.get(s)
        self._raise_status(r)
        try:
            security_dict = r.json()
            return security_dict
        except:
            # No data
            return None
        # http://www.treasurydirect.gov/TA_WS/securities912796CJ6/02/11/2014?format=json
        # http://www.treasurydirect.gov/TA_WS/securities/912796CJ6/02/11/2014?format=xhtml 

    # def announced(self, tpye, days=7 ,pagesize=2, reopening='Yes'):
        # Bill, Note, Bond, CMB, TIPS, FRN
        # http://www.treasurydirect.gov/TA_WS/securities/announced?format=html&type=FRN 

if __name__=='__main__':
    td = TreasuryDirect()
    # print td.security_info('912796CJ6', '02/11/2014') 
    print td.security_info('912796AW9', datetime.date(2014, 2, 28))