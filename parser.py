from requests_html import HTMLSession
from school_parser import *

def form_url(page=1):
	default = prefix + state + city + schools + ms + '&' + hs + '&' + table_view
	if page == 1:
		return default
	else:
		return prefix + state + city + schools + ms + '&' + hs + '&' + table_view + '&' + 'page=' + str(page)

def find_schools(state, city):
	"""
	"""

	# Create an initial request to url
	session = HTMLSession()
	r = session.get(form_url())
	r.html.render()

	# Get all row information for every available page
	schools = {}
	columns = r.html.find('tr')[0]
	while r.html.find('tr') != []:
		rows = r.html.find('tr')
		for i in range(1, len(rows)):
			cells = rows[i].find('td')
			name = cells[0].find('a')[0].text
			link = prefix + cells[0].find('a')[0].attrs['href']
			address = cells[0].find('.address')[0].text
			school_type = cells[1].text
			school_grades = cells[2].text
			total_students = cells[3].text
			student_teacher_ratio = cells[4].text
			district = cells[6].text

			# Create School Object
			school = {}
			school['name'] = name
			school['link'] = link
			school['address'] = address
			school['type'] = school_type
			school['grades'] = school_grades
			school['total_students'] = total_students
			school['student_teacher_ratio'] = student_teacher_ratio
			school['district'] = district
			school = get_school_info(session, school)
			schools[name] = school

		# Render next page of results
		page += 1
		r = session.get(form_url(page))
		r.html.render()
	print(schools)

# Form url to grab list of schools
prefix = 'https://www.greatschools.org/'
state = input("What state would you like to search for schools? : ").lower() + '/'
city = input("What city would you like to search? : ").lower() + '/'
schools = 'schools/?'
ms = 'gradeLevels%5B%5D=m'
hs = 'gradeLevels%5B%5D=h'
table_view = 'view=table'
page = 1
find_schools(state, city)