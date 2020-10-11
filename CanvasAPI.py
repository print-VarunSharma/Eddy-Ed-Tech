import requests
import pprint



'''

Student Class: 
    Instance of class, created from an Auth_Token specifically Bearer Token 

    Will up front request for information initially to create a "profile"

    Profile will generate attributes for the instance as seen below

        - Courses
            - Assignments for each course
            - Quizes for Courses
        - Announcements 
        - Notifications 
        
'''



'''
For paginated responses

while r.links['current']['url'] != r.links['last']['url']:  
              r = requests.get(r.links['next']['url'], headers=header)  
              page_response = r.json()  
              for p_response in page_response:  
                     assignments_found_thus_far.append(p_response)

'''


def create_request_URL(init, resource_ep = [] , params = None):
    ret = init
    for r in resource_ep:
        assert(type(r) == type(""))
        ret += '/'
        ret += r
    if params:
        assert (type(params) == type(dict()))
        ret += "?"
        for p in params:
            assert(type(p) == type(""))
            assert(type(params[p]) == type(""))
            ret += p
            ret += "="
            ret += params[p]
            ret += "&"
        ret = ret[:-1]
    return ret


class Student():
    gateway = "https://canvas.ubc.ca/api/v1"
    init_self_gateway = "{}/users/self".format(gateway)
    
    def __init__(self,bearer_token):
        assert(type(bearer_token) == type(""))
        self.courses = {}
        self.bearer_token = bearer_token
        self.pp = pprint.PrettyPrinter(indent=4)
        self.auth_header ={
            'Authorization': 'Bearer {}'.format(self.bearer_token),
        }
        json_profile = requests.request("GET", self.init_self_gateway, headers = self.auth_header).json()
        self.id = json_profile["id"]
        self.name = json_profile["name"]

        self.extra_links = {}

        self.get_courses()


    def add_extra_link(self, short_hand, link):
        self.extra_links[short_hand] = link
    def remove_extra_link(self, short_hand):
        if short_hand not in self.extra_links.keys():
            print("short hand of extra link not in profile")
            return 
        self.extra_links.pop(short_hand)


    # will retrieve the 
    def get_courses(self, enrollment_type = "student", enrollment_state = "active"):
        params = {"enrollment_type": "student",
                    "enrollment_state" : "active"
        }
        url = create_request_URL(init = self.gateway, resource_ep = ["courses"], params = params)
        payload  = {}
        response = requests.request("GET", url, headers=self.auth_header, data = payload)
        courses = response.json()
        for c in courses:
            Course_obj = Course(c, self.bearer_token)
            self.courses[Course_obj.course_code] = Course_obj
    
    # on all registerd courses for this student
        # retrieve upcoming assignemnts 
    def update_assignments(self):
        for c in self.courses:
            Course_obj = self.courses[c]
            Course_obj.update_assignments()
    
    
    def remove_course(self, course_code):
        if course_code not in self.courses.keys():
            print("course_code not in courses")
            return 
        self.courses.pop(course_code)

    def get_account_notifications(self):
        r_ep = ["accounts", "self", "account_notifications"]
        url = create_request_URL(init = self.gateway, resource_ep = r_ep)
        response = requests.request("GET", url, headers=self.auth_header)
        r_ep = ["accounts" "self", "account_notifications"]
        if response.status_code == 200:
           modules = response.json()
           return modules
        else:
            print(response.status_code)


class Course():
# single Course used within a Courses obj
        # course_code e.g. "CPSC 320 101/102 2020W"
        # calendar -> dictionary
            # e.g. 
            # calendar": {
                        #     "ics": "https://canvas.ubc.ca/feeds/calendars/course_hp0YU0SjrBMJgSWheRFlUCKJjUsMqK1IrtQtfEug.ics"
                            # } 
        # id, specific to access api resources related to particular course
        # name (full name) e.g. "CPSC 320 101/102 2020W Intermediate Algorithm Design and Analysis"

    gateway = "https://canvas.ubc.ca/api/v1/courses"

    def __init__(self, Course, bearer_token):
        keys = ["course_code", "calendar", "id", "name"]
        values = []
        self.bearer_token = bearer_token
        for k in keys:
            values.append(Course[k])
        self.course_code = values[0] 
        self.calendar = values[1] 
        self.id = values[2]
        self.name = values[3] # verbose
        self.assignments = []
        self.resource_ep = [str(self.id)]
        self.auth_headers = {
        'Authorization': 'Bearer {}'.format(self.bearer_token),
        }
        
        # extra_links
        self.extra_links = {}
        self.update_assignments()


    # assumed course_code is <COURSE LETTER> <COURSE NUM>
    # not neccessarily the case for non UBC courses, quite niave
    def get_pretty_name(self):
        x = self.course_code.split()
        return (x[0], x[1])

     # kind of a throw up method 
    def update_assignments(self):
        response = self.get_assignments()
        raw = response.json()

        if response.status_code == 200:
            self.assignments = []
            for a in raw:
                ass = Assignments(a, self.bearer_token)
                self.assignments.append(ass)
            while response.links['current']['url'] != response.links['last']['url']:
                response = requests.request("GET", response.links["next"]["url"], headers=self.auth_headers)
                raw = response.json()
                for a in raw:
                    ass = Assignments(a, self.bearer_token)
                    self.assignments.append(ass)
        else:
            print(response.status_code)

    def get_assignments(self, upcoming = True):
        params = {"bucket" : "upcoming"}  if upcoming else {}
        r_ep = self.resource_ep.copy()
        r_ep.append("assignments")

        response = self.get_resource(params = params, r_ep = r_ep, header = self.auth_headers)
        if response.status_code == 200:
            return response
        else:
            print(response.status_code)
            return None

    def add_link(self, short_hand,link):
        self.extra_links[short_hand] = link


    def remove_link(self, short_hand):
        if short_hand in self.extra_links:
            self.extra_links.pop()


    # kind of a throw up of everything just in case implemented
    def get_activity_stream(self):
        r_ep = self.resource_ep.copy()
        r_ep += ["activity_stream"]
        response = self.get_resource(r_ep = r_ep, header = self.auth_headers)
        return_obj = []
        if response.status_code == 200:
            return response.json()
        else:
            print(response.status_code)
            return None
    
    def get_quizzes(self):
        r_ep = self.resource_ep.copy()
        r_ep += ["quizzes"]
        response = self.get_resource(r_ep = r_ep, header = self.auth_headers)
    
    def get_resource(self, params = {}, r_ep = [], payload = {}, header = None):
        headers = self.auth_headers if header == None else header
        url = create_request_URL(init = self.gateway, resource_ep = r_ep, params=params)
        response = requests.request("GET", url, headers=headers, data = payload)
        return response



    # https://canvas.instructure.com/doc/api/modules.html
    # module build 
    # lack of consistency between professors use of modules 
        # some use it to hold by topic
        # others based on type of work e.g. reading 
    # 
    def get_modules(self):
        r_ep = self.resource_ep.copy()
        r_ep += ['modules']
        response = self.get_resource(r_ep = r_ep, header = self.auth_headers)

        if response.status_code == 200:
           modules = response.json()
           return modules
        else:
            print(response.status_code)
    
    def remove_assignment(self, ass_id):
        for a in self.assignments:
            pass

    # this is quite underwhleming at least for my account as I am not 
    # seeing anything directly related to my courses
    def __repr__(self):
        return str(vars(self))
    


class Assignments():

    # ATTRIBUTE EXPLAIN
        # description is in html, perhaps strip or use when outputting as a bot
        # due_at is date formated as such e.g. 2020-10-05T02:00:00Z
        # html_url, url directly to resource
        # id assignment id, useful for further api calls
        # submission_types -> array of strings descrbing submission types

    def __init__(self, ass, bearer_token):
        keys = ["description", "due_at", "html_url", "id", "name", "submission_types"]
        values = []
        self.bearer_token = bearer_token
        for k in keys:
            values.append(ass[k])
        self.description = values[0]
        self.due_at = values[1]
        self.html_url = values[2]
        self.id = values[3]
        self.name = values[4]
        self.submission_types = values[5]    



    def __repr__(self):
        return str(vars(self))
    
if __name__ == "__main__":
    API_URL = "https://canvas.ubc.ca/api/v1/users/self"
    API_KEY = ""

    req = requests.get(API_URL, headers = {"Authorization": "Bearer 11224~xe1g377tlaOPI0lx5SBBVrmgpKZ9jH2WmUPoLn0NapADNNTkz6ufwmxbn2y5wfhT"})
    #print("Bearer {}".format(API_KEY))
    json_req = req.json()

    self_id = json_req["id"]
    print(self_id)


    sa = Student(API_KEY)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sa.courses)

    # TODO
    # Remove a course from the listing 
    # add a course?

    # For a course get the relevant asingments
    def print_ass(student):
        for c in student.courses:
            course = student.courses[c]
            assignments = course.assignments
            for a in assignments:
                print(course.name, a.name)

    print_ass(sa)