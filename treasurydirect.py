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

    def _check_type(self, s):
        types = ['Bill', 'Note', 'Bond', 'CMB', 'TIPS', 'FRN']
        if s in types:
            return
        else:
            raise ValueError('Incorrect security tpye format, should be one of Bill, Note, Bond, CMB, TIPS, FRN')

    def _process_request(self, url):
        r = requests.get(url)
        self._raise_status(r)
        try:
            d = r.json()
            return d
        except:
            # No data - Bad Issue Date
            return None


        # http://www.treasurydirect.gov/NP_WS/

    def security_info(self, cusip, issue_date):
        """
        This function returns data about a specific security identified by CUSIP and issue date.
        """
        self._check_cusip(cusip)
        issue_date = self._check_date(issue_date)
        url = self.base_url + self.securities_endpoint + '{}/{}?format=json'.format(cusip, issue_date)
        security_dict = self._process_request(url)
        return security_dict
        # http://www.treasurydirect.gov/TA_WS/securities912796CJ6/02/11/2014?format=json
        # http://www.treasurydirect.gov/TA_WS/securities/912796CJ6/02/11/2014?format=xhtml 

    def announced(self, security_type, days=7 ,pagesize=2, reopening='Yes'):
        """
        This function returns data about announced securities.  
        Max 250 results.  
        Ordered by announcement date (descending), auction date (descending), issue date (descending), security term length (ascending)
        """
        # if any(security_type.lower() in s.lower() for s.lower() in types):
        self._check_type(security_type)
        url = self.base_url + self.securities_endpoint + '/announced?format=json' + '&type={}'.format(security_type) 
        announced_dict = self._process_request(url)
        return announced_dict
        # http://www.treasurydirect.gov/TA_WS/securities/announced?format=html&type=FRN 

if __name__=='__main__':
    td = TreasuryDirect()
    print td.security_info('912796CJ6', '02/11/2014') 
    print td.security_info('912796AW9', datetime.date(2013, 3, 7))
    print td.announced('FRN')