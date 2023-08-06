import requests


def fetch_aws_cdk_latest_version():
    json_body = fetch_aws_cdk_all_releases()
    all_releases = sorted([j['name'] for j in json_body], reverse=True)

    latest_version = all_releases[0]

    print(latest_version)

    return latest_version


def fetch_aws_cdk_all_releases():
    headers = {
        'User-Agent': 'MorningCode-AWS-CDK-UPDATE-CHECKER',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
    }
    r = requests.get(get_aws_cdk_url(), headers=headers)

    if r.status_code != 200:
        raise RuntimeError(
            '[' + str(r.status_code) + '] ' +
            r'could not fetch releases from github...please try again later!'
        )

    return r.json()


def get_aws_cdk_url():
    return 'https://api.github.com/repos/aws/aws-cdk/releases'
