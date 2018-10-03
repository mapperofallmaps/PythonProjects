import requests
import sys
import argparse
import re
from queue import Queue
from threading import Thread

# Currently this script adds a extra dash '-' to the front of the Partner pdp url
# Remove it in line 80 if you do not need it

api_endpoints = {
    'test': [
        'http://api-test.homeaway.com/distributions/0000/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-test.homeaway.com/distributions/0001/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-test.homeaway.com/distributions/0002/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-test.homeaway.com/distributions/0003/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-test.homeaway.com/distributions/0004/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
    ],
    'stage': [
        'http://api-stage.homeaway.com/distributions/0000/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-stage.homeaway.com/distributions/0001/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-stage.homeaway.com/distributions/0002/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-stage.homeaway.com/distributions/0003/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api-stage.homeaway.com/distributions/0004/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
    ],
    'prod': [
        'http://api.homeaway.com/distributions/0000/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api.homeaway.com/distributions/0001/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api.homeaway.com/distributions/0002/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api.homeaway.com/distributions/0003/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
        'http://api.homeaway.com/distributions/0004/{distribution_uuid}/addUnitDistributionWebsiteConfiguration',
    ]
}


class AddUnitDistributionWebsiteConfigWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            url, headers, body = self.queue.get()
            response = requests.request("POST", url, headers=headers, data=body)
            if response.status_code == requests.codes.ok:
                print('Successfully configured a new unit distribution website config')
            self.queue.task_done()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Dry run only")
    parser.add_argument("env", help="Environment to access")
    parser.add_argument("distribution_uuid", help="UUID for Distribution")
    parser.add_argument("bearerToken", help="Auth Bearer token")
    parser.add_argument("affiliate_name", help="Affiliate Name")
    parser.add_argument("partner_pdp_url_format", help="PDP URL")
    parser.add_argument("site", help="Site Name")

    args = parser.parse_args()

    if args.dry_run:
        print('*** DRY RUN ONLY ***')

    # Check connectivity to servers
    # try:
    #     [requests.get('http://api-test.homeaway.com/distributions/0000/' + args.distribution_uuid)]
    # except:
    #     sys.exit('Failed to connect to HomeAway API ' + args.env + 'servers')

    headers = {
        'X-HomeAway-ApiVersion': "*",
        'Authorization': f"Bearer {args.bearerToken}",
        'Content-Type': 'application/xml'
    }

    body = '<unitDistributionWebsiteConfiguration xmlns="http://api.homeaway.com/domain/v0">' \
        f'<affiliateId>0</affiliateId>' \
        f'<affiliateName>{args.affiliate_name}</affiliateName>' \
        f'<partnerPdpUrlFormat>-{args.partner_pdp_url_format}</partnerPdpUrlFormat>' \
        f'<site>{args.site}</site>' \
        '</unitDistributionWebsiteConfiguration>'

    queue = Queue()

    for count in range(8):
        worker = AddUnitDistributionWebsiteConfigWorker(queue)
        worker.daemon = True
        worker.start()

    for entry in api_endpoints[args.env]:
        url = re.sub('{distribution_uuid}', args.distribution_uuid, entry)

        queue.put((url, headers, body))

    queue.join()


if __name__ == "__main__":
    main()
