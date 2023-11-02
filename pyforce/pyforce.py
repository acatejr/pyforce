from simple_salesforce import Salesforce

class Pyforce:


    def __init__(self, *args, **kwargs) -> None:
        """Class initializer.
        If args is supplied then it must b be a config dict object compose whose keys are user, 
        password, security_token, and domain, and corresponding values.
        """
        
        self.sfinstance = None


        if args and len(args) == 1:
            config = args[0]
            values = list(config.values())
            keys = list(config.keys())
            if keys == ["user", "password", "security_token", "domain"] and len(values) > 2 and len(values) < 5:
                self.user = config["user"]
                self.password = config["password"]
                self.token = config["security_token"]
                self.domain = config["domain"]

                sf = Salesforce(
                    password=self.password,
                    username=self.user,
                    security_token=self.token,
                    domain=self.domain
                )

                if sf:
                    self.sfinstance = sf

        elif kwargs:
            pass


    def get_contacts(self, limit=None):
        contacts = []
        
        if limit <= 0:
            return contacts
        
        soql = "SELECT Id, Emplid__c, Name, Email, hed__AlternateEmail__c, hed__Preferred_Email__c, hed__UniversityEmail__c, hed__WorkEmail__c, NetID__c, EDS_Affiliations__c, EDS_Primary_Affiliation__c FROM Contact"

        if limit > 0:
            soql = f"{soql} LIMIT {limit}"
        
        data = self.sfinstance.query_all_iter(soql)
        source = "devint"
        for row in data:
            contact = {
                "source": source,
                "contactid": row["Id"] if row["Id"] is not None else "",
                "emplid": row["Emplid__c"] if row["Emplid__c"] is not None else "",
                "netid": row["NetID__c"] if row["NetID__c"] is not None else "",
                "email": row["Email"] if row["Email"] is not None else "",
                "name": self.clean_contact_name(row["Name"]),
                "alternate_email": row["hed__AlternateEmail__c"] if row["hed__AlternateEmail__c"] is not None else "",
                "work_email": row["hed__WorkEmail__c"] if row["hed__WorkEmail__c"] is not None else "",
                "university_email": row["hed__UniversityEmail__c"] if row["hed__UniversityEmail__c"] is not None else "",
                "preferred_email": row["hed__Preferred_Email__c"] if row["hed__Preferred_Email__c"] is not None else "",
                "eds_affiliations": row["EDS_Affiliations__c"].strip() if row["EDS_Affiliations__c"] is not None else "",
                "eds_primary_affiliation": row["EDS_Primary_Affiliation__c"] if row["EDS_Primary_Affiliation__c"] is not None else ""
            }
            contacts.append(contact)

        return contacts
    

    def clean_contact_name(self, val):
        if val is None or val == "":
            return ""

        return val.encode("utf-8-sig")

