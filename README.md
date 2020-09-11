# ec2-snapshot-cleanup
A simple Python script to delete old EBS snapshots in bulk from your AWS account

Tested with Python 3.7.7

## Setup
Just clone this repo, then run the following command

```
pip install -r requirements.txt
```

Then open the ec2-snapshot-cleanup.py in a code/text editor and set the following variables to appropriate values:
* DRYRUN
* PROFILE_NAME
* REGION
* MAX_DAYS_TO_RETAIN

**CAUTION** - if you set DRYRUN to `True`, the script will delete old snapshots that are older than `MAX_DAYS_TO_RETAIN` days old. This is a **NON-REVERSIBLE** operation.

After you've configured the above variables, you can run the following command to perform the cleanup.

```
python ec2-snapshot-cleanup.py
```

