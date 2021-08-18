import os

import boto3


BUCKET = os.environ["S3_BUCKET"]
MAX_AGE = 300  # 5 minutes
METRIC_WIDGET_PT3H_LINE = """{
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
            "label": "USD",
            "showUnits": false
        }
    },
    "title": "XRP/USD Last 3H",
    "width": 800,
    "height": 300,
    "start": "-PT3H",
    "end": "P0D",
    "legend": {
        "position": "hidden"
    }
}"""

METRIC_WIDGET_PT3H_LINE_ALLNETS = """{
    "metrics": [
        [ "xrpl/testnet/oracle", "price", "Currency", "USD", { "color": "#7f7f7f" } ],
        [ "xrpl/mainnet/oracle", ".", ".", ".", { "color": "#1f77b4" } ]
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
            "label": "USD",
            "showUnits": false
        }
    },
    "singleValueFullPrecision": true,
    "setPeriodToTimeRange": false,
    "title": "XRP/USD Last3H",
    "legend": {
        "position": "bottom"
    },
    "width": 800,
    "height": 300,
    "start": "-PT3H",
    "end": "P0D"
}"""

METRIC_WIDGET_PT1D_LINE = """{
    "metrics": [
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD", { "color": "#CB1FCB" } ]
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
            "label": "USD",
            "showUnits": false
        }
    },
    "title": "XRP/USD Last 24H",
    "width": 800,
    "height": 300,
    "start": "-P1D",
    "end": "P0D",
    "legend": {
        "position": "hidden"
    }
}"""
# Unfortunately 'number'/'singleValue' is not yet a supported widget image output
# type, this will result in a default widget returned
# METRIC_WIDGET_NUMBER = """{
#     "view": "singleValue",
#     "stacked": false,
#     "liveData": true,
#     "stat": "Average",
#     "period": 300,
#     "singleValueFullPrecision": true,
#     "setPeriodToTimeRange": false,
#     "title": "XRP/USD",
#     "metrics": [
#         [ "xrpl/testnet/oracle", "price", "Currency", "USD" ]
#     ],
#     "width": 1617,
#     "height": 250,
#     "start": "-PT3H",
#     "end": "P0D"
# }
# """
cw = boto3.client("cloudwatch")
s3 = boto3.resource("s3")

pt3h_line_image = s3.Object(BUCKET, "price_pt3h_line.png")
pt3h_line_image_allnets = s3.Object(BUCKET, "price_pt3h_line_allnets.png")
pt1d_line_image = s3.Object(BUCKET, "price_pt1d_line.png")
# number_image = s3.Object(BUCKET, "price_number.png")




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
    metric_widget_pt3h_line_allnets_resp = cw.get_metric_widget_image(MetricWidget=METRIC_WIDGET_PT3H_LINE_ALLNETS)
    if metric_widget_pt3h_line_allnets_resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        pt3h_line_image_allnets.put(
            ACL="private",
            Body=metric_widget_pt3h_line_allnets_resp["MetricWidgetImage"],
            CacheControl=f"max-age={MAX_AGE}",
            ContentType="image/png",
        )
    else:
        raise Exception("Non-200 Status Code")
    metric_widget_pt1d_line_resp = cw.get_metric_widget_image(MetricWidget=METRIC_WIDGET_PT1D_LINE)
    if metric_widget_pt1d_line_resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        pt1d_line_image.put(
            ACL="private",
            Body=metric_widget_pt1d_line_resp["MetricWidgetImage"],
            CacheControl=f"max-age={MAX_AGE}",
            ContentType="image/png",
        )
    else:
        raise Exception("Non-200 Status Code")
