import argparse
import yaml
from src.utils import upload_to_s3, process_task, gcp

args = argparse.ArgumentParser(
    description="Provies some inforamtion on the job to process"
)
args.add_argument(
    "-t", "--task", type=str, required=True,
    help="This will point to a task location into the config.yaml file.\
        Then it will follow the step of this specific task.")
args = args.parse_args()

with open("./config/config.yml", 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

config_export = config[args.task]["export"]

if config_export[0]["export"]["host"] == 's3':
    upload_to_s3(process_task(args.task), config_export[0]["export"]["bucket"], config_export[0]["export"]["filename"])
elif config_export[0]["export"]["host"] == 'gsheet':
    gcp(spreadsheet_id = config_export[0]["export"]["spread_sheet_id"], 
                           df = process_task(args.task),
                           worksheet_name = config_export[0]["export"]["worksheet_name"])
  