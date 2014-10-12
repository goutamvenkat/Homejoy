from pyramid.view import view_config
from shapely.geometry import Polygon, Point, LineString
import fiona

@view_config(route_name='home',
			 renderer='zip_code_template.html')
def my_view(request):
	start_lat, start_long = [request.matchdict['lat1'], request.matchdict['long1']]
	end_lat, end_long = [request.matchdict['lat2'], request.matchdict['long2']]

	start_lat = float(start_lat)
	start_long = float(start_long)
	end_lat = float(end_lat)
	end_long = float(end_long)
	zip_codes = []
	required_polygon = []
	with fiona.open('myproject/tl_2014_us_zcta510.shp', 'r') as f:
		for line in f:
			zip_code = int(line['properties']['ZCTA5CE10'])
			if zip_code > 90000 and zip_code < 96163: # check for California
				if line['geometry']['type'] == 'Polygon':
					polygon = line['geometry']['coordinates']
					s = Polygon(polygon[0])
					linestr = LineString([(start_long, start_lat), (end_long, end_lat)])
					if linestr.intersects(s):
						zip_codes.append(zip_code)
						required_polygon.append(polygon[0])

				else:
					multi_polygon = line['geometry']['coordinates']
					for polygon in multi_polygon:
						s = Polygon(polygon[0])
						linestr = LineString([(start_long, start_lat), (end_long, end_lat)])

						if linestr.intersects(s):
							zip_codes.append(zip_code)
							required_polygon.append(polygon[0])

	return dict(zip_codes=zip_codes, required_polygon=required_polygon)


