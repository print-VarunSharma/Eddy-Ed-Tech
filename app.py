from canvasAPI import Student, Course, Assignments
import os
from slack_bolt import App
import os
from dotenv import load_dotenv
load_dotenv()

signing_secret = os.getenv("SIGNING_SECRET")
token = os.getenv('SLACK_BOT_TOKEN')
CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")

# Initializes your app with your bot token and signing secret
app = App(
    token,
    signing_secret
)

STUDENT = Student(CANVAS_API_TOKEN)

def customize_course_choice_block(student):  
  option_arr = []
  
  for i,c in enumerate(student.courses.keys()):
    t = {
						"text": {
							"type": "mrkdwn",
							"text": c
						},
						"value": str(i)
					}
    option_arr.append(t)
  block = {
    "type": "modal",
    "title": {
      "type": "plain_text",
      "text": "Eddie Ed Tech Bot",
      "emoji": true
    },
    "submit": {
      "type": "plain_text",
      "text": "Submit",
      "emoji": true
    },
    "close": {
      "type": "plain_text",
      "text": "Cancel",
      "emoji": true
    },
    "blocks": [
      {
        "type": "header",
        "text": {
          "type": "plain_text",
          "text": "This is Eddy",
          "emoji": true
        }
      },
      {
        "type": "image",
        "image_url": "https://images.unsplash.com/photo-1511649475669-e288648b2339?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2378&q=80",
        "alt_text": "inspiration"
      },
      {
        "type": "section",
        "text": {
          "type": "plain_text",
          "text": "Eddy is Easy. He helps save students and educators time by integrating with other E-learning platforms such as Canvas and supercharges your workspace by having all your link resources ready to go.",
          "emoji": true
        }
      },
      {
        "type": "section",
        "text": {
          "type": "plain_text",
          "text": "Lets Begin with adding your courses",
          "emoji": true
        }
      },
      {
        "type": "divider"
      },
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "Select what courses you'd like to add."
        },
        "accessory": {
          "type": "checkboxes",
          "options": option_arr
        }
      }
    ]
  }
  return block





@app.message('sc')
def give_modal(message, say):
  client.views_push()
  

@app.message("student")
def choose_course_block(message, say):
  b = personalize_information(STUDENT)
  say(
    blocks = b,
    text = "error"
  )

@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.message("onboard")
def message_onboard(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hey there <@{message['user']}>! :wave:" 
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "We're excited to get started with you! Eddy helps you to save valuble time through integrating with your e-learning platform right here within Slack. Here are just few things which you will be able to do:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "• Receive information about courses \n • Never miss a quizz  \n • Stay on top of Assignments \n • Have all your links ready for the day  "
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "But before you can do all these fantastic things, we need to connect your Canvas to me. Simply click the button below:"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Connect account",
						"emoji": True
					},
					"value": "click_me_123",
           "action_id": "onboard_click"
				}
			]
		}
	],
        #text=f"Hey there <@{message['user']}>!"
    )

#The Intro to eddy 
# two buttons tell me more and skip tutorial 
@app.message("intro")
def intro(message, say):
    # say() sends a message to the channel where the event was triggered\
    say(
        blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Hello, I'm Eddy Ed-Tech. \n I'm here to supercharge your virtual work space!"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": "https://www.iconfinder.com/data/icons/chat-bot-emoji-filled-color/300/141453384Untitled-3-512.png",
                        "alt_text": "cute cat"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Tell me more"
                            },
                            "style": "primary",
                          "action_id": "to_onboard_click",
                            "value": "click_me_123"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "emoji": True,
                                "text": "Skip Turtorial"
                            },
                            "style": "danger",
                          "action_id": "intro_click",
                            "value": "click_me_123"
                        }
                    ]
                }
            ],
        text=f"Hey there <@{message['user']}>!"
    )

#   CONNECTING TO YOUR E-LEARNING PLATFORM
#   a gif as well as a continue button, 

@app.message("testing2")
def testing_two(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Connect to your E-learning platform",
                "emoji": True
            }
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "I Need a Marg",
                "emoji": True
            },
            "image_url": "https://media2.giphy.com/media/xT5P0uFIkoG4ovqLWo/giphy.gif",
            "alt_text": "marg"
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "To receive alerts and information from your E-Learning platform you will have to input your necessary sign-in data.",
                "emoji": True
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Contine",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "style": "primary"
                }
            ]
        }
            ],
        text=f"Hey there <@{message['user']}>!"
    )

#   CONNECTING TO YOUR E-LEARNING PLATFORM
#   a gif as well as a continue button, DIFFERENT GIF WILL HAVE TO POULATE THIS

@app.message("testing3")
def testing_three(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Adding your courses, assignments, and quizzes",
                "emoji": True
            }
        },
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": "I Need a Marg",
                "emoji": True
            },
            "image_url": "https://media2.giphy.com/media/xT5P0uFIkoG4ovqLWo/giphy.gif",
            "alt_text": "marg"
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Select what information you want from your E-learning platform . Don't worry you can always change this later ",
                "emoji": True
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Contine",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "style": "primary"
                }
            ]
        }
            ],
        text=f"Hey there <@{message['user']}>!"
    )

@app.message("token")
def token(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
                {
            "title": {
                "type": "plain_text",
                "text": "Input your Token",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "type": "modal",
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Go to your E-Learning platform and generate your token in your profile settings.\n Hit Submit and close this window when you are done. ",
                        "emoji": True
                    },
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True
                    }
                }
            ]
        }
            ],
        text=f"Hey there <@{message['user']}>!"
    )
    
@app.action("intro_click")
def action_intro_click(body, ack, say):
    ack()
    say([
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "We're excited to get started with you! Eddy helps you to save valuble time through integrating with your e-learning platform right here within Slack. Here are just few things which you will be able to do:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "• Receive information about courses \n • Never miss a quizz  \n • Stay on top of Assignments \n • Have all your links ready for the day  "
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "But before you can do all these fantastic things, we need to connect your Canvas to me. Simply click the button below:"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Connect account",
						"emoji": True
					},
					"value": "click_me_123",
           "action_id": "onboard_click"
				}
			]
		}
	])

@app.action("to_onboard_click")
def action_onboard_click(body, ack, say):
    # Acknowledge the action
    ack(
      #redirect(url_for('message_onboard'))
    )
    
    app.message("message",message_onboard(body["message"], say))
    #say(f"<@{body['user']['id']}> onboarding")
    
@app.action("onboard_click")
def action_onboard_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> onboarding")

'''This is the button from hello message'''
@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")

@app.command("/echo")
def repeat_text(ack, say, command):
    # Acknowledge command request
    ack()
    say(f"hello {command['text']}")
    

@ app.command("/coursechoice")
def choose_course(ack,say,command):
  ack()
  say(blocks = [
    {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "This is Eddy",
				"emoji": True
			}
		},
		{
			"type": "image",
			"image_url": "https://images.unsplash.com/photo-1511649475669-e288648b2339?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2378&q=80",
			"alt_text": "inspiration"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Eddy is Easy. He helps save students and educators time by integrating with other E-learning platforms such as Canvas and supercharges your workspace by having all your link resources ready to go.",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Lets begin with adding your courses",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Choose your course"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*POLI 369B*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*CPSC 415*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*Skip*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Choose your course"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "CPSC 390",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*GERM 401*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*Skip*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Choose your course "
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*COMM 370*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*POLI 380*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*Skip*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "All done?"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Submit",
					"emoji": True
				},
				"value": "click_me_123"
			}
		}
  ])
    
    
@app.command('/showcpsc')
def showcpsc(ack,say,command):
  print('here')
  ack()
  say(blocks = [
    {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You have a new assignment available!  \n*<fakeLink.toEmployeeProfile.com|CPSC 415 PD 2>*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Name:*\n Project Deliverable 2"
				},
				{
					"type": "mrkdwn",
					"text": "*Due:*\nOct 23 2020"
				},
				{
					"type": "mrkdwn",
					"text": "*Updated:*\nOct 1, 2020 (2 day)"
				},
				{
					"type": "mrkdwn",
					"text": "*Description :*\n Second Project Deliverable, focus on ... "
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Add to calendar"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Acknowledge"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}
  ])
  
  
@app.command("/assignments")
def showAss(ack,say,command):
  ack()
  say(blocks = [
		{
			"type": "header",
			"block_id": "MA+Iw",
			"text": {
				"type": "plain_text",
				"text": "Assignments :rocket:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"block_id": "mkII",
			"text": {
				"type": "plain_text",
				"text": "Brief Overview of all your assignments. \n Enter /add to add more outside this list",
				"emoji": True
			}
		},
		{
			"type": "image",
			"title": {
				"type": "plain_text",
				"text": "I Need a Marg",
				"emoji": True
			},
			"image_url": "https://slack-imgs.com/?c=1&o1=ro&url=https%3A%2F%2Fimages.unsplash.com%2Fphoto-1434030216411-0b793f4b4173%3Fixlib%3Drb-1.2.1%26ixid%3DeyJhcHBfaWQiOjEyMDd9%26auto%3Dformat%26fit%3Dcrop%26w%3D2100%26q%3D80",
			"alt_text": "marg"
		},
		{
			"type": "divider",
			"block_id": "fAve"
		},
		{
			"type": "section",
			"block_id": "MLMQk",
			"fields": [
				{
					"type": "plain_text",
					"text": "*POLI 369 Paper on International Law in Space*",
					"emoji": True
				},
				{
					"type": "plain_text",
					"text": "*CPSC 405 Full Statck Term Project*",
					"emoji": True
				},
				{
					"type": "plain_text",
					"text": "*GERM 304 Group Analysis of the GDR*",
					"emoji": True
				},
				{
					"type": "plain_text",
					"text": "*POLI 460 Debate Submission*",
					"emoji": True
				},
				{
					"type": "plain_text",
					"text": " \n *CENS 301 Group Work for discussion on Society and the State*",
					"emoji": True
				}
			]
		}
	])
    
@app.command('/showpoli')
def showPoli(ack,say,command):
  print('here')
  ack()
  say(blocks = [
    {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "You have a new assignment available!  \n*<fakeLink.toEmployeeProfile.com|POLI 369B Paper>*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Name:*\n Paper on International Law in Space"
				},
				{
					"type": "mrkdwn",
					"text": "*Due:*\nOct 10 2020"
				},
				{
					"type": "mrkdwn",
					"text": "*Updated:*\nOct 2, 2020 (1 day)"
				},
				{
					"type": "mrkdwn",
					"text": "*Description :*\n Readings: Acemoglu and Robinson 3.8, 4.1."
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Add to calendar"
					},
					"style": "primary",
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Acknowledge"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}
  ])

@app.command("/linkbucket")
def linkbucket(ack, say, command):
    # Acknowledge command request
    ack()
    say(blocks = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Link Bucket :rocket:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Your workspace is supercharged. Here are all the resources you'll need for the day! :smile:"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://docs.microsoft.com/en-us/learn/%7CMicrosoft Learn>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://media-exp1.licdn.com/dms/image/C560BAQGG-2Kb6o7o4A/company-logo_200_200/0?e=1606953600&v=beta&t=aTjKNi0Nbc1gjrWH12SwHARYaMqMzTszvb6T3WwwzF8",
				"alt_text": "cute cat"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://byers.typepad.com/space//%7CProfessor Byers' POLI 369 Astropolitics Website>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://images.axios.com/IQgM86W7HoDx3PqeynYILgb0SbI=/0x0:1920x1080/1920x1080/2020/05/26/1590536109482.jpg",
				"alt_text": "cute cat"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://www.youtube.com/watch?v=wAPCSnAhhC8%7C Your Favorite YouTube Playlist>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://i.ytimg.com/vi/5qap5aO4i9A/maxresdefault.jpg",
				"alt_text": "cute cat"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://app-ca.tophat.com/e/847786/lecture/%7CTopHat>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
				"alt_text": "cute cat"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://www.coursera.org/learn/machine-learning/%7CCoursera-learn-machine-learning>"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://tophat.com/wp-content/uploads/2017/05/tophat.png",
				"alt_text": "cute cat"
			}
		}
	])
    
@app.options("menu_selection")
def show_menu_options(ack):
    options = [
        {
            "text": {"type": "plain_text", "text": "Option 1"},
            "value": "1-1",
        },
        {
            "text": {"type": "plain_text", "text": "Option 2"},
            "value": "1-2",
        },
    ]
    ack(options=options)
    
@app.message("courses")
def message_courses(message, say):
  say(
  [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "This is Eddy",
				"emoji": True
			}
		},
		{
			"type": "image",
			"image_url": "https://images.unsplash.com/photo-1511649475669-e288648b2339?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2378&q=80",
			"alt_text": "inspiration"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Eddy is Easy. He helps save students and educators time by integrating with other E-learning platforms such as Canvas and supercharges your workspace by having all your link resources ready to go.",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Lets Begin with adding your courses",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a course you would like to add"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a course you would like to add"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Pick a course you would like to add"
			},
			"accessory": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				]
			}
		}
	])
  
@app.shortcut({"callback_id": "open_onboard_modal", "type": "message_action"})
def open_modal(ack, shortcut, client):
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using one of the built-in WebClients
    client.views_open(
        trigger_id=shortcut["button_click"],
        # A simple view payload for a modal
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "My App"},
            "close": {"type": "plain_text", "text": "Close"},
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "About the simplest modal you could conceive of :smile:\n\nMaybe <https://api.slack.com/reference/block-kit/interactive-components|*make the modal interactive*> or <https://api.slack.com/surfaces/modals/using#modifying|*learn more advanced modal use cases*>."
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "Psssst this modal was designed using <https://api.slack.com/tools/block-kit-builder|*Block Kit Builder*>"
                        }
                    ]
                }
            ]
        }
    )

@app.event("app_home_opened")
def open_modal(client, event, logger):
    try:
        # Call views.publish with the built-in client
        client.views_publish(
            # Use the user ID associated with the event
            user_id=event["user"],
            # Home tabs must be enabled in your app configuration
            view={
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "This is Eddy",
				"emoji": true
			}
		},
		{
			"type": "image",
			"image_url": "https://images.unsplash.com/photo-1511649475669-e288648b2339?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2378&q=80",
			"alt_text": "inspiration"
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Eddy is Easy. He helps save students and educators time by integrating with other E-learning platforms such as Canvas and supercharges your workspace by having all your link resources ready to go.",
				"emoji": true
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Open up Eddy anytime and he"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://www.iconfinder.com/data/icons/chat-bot-emoji-filled-color/300/141453384Untitled-3-512.png",
				"alt_text": "cute cat"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Want to know more?",
						"emoji": true
					},
					"value": "click_me_123"
				}
			]
		}
	]
}
        )

    except Exception as e:
        logger.error(f"Error opening modal: {e}")

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 4000)))