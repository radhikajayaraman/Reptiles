#!/bin/bash

python <<END

import requests

re=requests.get('$1')

r=re.text

print r 

END

