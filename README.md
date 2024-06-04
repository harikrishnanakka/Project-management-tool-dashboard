# PROJECT-MANAGEMENT-TOOL-DASHBOARD

1.it is tool or Dashboard for the project management where it is very useful for the Team mates in the Company.

2.it has many features like home page,calenders,conversation chat,payment options,settings and filings.

3.There is the graphical representation where the graph is based on the:

a. Project Progress Graph:

● Shows the percentage of tasks completed in a project.

● Helps visualise overall project progress.

b. Task Timeline:

● Visualises the timeline of tasks within a project.

● Highlights deadlines and milestones

# How to install and work on this project:

1.I created the virtualenvironment in my project so there is no need of installation in your computer. just activate the virtual environment.

    cd myenv/scripts/activate.bat

2.Next step run the Development Server by using the below command:

    python manage.py runserver

3.After that place the url in the browser like:

     http://127.0.0.1:8000/

4.you can see the dashboard in your browser and the graphical representation in the dashboard


# create,read,update and delete:

1.Based on the project requirement i used the role Based authentication like projectManager can have all access,Team Members can have limmited 

access for crud operations and client cannot access any of the operations.

2.For this Authentication i used the token authentication where it can be used token for the authentication.

3.Use the postman for testing the endpoints of the api:

4.firstly we need to go to the endpoint for creating the username,password and role:

       http://localhost:8000/api/register/

5.The above endpoint is used to creating the username,password and role

6.Now for the Authentication you have to enter the your username,password and role for that use the endpoint like:

        http://localhost:8000/api-token-auth/

7.By the above endpoint we can authenticate and the token is generated:

8.The generated token is given in the Headers in the POSTMAN:

![Screenshot (30)](https://github.com/harikrishnanakka/Project-management-tool-dashboard/assets/152170400/d66cf276-2388-4082-84e4-573e7ffa9783)

9.like from the above you can see like that you have to use the token authentication.

10.Then after you can use the other endpoint for the CRUD operations:

       http://localhost:8000/api/projects/


       json data:{

                  "name":"Development of the AI",

                  "description":"It is breif about the development",

                  "start_date":"2024-05-01",

                  "end_date":"2024-06-03"

       }

11.The above enpoint is used to prepare the project you can do the crud opeartion for this Based on the role


12.Then After you can add the task by using on the endpoint based on the project primary key:
         
         http://localhost:8000/api/tasks/


        json data:{
                   "name":"Revanth"

                    "description":"Done with the frontend",
                     
                    "status":"done" ,   #done or pending

                    "deadline":"2024-06-15",

                    "project":"Development of AI"


}


14.Based on the above data you can also send the data, also you can update and delete the data based on the id of the project like:


         http://localhost:8000/api/projects/1/

Overall this is the project for the project management dashboard



https://github.com/harikrishnanakka/Project-management-tool-dashboard/assets/152170400/90fa6a52-a967-4f9b-88da-cbfa903a6606

The above is the project overview
     

******************************************TASK END****************************************************************************
       

