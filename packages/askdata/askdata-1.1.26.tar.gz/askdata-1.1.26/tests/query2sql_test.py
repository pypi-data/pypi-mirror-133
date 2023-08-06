from askdata import query2sql


if __name__ == "__main__":
    smartquery = '{"queries":[{"id":"q0","fields":[{"column":"DENOMINAZIONE_REGIONE","alias":"Denominazione regione","aggregation":null,"dataset":"f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-34b83631-1108-41c3-870f-cee0636c58c7","internalDataType":"STRING","expression":false},{"column":"TOTALE_CASI","alias":"Totale casi","aggregation":"SUM","dataset":"f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-34b83631-1108-41c3-870f-cee0636c58c7","internalDataType":"NUMERIC","expression":false}],"datasets":[{"dataset":"f2c705dd-f63f-475b-95a9-c1ad20f33716-MYSQL-34b83631-1108-41c3-870f-cee0636c58c7"}],"relationships":null,"where":[],"orderBy":[{"field":"TOTALE_CASI","order":"ASC"}],"limit":3,"offset":null,"joinedSmartQuery":null,"pivot":null,"pivotableFields":null,"join":null,"valid":true}]}'
    response = query2sql.query_to_sql(smartquery=smartquery, db_driver="PostgreSQL")
    print(response)
