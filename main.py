import os
import click
from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()

sf_user = os.environ.get('SF_USER')
sf_pass = os.environ.get('SF_PASS')
sf_access_token = os.environ.get('SF_ACCESS_TOKEN')
sf_domain = os.environ.get('SF_DOMAIN')

 
def sf_instance(user, password, token, domain):
    """Creates a saleforce connection instance.

    Args:
        user (str): The Salesforce user id
        password (str): The Salesforce user password
        token (str): The Salesforce authentication token
        domain(str): The salesforce domain name (instance)

    Returns:
        sf (obj): The salelsforce connection instance.
    """

    sf = Salesforce(
        password=password,
        username=user,
        security_token=token,
        domain=domain
    )

    return sf


@click.group(help="Salesforce tools.")
def cli():
    pass


@click.command(help="Executes a raw SOQL query")
@click.option("--soql", help="Run SOQL query")
def query(soql):

    if soql and len(soql):     
        sf = sf_instance(user=sf_user, password=sf_pass, token=sf_access_token, domain=sf_domain)
        fields = soql[soql.index("Select ") + len("Select "):soql.index(" From")]
        fields = fields.replace(" ","").split(",")
        data = sf.query_all(soql)
        
        print(f'"{fields[0]}"')
        if data and data['totalSize'] > 0:
            records = data["records"]        
            for record in records:
                values = []
                for f in fields:
                    values.append(f'"{record[f]}"')
                
                print(",".join(v for v in values))
    
        sf = None

# @click.command(help="Delete a campaign's member accounts.")
# @click.option("--campaign_id", help="The campaign id")
# def remove_accounts_from_campaign(campaign_id):
#     if campaign_id:
#         soql = f"Select Contact.Account.Id From CampaignMember Where CampaignId = '{campaign_id}' And Contact.Email Like '%.clm.invalid'"
#         sf = sf_instance(user=sf_user, password=sf_pass, token=sf_access_token, domain=sf_domain)    
#         accounts = sf.query_all(soql)
#         data = []
#         if accounts and len(accounts) and accounts["totalSize"] > 0:
#             records = accounts["records"]
#             for record in records:
#                 account_id = record["Contact"]["Account"]["Id"]
#                 data.append({"Id": account_id})
        
#         if data and len(data):
#             sf.bulk.Account.delete(data=data, batch_size=10000)
#             # resp = sf.bulk.Account.delete(data=data, batch_size=10000, use_serial=True)
            
#         sf = None


@click.command(help="Delete all instances of a Salesforce object for the supplied object id(s)")
@click.option("--sfobj", help="The Salesforce object name")
@click.option("--fname", help="The input csv file name")
def bulk_delete(sfobj, fname):
    
    data = []
    
    with open(fname) as infile:
        cnt = 0
        for line in infile:            
            if cnt > 0:
                id = line.replace('"', "").strip("\n")
                data.append({"Id": id})
            cnt += 1
    
    if data and len(data):
        sf = sf_instance(user=sf_user, password=sf_pass, token=sf_access_token, domain=sf_domain)
        sf_cmd = f'sf.bulk.{sfobj}.delete(data=data, batch_size=10000)'
        eval(sf_cmd)
        sf = None


if __name__ == "__main__":
    cli.add_command(query)
    # cli.add_command(remove_accounts_from_campaign)
    cli.add_command(bulk_delete)
    cli()    
