#!/usr/bin/python
#
# Connie Chang (cfchang@bu.edu)
# Final Project CS 108
# filename: movieRating.py
# description: This program keeps track of TV shows that users want to add to a list
# This program can add, delete, and update profiles and TV shows as well as
# average user ratings. In a way, it's kind of like a mini Rotten Tomatoes.

import MySQLdb as db
import time
import cgi
import cgitb; cgitb.enable()
import Cookie
import os

print "Content-Type: text/html"
print "" # blank line

################################################################################
def getConnectionAndCursor():
    """
    This function will connect to the database and return the
    Connection and Cursor objects.
    """ 
    # connect to the MYSQL database
    conn = db.connect(host="localhost",
                      user="cfchang",
                      passwd="0388",
                      db="cfchang")

    cursor = conn.cursor()
    return conn, cursor
################################################################################
def debugFormData(form):
    """
    A helper function which will show us all of the form data that was
    sent to the server in the HTTP form.
    """
    
    print("""
    <h2>DEBUGGING INFORMATION</h2>
    <p>
    Here are the HTTP form data:
    """)
    print("""
    <table border=1>
        <tr>
            <th>key name</th>
            <th>value</th>
        </tr>
    """)
    
    # form behaves like a python dict
    keyNames = form.keys()
    # note that there is no .values() method -- this is not an actual dict

    ## use a for loop to iterate all keys/values
    for key in keyNames:

        ## discover: do we have a list or a single MiniFieldStorage element?
        if type(form[key]) == list:

            # print out a list of values
            values = form.getlist(key)
            print("""
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, str(values)))

        else:
            # print the MiniFieldStorage object's value
            value = form[key].value
            print("""
        <tr>
            <td>%s</td>
            <td>%s</td>
        </tr>
            """ % (key, value))
        
    print("""
    </table>
    <h3>End of HTTP form data</h3>
    <hr>
    """)

## end: def debugFormData(form)

################################################################################
def doHTMLTail():
    """
    A helper function to link back to the main home page.
    """

    # always show this link to go back to the main page
    # Write some CSS and html to format various sections of the following pages
    
    print ("""
    <!DOCTYPE html>
    <style>
        #header {
        background-color:CornflowerBlue;
        color:white;
        clear:both;
        text-align:center;
        padding:5px;	 	
    }
     <style>
    #header {
        background-color:Blue;
        color:White
        text-align:center;
        padding:5px;
    }
    #body{
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        color: White;
        background-color: Black;
        background-image: url(http://sandymillin.files.wordpress.com/2013/03/tv-shows-word-cloud.png);
        font-family: arial;
        font-size: 15px;
    }
    #section {
        background-color:SkyBlue;
        height:300px;
        width:500px;
        float:center;
        padding:5px;
        
    #section2 {
        background-color:coral;
        height:300px;
        width:500px;
        float:center;
        padding:5px;
    }
    #table1
    {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 15px;
    }
    #table2
    {
        border: 1px solid black;
        border-collapse: collapse;
        background-color:coral;
        padding: 15px;
    }
    #nav1 {
        line-height:30px;
        background-color:Navy;
        color: White;
        height:500px;
        width:150px;
        float:left;
        padding:5px;	      
    }   
    #nav2 {
        line-height:30px;
        background-color:Navy;
        color: White;
        height:500px;
        width:150px;
        float:right;
        padding:5px;	      
    }
    </style>
    <hr>
    <div id="header">
        <header>
        <a href="./movieRating.py">Return to the Main Page</a><br>
        </header>
    </div>
    </html>

    """)
################################################################################
def mainPage(title):
    """
    A helper function to print out title and main page where user can select
    if they want to see the full list of TV shows and full list of Users.
    """
    #Write some html code for the header and formatting the main page
    #Includes the Show and User submit button and user authentification.
    
    print("""
    <html>

    <head>
    <title>%s</title>
    </head>    

        <div id="header">
            <header>
            <h1><center>Welcome to Show Select!</center></h1>
            </header>
        </div>
        <hr>
            <article>
                <p>

            <center><table border="10" cellpadding="6" width="1100px height="50px" bgcolor="Coral" ></center>
                <tr>
                <td>
                <center><font face="helvetica" size ="3" color="white">
                    Show Select allows users to create a complete list of TV shows. <br>
                    Each user can customize and modify their own list of shows and rate them accordingly
                    on their show list page.
                    </font>
                    </center>
                </td>
                </tr>
            </table></center>
            <br>
                <body background="tv-shows-word-cloud.jpg">
                    <div id="nav1">               
                    </div>
                    <div id="nav2">
                    </div>

                    <center><table border="10" cellpadding="6" width="1000px" height="300px" bgcolor="RoyalBlue" ></center>
                    <form method="get">
                        <tr>
                        <td>
                            <center><button type="submit" name="shows" value="Shows">Shows</button></center>
                        </td>
                        <td>
                            <center><input type="submit" name="users" value="Users"></center>
                        </td>
                        </tr>
                    <center></table></center>
                    <hr>
                    </form>
                    </table>
                </div>
                </p>
            </article>

    <!--Attempt to create a login
            <article>
                <center>If you are not a registered user, please enter your:</center>
                <p>
                <form method="post">
                <center><table></center>
                  <tr>
                    <td>
                      <center><h3>Email Address:</h3></center>
                    </td>
                    <td>
                      <center><input type="text" name="email" size="20"><br></center>
                    </td>
                  </tr>
                  <tr>
                    <td>
                      <center><h3>Password:</h3></center>
                    </td>
                    <td>
                    <center><input type="password" name="password" size="20"><br></center>
                  </tr>
                  <tr>
                    <td>
                    <center><input type="submit" name="login_button" value="Authenticate"></center>
                    </td>
                    <td>
                    </td>
                  </tr>
                <center></table></center>
                </form>
                </p>
                </article>
                -->
    </html>
    """ % (title))
################################################################################

def doAuthentication(form):

    # get email, password:
    email = form["email"].value
    password = form["password"].value

    # run a query against the database, check if valid username
    #HOWWWWW????

    # create a cookie, and send it to the client
    cookie=Cookie.SimpleCookie()
    cookie["login"] = email
    cookie["whatever"]="blahblahblah"

    # send cookie to the client
    print cookie # writes an HTTP header 

    # this function will print the rest of the HTTP headers
    #doHTMLHead("Remember Me")

    print """
    Authentication complete, %s. You have been identified by our servers.
    """ % email
##############################################################################
def printWelcomeScreen(email):
    """
    A helper function that confirms that a cookie has been sent to the server.
    """

    print """
    Welcome back, %s. It's good to see you again.
    """ % email

################################################################################
def getAllUsers():
    """
    Middleware function to get all users from the userList table.
    Returns a list of tuples of (profileID, userName).
    """

    # connect to database
    conn, cursor = getConnectionAndCursor()
    
    # build SQL
    sql="""
    SELECT profileID, userName
    FROM userList
    """
    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data
################################################################################

def getOneProfile(profileID):
    """
    Middleware function to retrieve one profile record from the database.
    It returns a list containing records of one tuple. (One Profile).
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM userList
    WHERE profileID=%s
    """

    # execute the query
    parameters = (int(profileID), )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    cursor.close()
    conn.close()

    #print data
    return data
################################################################################
def printAllUsers(data):
    """
    Presentation layer function to display a table containing all users userName.
    """
    
    ## create an HTML table for output:
    print("""
    <div id="header">
    <header><h2>User List</h2></header>
    <p>
    </div>
    <hr>

    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    
    <center><table border="1" cellpadding="2" cellspacing="0" width="50%" bgcolor="coral"></center>
      <tr>
        <td><font size=+1"><b>profileID</b></font></td>
        <td><font size=+1"><b>User Name</b></font></td>
      </tr>
    """)
    #Loop to access and link each userName to each person's profile page.
    for row in data:
        (profileID, userName)=row

        print("""
      <tr>
        <td><a href="?profileID=%s">%s</a></td>
        <td><a href="?profileID=%s">%s</a></td>
      </tr>
        """ % (profileID, profileID, profileID,userName))
        
    #Close table and confirm that changes have to been made to the database                   
    print("""
    <center></table></center>
    """)
    print("<center>Found %d users.</center><br>" % len(data))

    # form to bring up add new profile
    print ("""
    <form>
    <center><table border="3" cellpadding="10" cellspacing="0" width="10%" bgcolor="PowderBlue"></center>
    <tr><td><input type="submit" name="newUser" value="Add New User"></tr></td> </table>
    </form>
    """)

################################################################################
def printOneProfile(data):
    """
    Presentation layer of each user's profile page. 
    """
    #unpack data values
    (profileID,link,userName,email,activities)=data[0]

    #write some HTML code to format and print out on page
    print """
    <div id="header">
    <center><header><h2>%s's Profile Page</h2></header></center>
    <p>
    </div>
    <hr>
  
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
      
    <center><img src="%s" width=250 height=300></center><br>
    <center><table border="3" cellpadding="10" cellspacing="0" width="100" bgcolor="Coral"></center>
    <form method="get">
        <tr>
            <td>Email:</td>
            <td>%s</td>
        </tr>
            <td>About Me:</td>
            <td>%s</td>
        <tr>
    </form>
    <center></table></center>
    """ % (userName,link,email,activities)

    #Form to allow user to update Profile 
    print """
    <center><table border="3" cellpadding="10" cellspacing="0" width="100" bgcolor="PowderBlue"></center>
    <form method="get">
        <br>
        <tr><td>
            <center><input type="submit" name="beginUpdateProfile" value="Update"></center>
            <center><input type="hidden" name="profileID" value="%s"></center>
        </td></tr>
    </form>
    </table>
    """ % (profileID)

    #Form to allow user to delete profile
    print """
    <center><table border="3" cellpadding="10" cellspacing="0" width="100" bgcolor="PowderBlue"></center>
    <form method="get">
        <tr><td>
            <input type="submit" name="deleteProfile" value="Remove">
            <input type="hidden" name="profileID" value="%s">
        </td></tr>
    </form>
    <center></table></center>
    """ % (profileID)

    #Form to allow user to access their list of shows
    print """
    <center><table border="3" cellpadding="10" cellspacing="0" width="100" bgcolor="PowderBlue"></center>
    <form method="get">
        <tr><td>
            <input type="submit" name="showList" value="Show List">
            <input type="hidden" name="profileID" value="%s">
        </td></tr>
    </form>
    <center></table></center>
    """ % (profileID)
    
    

################################################################################
def printAddProfileForm():
    """
    Presentation layer: Form page for new users to input information
    """
    # write some more HTML code to format user input form fields
    print ("""
    <div id="header">
    <header><h2>Add New Profile</h2></header>
    <p>
    </div>
    <hr>

    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    
    <center><table border=1></center>
    <form method="post">
        <tr>
            <td><label>User Name:</label></td>
            <td><input type="text" name="userName"></td><br>
        </tr>
        <tr>
            <td><label>Profile Picture:<br>Input a URL</label></td>
            <td><input type="text" name="link"></td><br>
        </tr>
        <tr>
            <td><label>Email:</label></td>
            <td><input type="text" name="email"></td><br>
        </tr>
        <tr>
            <td><label>About Me:</label></td>
            <td><input type="text" name="activities"></td><br>
        </tr>
        <tr>
            <td><input type="submit" value="Add"></td>
        </tr>
    </form>
    <center></table></center>
    """)
################################################################################
def addProfile(userName,link,email,activities):
    """
    Finds the next valid profileID for the profiles table
    (One more than the current maximum id. Insert must provide 5 fields)
    (nextID,link,userName,email,activities)
    """
     # connect to db
    conn, cursor = getConnectionAndCursor()
    # write some sql
    sql1 = """
    SELECT*FROM userList
    WHERE profileID
    ORDER BY profileID DESC
    """
    # execute the SQL against the database cursor
    cursor.execute(sql1)
    # read/process the result set form the database
    results = cursor.fetchall()
    # Access to first row in profile table
    (profileID,link2,userName2,email2,activities2)=results[0]

    sql2 = """
    INSERT INTO userList(profileID,link,userName,email,activities)
    VALUES(%s,%s,%s,%s,%s)
    """
    
    # Creates new id number by increasing 1 to max value.
    nextID=int(profileID)+1
    # Insert new data into each variable
    parameters = (nextID,link,userName,email,activities)

    # (3) execute the SQL against the database cursor
    cursor.execute(sql2, parameters)
    
    # (4) read/process the result set form the database
    # UPDATE/INSERT/DELETE: we don't get records back
    # find the rowcount
    rowcount = cursor.rowcount
    
    # note that results is a list of tuples    
    # (5) clean up
    conn.commit() # commit changes to the database
    cursor.close()
    conn.close()

    return rowcount

################################################################################

def printUpdateProfileForm(data):
    """
    Display HTML form to update the profile for a user.
    Parameter data should be a tuple containing a single record
    from the profiles table.
    Get the data for this record from the getOneProfile(profileID)
    Contain hidden form field containing the profileID and a submit button
    """
    #unpack data values
    (profileID,userName,link,email,activities)=data[0]

    #HTML code to format the user input fields
    print """
    <div id="header">
    <header><h2>Update Profile Form</h2></header>
    </div>

    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    
    
    <form>
    <center><table border="1"></center>
        <tr>
            <td><label>User Name:</label></td>
            <td>%s</td>
        </tr>
        <tr> 
            <td><label>Profile Picture:</label></td>
            <td><img src="%s" width=133 height=150></td>
        </tr>
        <tr>
            <td><label>Email:</label></td>
            <td><input type="text" name="email"></td><br>
        </tr>
        <tr>
            <td><label>About Me:</label></td>
            <td><input type="text" name="activities"></td><br>
        </tr>
        <tr>
            <td>
            <input type="submit" name="completeUpdateProfile" value="Update Profile">
            <input type="hidden" name="profileID" value="%s">
            <input type="submit" name="cancel" value="Cancel Update">
            </td>
        </tr>
    </form>
    <center></table></center>
    """ % (link,userName,profileID)
    
################################################################################
def updateProfile(email, activities,profileID):
    """
    SQL to do an UDPATE query to modify the profile.
    The update must replace the existing email and activities for the
    profile record corresponding to profileID, using the values provided as
    parameters. The function should return a row count of how 
    many records were affected.
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    # prep some SQL
    sql = """
    UPDATE userList
    SET email=%s,
    activities=%s
    WHERE profileID=%s
    """
    parameters = (email,activities,profileID)

    #run the SQL
    cursor.execute(sql, parameters)
    
    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def deleteProfile(profileID):
    """
    SQL to do an UDPATE query to modify the profile.
    The update must replace the existing email and activities for the
    profile record corresponding to profileID, using the values provided as
    parameters. The function should return a row count of how 
    many records were affected.
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    # prep some SQL
    sql = """
    DELETE FROM userList
    WHERE profileID=%s
    """
    parameters = (profileID)

    #run the SQL
    cursor.execute(sql, parameters)
    
    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount

    
################################################################################
def getAllShows():
    """
    Middleware function to get all shows from the shows table.
    Returns a list of tuples.
    """
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT idNum,title,rating
    FROM shows
    """

    # execute the query
    cursor.execute(sql)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data
################################################################################
def printAllShows(data):
    """
    Presentation layer function to display a table containing all show titles
    """

    #Top header banner
    print """
    <div id="header">
    <head>
    <h2>Show List</h2>
    </head>
    <p>
    </div>
    <hr>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br> 
    """

    #Table to display show titles and ratings
    print"""
    <body background="tv-shows-word-cloud.jpg">
    <article>
    <center><table border="1" cellpadding="2" cellspacing="0" width="50%" bgcolor="coral"></center>
        <tr>
            <td><font size=+1"><b>ID</b></font></td>
            <td><font size=+1"><b>Titles</b></font></td>
            <td><font size=+1"><b>Official Ratings</b></font></td>
            <td><font size=+1"><b>User Ratings</b></font></td>
        </tr>
    </article>
    """
    
    #Loop to do the algorithm to get average of user ratings
    # And access each tv show desciption page
    
    for row in data:
        (idNum,title,rating)=row
        
        userRatings=getOneShowRating(idNum)
        userRatingList=[i[0] for i in userRatings]
        n=len(userRatingList)
        if n!=0:
            userRating= sum(userRatingList)/float(n)
        else:
            userRating=0

        print ("""
      <tr>
        <td><a href="?idNum=%s">%s</a></td>
        <td><a href="?idNum=%s">%s</a></td>
        <td>%s</td>
        <td>%.2f</td>
      </tr>
        """ % (idNum, idNum, idNum, title,rating,userRating ))
        
    #close table
    print ("""
    <center></table></center>
    """)
    #Total shows
    print ("<center>Found %d titles.</center><br><div>" % len(data))

    # form to bring up input new show
    print ("""
    <body>
    <center><table border="3" cellpadding="5" cellspacing="3" width="10%" bgcolor="CornflowerBlue"></center>
    <form>
        <tr>
            <td>
            <input type="submit" name="newShow" value="Add New Show">
            </td>
        </tr>
    </form>
    
    """)

    # form to select all shows by category
    print ("""
<!-- Select Options-->

    <form>
    <tr>
    <td>
    <p>Select by Category</p>
    <select name="category">
        <option value="Anime">Anime</option>
        <option value="Comedy">Comedy</option>
        <option value="Drama">Drama</option>
        <option value="Fantasy">Fantasy</option>
        <option value="Horror">Horror</option>
        <option value="Mystery">Mystery</option>
        <option value="Romance">Romance</option>
        <option value="Thriller">Thriller</option>  
    </select>
    <input type="submit" name="searchByCategory" value="Search">
    </td>
    </tr>
    </table>
    </form>
    </br>

    </body>
    """)
################################################################################
def getOneShow(idNum):
    """
    Middleware function to retrieve one show record from the database.
    It returns a list containing records of one tuple. (One show).
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT *
    FROM shows
    WHERE idNum=%s
    """

    # execute the query
    parameters = (int(idNum), )
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    cursor.close()
    conn.close()

    #print data
    return data
################################################################################
def printOneShow(data):
    """
    Presentation layer function to display the profile page for one user.
    """
    #calculate the average user ratings by calling getOneShowRating
    for row in data:
        #unpack data values
        (idNum,title,link,description,category,rating)=data[0]
        userRatings=getOneShowRating(idNum)
        userRatingList=[i[0] for i in userRatings]
        n=len(userRatingList)
        if n!=0:
            userRating= sum(userRatingList)/float(n)
        else:
            userRating=0
    
    #HTML code to format. Links back to Main, All shows, and all users
    print ("""
    <div id="header">
    <center><header><h2>%s</h2></heade></center>
    <p>
    </div>
    <hr>
    
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    
    <center><img src="%s" width=500 height=300></center><br>
    <center><table border="1" cellspacing="1" width="650" bgcolor="PowderBlue"></center>
    <form method="get">
        <tr>
            <td>Category:</td>
            <td>%s</td>
        </tr>
            <td>Official Ratings:</td>
            <td>%s</td>
        <tr>
            <td>User Ratings:</td>
            <td>%.2f</td>
        </tr>
        <tr>
            <td>Description:</td>
            <td>%s</td>
        </tr>
    </form>
    <center></table></center>
    <br>
    """ % (title,link,category,rating,userRating,description))

    #Allow user to choose to update show 
    print """
    <center><table border="1" cellspacing="1" width="100" bgcolor="PowderBlue"></center>
    <form method="get">
        <tr>
        <td>
            <label>Update Show</label>
            <input type="submit" name="beginUpdateShow" value="Update">
            <input type="hidden" name="idNum" value="%s">
        </td>
        </tr>
    </form>
    """ % (idNum)

    #Allow user to delete show from complete list
    print """
    <form method="get">
        <tr>
        <td>
            <label>Delete Show</label>
            <input type="submit" name="deleteShow" value="Remove">
            <input type="hidden" name="idNum" value="%s">
        </td>
        </tr>
    </form>
    <center></table></center>
    """ % (idNum)

################################################################################
def printAddShowForm():
    """
    presentation layer: create a form page for new users to input information
    """
    
    #HTML code to format user input form fields
    print ("""
    <div id="header">
    <h2>Add New Show</h2>
    <p>
    </div>
    <hr>

    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    

    <article>
    <center><table border=1></center>
    <form method="post">
        <tr>
            <td><label>Title:</label></td>
            <td><input type="text" name="title"></td><br>
        </tr>
        <tr>
            <td><label>Show Image:<br>Input a URL:</label></td>
            <td><input type="text" name="link"></td><br>        
        </tr>
        <tr>
            <td><label>Description:</label></td>
            <td><input type="text" name="description"></td><br>
        </tr>
        
        <!-- drop down box for Category-->
        <tr>
            <td><label>Category:</label></td>
            <td><select name="category" size="1">
                <option value="Anime">Anime</option>
                <option value="Comedy">Comedy</option>
                <option value="Drama">Drama</option>
                <option value="Fantasy">Fantasy</option>
                <option value="Horror">Horror</option>
                <option value="Mystery">Mystery</option>
                <option value="Romance">Romance</option>
                <option value="Thriller">Thriller</option>  
            </select></td>   
        </tr>

         <!-- drop down box for rating-->
        <tr>
        <td>
            <label>Rating:</label>
        </td>
        <td>
            <select name="rating" size="1">
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            </select>
        </tr>
        </td>
        <tr>
            <td><input type="submit" value="Add"></td>
        </tr>
    </form>
    <center></table></center>
    </article>
    """)
################################################################################
def addShowList(profileID,addShowListID,rating):
    """
    Finds the next valid idNum for the profiles table
    (One more than the current maximum id. Insert must provide 5 fields)
    (nextID,title,link,description,category,rating)
    """

     # (1) obtain a database connection and cursor
    conn, cursor = getConnectionAndCursor()
    
    # write some sql
    sql1 = """
    SELECT*FROM showList
    WHERE ratingID
    ORDER BY ratingID DESC
    """
    # execute the SQL against the database cursor
    cursor.execute(sql1)
    # read/process the result set form the database
    results = cursor.fetchall()
    # Access to first row in profile table
    (ratingID, _, _, _)=results[0]

    sql2 = """
    INSERT INTO showList
    VALUES(%s,%s,%s,%s)
    """
    # Creates new id number by increasing 1 to max value.
    nextID=int(ratingID)+1
    parameters = (nextID,profileID,addShowListID,rating)
    
    # (3) execute the SQL against the database cursor
    cursor.execute(sql2, parameters)
    
    # (4) read/process the result set form the database
    # UPDATE/INSERT/DELETE: we don't get records back
    # instead: a rowcount of how many rows were affected by this query

    rowcount = cursor.rowcount
    
    conn.commit() # commit changes to the database
  
    #printOneProfile(data)
        
    # (5) clean up
    #conn.commit()
    cursor.close()
    conn.close()

    return rowcount

################################################################################
def addShow(title,link,description,category,rating):
    """
    Finds the next valid idNum for the profiles table
    (One more than the current maximum id. Insert must provide 5 fields)
    (nextID,title,link,description,category,rating)
    """

    # connect to db
    conn, cursor = getConnectionAndCursor()
    # write some sql
    sql1 = """
    SELECT*FROM shows
    WHERE idNum
    ORDER BY idNum DESC
    """
    # execute the SQL against the database cursor
    cursor.execute(sql1)
    # read/process the result set form the database
    results = cursor.fetchall()
    # Access to first row in profile table
    (idNum,title2,link2,description2,category2,rating3)=results[0]

    sql2 = """
    INSERT INTO shows(idNum,title,link,description,category,rating)
    VALUES(%s,%s,%s,%s,%s,%s)
    """
    
    # Creates new id number by increasing 1 to max value.
    nextID=int(idNum)+1
    # Insert new data into each variable
    parameters = (nextID,title,link,description,category,rating)

    # (3) execute the SQL against the database cursor
    cursor.execute(sql2, parameters)
    
    # (4) read/process the result set form the database
    # UPDATE/INSERT/DELETE: we don't get records back
    # find the rowcount
    rowcount = cursor.rowcount
    
    # note that results is a list of tuples    
    # (5) clean up
    conn.commit() # commit changes to the database
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def printUpdateShowForm(data):
    """
    Presentation layer: create a form page for users to change and update show page
    """
    #unpack data values
    (idNum,title,link,description,category,rating)=data[0]
    
    #HTML code to format
    print """
    <div id="header">
    <header><h2>Update Show Form</h2><header>
    </div>
    <hr>
    <form>
    <center><table></center>
        <tr>
            <td><label>Title:</label></td>
            <td>%s</td>
        </tr>
        <tr>
            <td><label>Show Picture:<br>Input URL</label></td>
            <td><img src="%s" width=133 height=150></td>
        </tr>
        <tr>
            <td><label>Description:</label></td>
            <td><input type="text" name="description"></td><br>
        </tr>
        <tr>
            <td>
            <label>Select by Category</label>
            </td>
            <td>
            <select name="category">
                <option value="Anime">Anime</option>
                <option value="Comedy">Comedy</option>
                <option value="Drama">Drama</option>
                <option value="Fantasy">Fantasy</option>
                <option value="Horror">Horror</option>
                <option value="Mystery">Mystery</option>
                <option value="Romance">Romance</option>
                <option value="Thriller">Thriller</option>  
            </select>
            </td>
        </tr>
        <tr>
            <td>
                <label>Rating:</label>
                <select name="rating" size="1">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                </select>
            </td>
        </tr>            
        <tr>
            <td>
            <input type="submit" name="completeUpdateShow" value="Update Show">
            <input type="hidden" name="idNum" value="%s">
            <input type="submit" name="cancel" value="Cancel Update">
            </td>
        </tr>
    <center></table></center>
    </form>    
    """ % (title, link,idNum)
################################################################################
def updateShow(description,category,rating,idNum):
    """
    SQL to do an UDPATE query to modify the show.
    The update must replace the existing description, category, and rating for the
    show record corresponding to idNum, using the values provided as
    parameters. The function should return a row count of how 
    many records were affected.
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    # prep some SQL
    sql = """
    UPDATE shows
    SET description=%s,
    category=%s,
    rating=%s
    WHERE idNum=%s
    """
    parameters = (description,category,rating, idNum)

    #run the SQL
    cursor.execute(sql, parameters)
    
    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def deleteShow(idNum):
    """
    SQL to do a DELETE query to modify the show for show with idNum
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    # prep some SQL
    sql = """
    DELETE FROM shows
    WHERE idNum=%s
    """
    parameters = (idNum)

    #run the SQL
    cursor.execute(sql, parameters)
    
    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def getShowList(profileID):
    """
    Middleware Function will run a SELECT  query against the showList table, and return a
    list of tuples the user corresponds to the profileID in showList.
    """

    # connect to database
    conn, cursor = getConnectionAndCursor()

    sql = """
    SELECT *
    FROM showList
    WHERE profileID = %s
    """
    #tuple
    parameters = (profileID, )
    # execute the query
    cursor.execute(sql, parameters)
    
    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()

    #data is a list of tuples containing the friends ids
    return data
################################################################################
def printShowList(profileID, data):
    """
    Presentation-layer function take 2 parameters.
    Accesses each show's information for each show that is included in the user's list
    """
    
    #HTML code to format table
    print """
    <div id="header">
    <header><h2>Show List</h2></header>
    <p>
    </div>
    <hr>

    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py">Main</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?shows=Shows">All Shows</a><br>
    <a href="http://cs-webapps.bu.edu/cs108/cfchang/movieRating.py?users=Users">All Users</a><br>
    
    
    <center><table border="1" cellpadding="2" cellspacing="0" width="50%" bgcolor="PowderBlue"></center>
      <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Official Ratings</th>
        <th>User Ratings</th>
        <th>Action</th>
      </tr>
    """
    #Calls getUserRatings to calculate the average userRatings
    userRatings= getUserRatings(profileID)
    userRatingList= [i[0] for i in userRatings]

    #loop to get show information and userRatings
    x=0
    for row in data: #each row in data is a tuple of tuples
        #if row:
        (ratingID,profileID,idNum,userRating)=row
        data=getOneShow(idNum)
        (idNum,title,link,description,category,rating) = data[0]  

    ## create an HTML table for output: 
        print ("""
          <tr>
            <td><a href="?idNum=%s">%s</a></td>
            <td><a href="?idNum=%s">%s</a></td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <form>
                <input type="submit" name="deleteShowList" value="Remove">
                <input type="hidden" name="ratingID" value="%s">
                </form>
            </td>
          </tr>
            """ % (idNum, idNum, idNum, title,rating, userRatingList[x],ratingID))
        x+=1
    
    #close table
    print("""
    <center></table></center>
    """)
    #total show titles for the user
    print("<center>Found %d shows.</center><br>" % (x))
    
    #Allow user to add show to user list
    #addShowList= submit button
    #showList = user input
    print """
    <form>
    <center><table border="1" cellpadding="2" cellspacing="0" bgcolor="coral"></center>
        <tr>
            <td>
            <input type="hidden" name="addShowListID">
            <label>Input show ID you want to add:</label>
            <input type="hidden" name="profileID" value="%s">
            <input type="hidden" name="showList" value="Show List">
            </td>
        </tr>
        <tr>
            <td>
            <input type="text" name="idNum">
            <input type="submit" name="addShowList" value="Add Show">
            </td>
        </tr>
        <tr>
            <td>
            <label>User Rating:</label>
            <select name="rating" size="1">
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
          </td>
        </tr>
    </form>
    </table>
    """ % (profileID,)
  
    #Allow user to write a show review.
    #Shows user info and text box for user (profileID) input for new status
    print """
    <h2>Write a Show Review</h2>
    <p>
    <center><table border="1" cellpadding="2" cellspacing="0" bgcolor="coral"></center>
    <form method="get">
        <tr>
            <td>
                <label>Input show ID you want to review:</label>
            </td>
        </tr>
        <tr>
            <td>
                <input type="text" name="idNum"><br>
            </td>
        </tr>
        <tr>
            <td>
                <label>Review Comment:</label>
            </td>
        </tr>
        <tr>
            <td>
                <input type="text" name="comment"><br>
                <input type="hidden" name="profileID" value="%s">
            </td>
        <tr>
            <td>
                <input type="submit" name="submit" value="send">
            </td>
        </tr>
    </form>
    </table>
    """ % (profileID)

    #Show user their comments and reviews for their shows
    data = getReviewCommentsForUsers(profileID)
    printReviewCommentsForUsers(data)

################################################################################
def deleteShowList(ratingID):
    """
    SQL to do a delete query to modify the show list.
    The function should return a row count of how 
    many records were affected.
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()

    # prep some SQL
    sql1 = """
    DELETE FROM showList
    WHERE ratingID=%s
    """
    parameters = (ratingID)

    #run the SQL
    cursor.execute(sql1, parameters)

    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def getAllShowsCategory(category):
     """
    Executes a search query to get all shows by category
     """
     conn, cursor = getConnectionAndCursor()

    # prep some SQL
     sql = """
     SELECT idNum, title, rating
     FROM shows
     WHERE category=%s
     """
     #note: in MySQL, we use %s for all substitutions (compared to ? in sqlite)
     parameters = (category, )
     # run the SQL
     cursor.execute(sql, parameters)
        
     # fetch the results
     data = cursor.fetchall()

     # clean up
     cursor.close()
     conn.close()
        
     return data
################################################################################
def postReviewComment(profileID, idNum, comment):
    """
    Execute an insert query for users to write reviews and comments about the show
    """
    
    # connect to database
    conn, cursor = getConnectionAndCursor()
    # write some sql
    sql1 = """
    SELECT*FROM reviews
    WHERE reviewID
    ORDER BY reviewID DESC
    """
    # execute the SQL against the database cursor
    cursor.execute(sql1)
    # read/process the result set form the database
    results = cursor.fetchall()
    # Access to first row in profile table
    (reviewID,dateTime2,profileID2,idNum2,comment2)=results[0]
    
    sql2 = """
    INSERT INTO reviews
    VALUES (%s,%s,%s,%s,%s)
    """

    tm = time.localtime()
    timestamp = '%04d-%02d-%02d %02d:%02d:%02d' % tm[0:6]
    
    nextID=int(reviewID)+1
    
    #tuple
    parameters = (nextID,timestamp, profileID, idNum, comment)
    # execute the query
    cursor.execute(sql2, parameters)

    # (4) read/process the result set form the database
    # UPDATE/INSERT/DELETE: we don't get records back
    # instead: a rowcount of how many rows were affected by this query
    rowcount = cursor.rowcount
    
    # clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def getReviewCommentsForUsers(profileID):
    """
    Retrieve review comments for selected users by getting data from the database
    """
     # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT*
    FROM reviews
    WHERE profileID = %s
    """
    #tuple
    parameters = (profileID, )
    # execute the query
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    #print data
    return data
################################################################################
def printReviewCommentsForUsers(data):
    """
    Presentation layer: print out the review comments for users
    """
    #print data
    # read in each profile's reviews. Possible that profileID does not have comments.
    print """
    <h2>Review List</h2>
    <table border="1" cellspacing="1" width="800" bgcolor="PowderBlue">
          <tr>
            <td><font size=+1"><b>showID</b></font></td>
            <td><font size=+1"><b>Date and Time</b></font></td>
            <td><font size=+1"><b>Comments</b></font></td>
            <td><font size=+1"><b>Action</b></font></td>

          </tr>
        """
    
    #unpack data for each tuple in a tuple.
    for comment in data:
        #store tuple 
        (reviewID,dateTime,profileID,idNum,comments)=comment
        
        print("""
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                <form>
                <input type="submit" name="deleteComment" value="Remove">
                <input type="hidden" name="reviewID" value="%s">
                </form>
                </td>
            <tr>
            """ % (idNum,dateTime,comments,reviewID))
    print """
    </table>
    <br>
    """
################################################################################
def getShowReviews(idNum):
    """
    Retrieve show reviews for selected shows with all users by getting data from the database
    """
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT*
    FROM reviews
    WHERE idNum = %s
    """
    #tuple
    parameters = (idNum, )
    # execute the query
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    #print data
    return data
################################################################################
def printShowReviews(data):
    """
    Presentation layer: Print out the review comments selected shows by all users
    """
    #print data
    # read in each profile's reviews. Possible that profileID does not have comments.
    print """
    <center><h2>Review Comments</h2></center>
    <center><table border="1" cellspacing="1" width="800" bgcolor="PowderBlue"></center>
          <tr>
            <td><font size=+1"><b>profileID</b></font></td>
            <td><font size=+1"><b>Date and Time</b></font></td>
            <td><font size=+1"><b>Comments</b></font></td>

          </tr>
        """
    #unpack tuple in a tuple
    for comment in data:
        #store tuple 
        (reviewID,dateTime,profileID,idNum,comments)=comment
        
        print("""
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            <tr>
            """ % (profileID,dateTime,comments))
        
    #close the table
    print ("""
    <center></table></center>
    """)
################################################################################
def deleteReview(reviewID):
    """
    SQL to do a DELETE query to modify the profile. Delete review comment.
    The function should return a row count of how 
    many records were affected.
    """
    # connect to db
    conn, cursor = getConnectionAndCursor()
    
    # prep some SQL
    sql = """
    DELETE FROM reviews
    WHERE reviewID=%s
    """
    parameters = (reviewID)

    #run the SQL
    cursor.execute(sql, parameters)
    
    #find the rowcount
    rowcount = cursor.rowcount
    
    #clean up
    conn.commit()
    cursor.close()
    conn.close()

    return rowcount
################################################################################
def getOneShowRating(idNum):
    # connect to database
    conn, cursor = getConnectionAndCursor()

    # build SQL
    sql = """
    SELECT userRating
    FROM showList
    WHERE idNum = %s
    """
    #tuple
    parameters = (idNum, )
    # execute the query
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    #print data
    return data
    
    
################################################################################
##def getOneShowRating(idNum):
##    """
##    Retrieve all user ratings for each show (idNum). Average them.
##    """
##    # connect to database
##    conn, cursor = getConnectionAndCursor()
##
##    #list of shows
##    n=0
##    shows=getShowList(idNum) #suppose to be profileID
##    showRatings=[]
##
##    #write SQL
##    for show in shows:
##        sql = """
##        SELECT userRating
##        FROM showList
##        WHERE idNum = %s
##        """
##            
##        parameters = show[0]
##        
##        #execute the query
##        cursor.execute(sql,parameters )
##        
##        # get the data from the database:
##        result = cursor.fetchall()
##        if len(result):
##            showRatings+=list(result)
##            n = len(showRatings)
##            
##    #sum the user show ratings
##    showRatings = sum([i[0] for i in showRatings])
##    
##    #Not divisible by 0
##    if n != 0:
##        showRatings = int(showRatings)/float(n)
##
##    # clean up
##    conn.close()
##    cursor.close()
##
##    return showRatings
################################################################################
def getUserRatings(profileID):
    """
    Retrieve user ratings for selected users by getting data from the database
    """
    # connect to database
    conn, cursor = getConnectionAndCursor()

    #Build SQL
    sql = """
    SELECT userRating
    FROM showList
    WHERE profileID = %s
    """
        
    #tuple
    parameters = (profileID, )
    # execute the query
    cursor.execute(sql, parameters)

    # get the data from the database:
    data = cursor.fetchall()

    # clean up
    conn.close()
    cursor.close()
    
    return data
    
################################################################################
if __name__ == "__main__":
    # read a cookie from the HTTP request:
    cs = os.environ["HTTP_COOKIE"]
    # create a cookie object from this string
    cookie=Cookie.SimpleCookie()
    cookie.load(cs)
    # get form fields
    form = cgi.FieldStorage()
    
    if "login" in cookie:
        email=cookie["login"].value
        printWelcomeScreen(email)
    # if no cookie, check for login in process:
    elif "login_button" in form:     
        doAuthentication(form)
        
    #select all shows by category
    elif "searchByCategory" in form:
        category=form["category"].value
        data = getAllShowsCategory(category)
        printAllShows(data) 
        
     #Update Show       
    elif "beginUpdateShow" in form:
        idNum=form["idNum"].value
        data=getOneShow(idNum)
        printUpdateShowForm(data)
    elif "completeUpdateShow" in form and "idNum" in form and "title" in form and "link" in form and "description" in form and "category" in form and "rating" in form:
        idNum=form["idNum"].value
        title=form["title"].value
        link=form["link"].value
        description=form["description"].value
        categroy=form["category"].value
        rating=form["rating"].value

        rowcount=updateShow(title,link,description,category,rating,idNum)
        if rowcount==1:
            print ("%d profile has been updated.<p>" % rowcount)
        else:
            print ("Please fill out form.")
        
    #Update User      
    elif "beginUpdateProfile" in form:
        profileID=form["profileID"].value
        data=getOneProfile(profileID)
        printUpdateProfileForm(data)
        
    elif "completeUpdateProfile" in form:
        email=form["email"].value
        activities=form["activities"].value
        profileID=form["profileID"].value

        rowcount=updateProfile(email, activities,profileID)
        if rowcount==1:
            print ("%d profile has been updated.<p>" % rowcount)
        else:
            print ("Please fill out form.")
        
    #Add new User    
    elif "newUser" in form:
        printAddProfileForm()
        if "userName" in form and "link" in form and "email" in form and "activities" in form:
            userName=form["userName"].value
            link=form["link"].value
            email=form["email"].value
            activities=form["activities"].value

            rowcount=addProfile(userName,link,email,activities)
            print("You have made a new profile!")
        
    #Add New Show    
    elif "newShow" in form:
        printAddShowForm()
        if "title" in form and "link" in form and "description" in form and "category" in form and "rating" in form:
            title=form["title"].value
            link=form["link"].value
            description=form["description"].value
            category=form["category"].value
            rating=form["rating"].value
            
            rowcount=addShow(title,link,description,category,rating)
            if rowcount == 1:
                 print("You have added a new show!")
            else:
                print ("Please fill out form.")

    #Update Show     
    elif "beginUpdateShow" in form:
        idNum=form["idNum"].value
        data=getOneShow(idNum)
        printUpdateShowForm(data)

    elif "completeUpdateShow" in form:
        description=form["description"].value
        category=form["category"].value
        rating=form["rating"].value
        idNum=form["idNum"].value

        rowcount=updateShow(description,category,rating,idNum)
        if rowcount==1:
            print ("%d show has been updated.<p>" % rowcount)
        else:
            print ("Please fill out form.")
            
    #Delete from All Shows
    elif "deleteShow" in form:
        idNum=form["idNum"].value
        rowcount=deleteShow(idNum)
        if rowcount==1:
            print("%d show has been deleted.<p>" % rowcount)
       
    #Delete Profile
    elif "deleteProfile" in form:
        profileID=form["profileID"].value
        rowcount=deleteProfile(profileID)
        if rowcount==1:
            print("%d profile has been deleted.<p>" % rowcount)
            
    #Delete Comment/ Review        
    elif "deleteComment" in form:
        reviewID=form["reviewID"].value
        rowcount=deleteReview(reviewID)
        if rowcount==1:
            print("%d review has been deleted.<p>" % rowcount)    
 
    elif "profileID" in form:
        profileID=form.getvalue("profileID")
        data=getOneProfile(profileID)

        #Review List
        if "idNum" in form and "comment" in form and "submit" in form:
            idNum=form["idNum"].value
            comment=form["comment"].value
            postReviewComment(profileID, idNum, comment)

        #Add one show to user show list
        if not "showList" in form:
            printOneProfile(data)
        elif "idNum" in form and "addShowList" in form and "rating" in form:
            idNum=form["idNum"].value
            rating=form["rating"].value

            rowcount=addShowList(profileID,idNum,rating)
            if rowcount==1:
                print "%d show has been added.<p>" % rowcount
            else:
                print ("Please fill out form.")
                
            data=getShowList(profileID)
            printShowList(profileID, data)
 
        else:
            data=getShowList(profileID)
            printShowList(profileID, data)
            
    #Delete one show in user show List        
    elif "deleteShowList" in form and "ratingID" in form:
            ratingID=form["ratingID"].value
            
            rowcount = deleteShowList(ratingID)
            if rowcount==1:
                print "%d show has been removed.<p>" % rowcount
                
##            data=getShowList(profileID)
##            printShowList(profileID, data)
    
    #TV show profiles and its user reviews        
    elif "idNum" in form:
        idNum=form["idNum"].value
        data=getOneShow(idNum)
        printOneShow(data)

        data=getShowReviews(idNum)
        printShowReviews(data)
        
    #All Users
    elif "users" in form:
        data=getAllUsers()
        printAllUsers(data)
        
    #All Shows
    elif "shows" in form:
        data=getAllShows()
        printAllShows(data)

    #print("DEBUG:",form,"<HR>") ##ADD THIS LINE OF CODE TO SEE THE FORM FIELDS
    #debugFormData(form)
        
    #add decision-logic to determine whether to show one profile,
    #or else show the list of all users.
        
    #main page
    else:
        mainPage("ShowSelect")
        
    #Link to go back to main page
    doHTMLTail()







