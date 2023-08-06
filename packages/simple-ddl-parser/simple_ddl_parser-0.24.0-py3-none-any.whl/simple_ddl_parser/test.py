from simple_ddl_parser import DDLParser

ddl =  """

        CREATE TABLE "material_attachments"
"""
result = DDLParser(ddl).run(group_by_type=True, output_mode="hql")
import pprint

pprint.pprint(result)
