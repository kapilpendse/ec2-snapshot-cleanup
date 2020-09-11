import boto3
from datetime import datetime
from time import sleep

DRYRUN = True # Set this to False to really delete snapshots
PROFILE_NAME = '' # Set this to your AWS CLI profile name (see ~/.aws/credentials or ~/.aws/config files)
REGION = '' # Set this to the AWS region in which you want to do the cleanup
MAX_DAYS_TO_RETAIN = 60 # Set this to the age (in days) of the oldest snapshot that you want to retain. Snapshots that are older than this many days will be deleted.

session = boto3.session.Session(profile_name=PROFILE_NAME)
client = session.client('ec2', region_name=REGION)

snapshots = client.describe_snapshots(OwnerIds=['self'])

snapshots_deleted = 0
snapshots_retained = 0
today = datetime.today()
for snapshot in snapshots['Snapshots']:
    difference = today - snapshot['StartTime'].replace(tzinfo=None)
    if difference.days > MAX_DAYS_TO_RETAIN:
        print("deleting this snapshot: {} - {}".format(difference.days, snapshot['SnapshotId']))
        snapshots_deleted = snapshots_deleted + 1
        try:
            sleep(0.005) # in order to avoid AWS API rate limiting exception
            client.delete_snapshot(SnapshotId=snapshot['SnapshotId'], DryRun=DRYRUN)
        except Exception as e:
            print("{}".format(str(e)))
            break
    else:
        print("retaining this snapshot: {} - {}".format(difference.days, snapshot['SnapshotId']))
        snapshots_retained = snapshots_retained + 1

print("Total snapshots: {}".format(len(snapshots['Snapshots'])))
print("Snapshots deleted: {}".format(snapshots_deleted))
print("Snapshots preserved: {}".format(snapshots_retained))

