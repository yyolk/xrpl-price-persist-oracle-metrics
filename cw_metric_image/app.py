import os

import boto3


BUCKET = os.environ["S3_BUCKET"]
MAX_AGE = 900  # 5 minutes
METRIC_WIDGET_PT3H_LINE = """\
{
    "metrics": [
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD" ]
    ],
    "view": "timeSeries",
    "stacked": false,
    "liveData": true,
    "stat": "Average",
    "period": 300,
    "yAxis": {
        "right": {
            "label": "",
            "showUnits": false
        },
        "left": {
            "label": "USD"
        }
    },
    "width": 1617,
    "height": 250,
    "start": "-PT3H",
    "end": "P0D"
}
"""

METRIC_WIDGET_NUMBER = """\
{
    "metrics": [
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD" ]
    ],
    "view": "singleValue",
    "stacked": false,
    "region": "us-east-1",
    "liveData": true,
    "stat": "Average",
    "period": 300,
    "yAxis": {
        "right": {
            "label": "",
            "showUnits": false
        },
        "left": {
            "label": "USD"
        }
    },
    "singleValueFullPrecision": true,
    "setPeriodToTimeRange": false,
    "title": "XRP/USD"
}
"""
cw = boto3.client("cloudwatch")
s3 = boto3.resource("s3")

pt3h_line_image = s3.Object(BUCKET, "price_pt3h_line.png")
number_image = s3.Object(BUCKET, "price_number.png")




def handler(event, context):
    metric_widget_pt3h_line_resp = cw.get_metric_widget_image(MetricWidget=METRIC_WIDGET_PT3H_LINE)
    if metric_widget_pt3h_line_resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        pt3h_line_image.put(
            ACL="private",
            Body=metric_widget_pt3h_line_resp["MetricWidgetImage"],
            CacheControl=f"max-age={MAX_AGE}",
            ContentType="image/png",
        )
    else:
        raise Exception("Non-200 Status Code")
    metric_widget_number_resp = cw.get_metric_widget_image(MetricWidget=METRIC_WIDGET_NUMBER)
    if metric_widget_number_resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        number_image.put(
            ACL="private",
            Body=metric_widget_number_resp["MetricWidgetImage"],
            CacheControl=f"max-age={MAX_AGE}",
            ContentType="image/png",
        )
    else:
        raise Exception("Non-200 Status Code")
