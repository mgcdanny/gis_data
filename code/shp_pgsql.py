import os
import fnmatch

matches = []
for root, dirs, files, in os.walk("."):
	for filename in fnmatch.filter(files, "*.shp"):
		temp = {"path": os.path.join(root, filename), 
				"table_name":filename.split(".")[0]}
		matches.append(temp)

for match in matches:
	try:
		os.system("""psql -d nyc_gis_db -c "DROP TABLE IF EXISTS nyc_gis_schema.{table_name}" """.format(table_name = match["table_name"]))
		cmd = """shp2pgsql -s 2263 {path} nyc_gis_schema.{table_name} | psql -q -d nyc_gis_db """
		doit = cmd.format(**match)
		os.system(doit)
	except Exception, e:
		print(e)
		pass

