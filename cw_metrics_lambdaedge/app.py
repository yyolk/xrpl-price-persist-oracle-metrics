from base64 import b64encode

import boto3


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
    "title": "XRP/USD Last 3H",
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
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD", { "color": "#cb1fcb" } ]
    ],
    "view": "timeSeries",
    "stacked": false,
    "liveData": true,
    "stat": "Average",
    "period": 900,
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

METRIC_WIDGET_PT7D_LINE = """{
    "metrics": [
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD", { "color": "#d62728" } ]
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
    "title": "XRP/USD Last 7D",
    "width": 800,
    "height": 300,
    "start": "-P7D",
    "end": "P0D",
    "legend": {
        "position": "hidden"
    }
}"""

METRIC_WIDGET_PT1M_LINE = """{
    "metrics": [
        [ "xrpl/mainnet/oracle", "price", "Currency", "USD", { "color": "#9967ee" } ]
    ],
    "view": "timeSeries",
    "stacked": false,
    "liveData": true,
    "stat": "Average",
    "period": 3600,
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
    "title": "XRP/USD Last 30D",
    "legend": {
        "position": "hidden"
    },
    "width": 800,
    "height": 300,
    "start": "-P30D",
    "end": "P0D"
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


cw = boto3.client("cloudwatch", region_name="us-east-1")

definitive_metric_widgets = {
    "3h": METRIC_WIDGET_PT3H_LINE,
    "3h_all": METRIC_WIDGET_PT3H_LINE_ALLNETS,
    "24h": METRIC_WIDGET_PT1D_LINE,
    "1d": METRIC_WIDGET_PT1D_LINE,
    "7d": METRIC_WIDGET_PT7D_LINE,
    "1w": METRIC_WIDGET_PT7D_LINE,
    "30d": METRIC_WIDGET_PT1M_LINE,
    "4w": METRIC_WIDGET_PT1M_LINE,
    "1M": METRIC_WIDGET_PT1M_LINE,
}


def handler(
    event,
    _,  # we don't use the context
):
    # this is an origin-request from lambda@edge
    req_uri = event["Records"][0]["cf"]["request"]["uri"]
    metric_widget = definitive_metric_widgets.get(req_uri.split("/")[1])
    # request a widget not supported, 404
    if metric_widget is None:
        return {
            "status": 404,
            "statusDescription": "Not Found",
        }

    # fetch the metric_widget_image
    metric_widget_resp = cw.get_metric_widget_image(MetricWidget=metric_widget)

    # lambda@edge uses a slightly different return syntax
    return {
        "status": 200,
        "body": b64encode(metric_widget_resp["MetricWidgetImage"]),
        "bodyEncoding": "base64",
        "headers": {
            "content-type": [
                {
                    "value": "image/png",
                }
            ],
            "cache-control": [
                {
                    "value": f"max-age={MAX_AGE}",
                }
            ],
        },
    }
