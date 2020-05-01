from requests_html import HTMLSession

def get_school_info(school):
	"""
	Web scrapes a school's GreatSchools page.
	school: a dictionary
	"""
	session = HTMLSession()
	r = session.get(school['link'])
	r.html.render()

	ranking = 0
	num_metrics = 0

	# Get Sections
	test_scores = r.html.find('#TestScores', first=True)
	equity = r.html.find('#Equity', first=True)
	students = r.html.find('#Students', first=True)
	teachers = r.html.find('#TeachersStaff', first=True)
	
	# Test Scores
	if test_scores:
		scores = test_scores.find('.score')
		english_prof = percent_check(scores[0].text)
		school['english_prof'] = english_prof
		math_prof = percent_check(scores[1].text)
		school['math_prof'] = math_prof
		test_scores_avg = (english_prof + math_prof) / 2

	# Student Demographics
	if students:

		# Racial Demographics
		demographics = {}
		for demo in students.find('.legend-separator'):
			dblock = demo.find('.legend-title')
			ethnicity = dblock[0].text
			percent = percent_check(dblock[1].text)
			demographics[ethnicity] = percent
		urm_percent = demographics['Hispanic'] + demographics['Black']
		school['hispanic'] = demographics['Hispanic']
		school['black'] = demographics['Black']
		school['urm_percent'] = urm_percent
		ranking += (urm_percent / 100) * 0.35
		num_metrics += 1

		# English Learners
		ell = students.find('#english-learners', first=True)
		if ell:
			ell_percent = percent_check(ell.find('tspan')[0].text)
			school['ell'] = ell_percent
			ranking += (ell_percent / 100) * 0.15
			num_metrics += 1

		# Low-income
		low_income = students.find('#students-participating-in-free-or-reduced-price-lunch-program', first=True)
		if low_income:
			low_income_percent = percent_check(low_income.find('tspan')[0].text)
			school['low_income'] = low_income_percent
			ranking += (low_income_percent / 100) * 0.5
			num_metrics += 1


	# Teachers with 3+ Years Experience
	if teachers:
		teacher_experience = teachers.find('.score')[0].text
		t_exp_percent = percent_check(teacher_experience)

	# Generate ANova Ranking
	school['ranking'] = ranking / num_metrics
	session.close()
	return school

def percent_check(percent):
	value = percent.replace('%', '')
	if '<' in value:
		return 0
	return int(value)
