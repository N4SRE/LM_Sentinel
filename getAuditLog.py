import azloganalytics
import LMUtils
from config import *

# Init logic monitor API class
n4lm = LMUtils.lmAPI(lmCompany, lmID, lmKey)

# Init Azure API class
la = azloganalytics.LogAnalytics(azID, azSecret, azTable)

# Grab last 5 minutes of logs
auditJSON = n4lm.getAuditLog(period=5)

# Identify possible truncation of logs
if len(auditJSON['items']) == 1000:
    print("Maximum length (1000) returned - results truncated")

# Send logs into Azure
for x in auditJSON['items']:
    la.sendtoAzure(x)
