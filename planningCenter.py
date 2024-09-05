from pypco import PCO
import json
from getConfig import getConfig
preacher =''
def getNames():
        global preacher

        config = getConfig()
	
        pco = PCO(config['PlanningCenterAppID'],config['PlanningCenterAppSecret'])

        service_type_id =  ''

        response = pco.get('https://api.planningcenteronline.com/services/v2/service_types')
        for i in response['data']:
                if i['attributes']['name'] == 'Sabbath Service':
                        service_type_id = i['id']
	
        api = 'https://api.planningcenteronline.com/services/v2/service_types/' + service_type_id + '/plans'
	
        searched_plans = pco.get(api + '?filter=future&per_page=1')
	
        current_plan = pco.get(api + '/' + searched_plans['data'][0]['id'])
	
        sermon_title = current_plan['data']['attributes']['title']

        series = current_plan['data']['attributes']['series_title']

        team_members = pco.get(api + '/' + searched_plans['data'][0]['id'] + '/team_members')
	
	
        for member in team_members['data']:
                if(member['attributes']['team_position_name'] == 'Preacher'):
                        print(member['attributes']['name'] + ' is preaching')
                        preacher = member['attributes']['name']
	
        return(preacher, sermon_title, series)
