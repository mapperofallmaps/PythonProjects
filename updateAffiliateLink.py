import requests
import sys
import argparse
import re
from queue import Queue
from threading import Thread
from config import hosts, operations, system_codes
from coreapi.request import CoreApiRequest

def main():
    args = parse_command_line_args()

    request = CoreApiRequest(args.env, args.bearer_token)

    unit_distribution_website_configs = get_unit_distribution_website_configs(args.env, args.bearer_token, args.distribution_url)

    counter = 0

    print('The following unit distribution website configs matching affiliate name "{}" and site "{}" have been updated:'.format(args.affiliate_name, args.site))

    for entry in unit_distribution_website_configs:
        result = re.search(args.from_link, entry['partnerPdpUrlFormat'])
        if result:
            if args.affiliate_name in {str(entry['affiliateName']), '*'} and args.site in str(entry['site']):
                affiliate_name = str(entry['affiliateName'])
                site = str(entry['site'])
                affiliate_id = str(entry['affiliateId'])
                partner_pdp_url_format = entry['partnerPdpUrlFormat'].replace(args.from_link, args.to_link)
                for system_code in system_codes:
                    distribution_url = re.sub('(?<=/distributions/)0000(?=/)', system_code, args.distribution_url)
                    url = distribution_url + '/' + operations['update_affiliate_link'] + f'/?affiliateName={affiliate_name}&site={site}&partnerPdpUrlFormat={partner_pdp_url_format}'
                    response = request.request("post", url, None)
                    if response.status_code == requests.codes.ok:
                        counter += 1
                    if (counter + 1) % 5 == 0:
                        print('Changed partnerPdpUrlFormat from "{}" to "{}"'.format(entry['partnerPdpUrlFormat'], partner_pdp_url_format))




def get_unit_distribution_website_configs(env, bearer_token, distribution_url):
    request = CoreApiRequest(env, bearer_token)
    r = request.request_json('get', distribution_url, None)
    return r['distribution']['unitDistributionWebsiteConfigurations']['unitDistributionWebsiteConfiguration']


def parse_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Dry run only")
    parser.add_argument("env", help="Environment to access")
    parser.add_argument("bearer_token", help="Auth bearer token")
    parser.add_argument("distribution_url")
    parser.add_argument("affiliate_name", help="use '*' to select all")
    parser.add_argument("site")
    parser.add_argument("from_link", help="Current value, use '*'' to select all")
    parser.add_argument("to_link", help="Desired value")

    return parser.parse_args()

if __name__ == '__main__':
    main()

