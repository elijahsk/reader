from xml.dom import minidom
import re
import urllib.request
import json

# get XML RSS feed
response = urllib.request.urlopen("http://www.dhs.sg/rss/what%2527s-new%3F-19.xml")
xml = response.read()

# get all XML as a string
xml_data = minidom.parseString(xml).getElementsByTagName('channel')

# get all items
parts = xml_data[0].getElementsByTagName('item')

rawdata=[]
temparray={}
# loop all items
for part in parts:
    # get title
    title = part.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
    # get link
    link = part.getElementsByTagName('link')[0].firstChild.nodeValue.strip()
    # get description
    description = part.getElementsByTagName('description')[0].firstChild.wholeText.strip()
    description = re.sub("<[^>]*>", "", description)
    description = description[:-10]
    temparray.update(title=title)
    temparray.update(link=link)
    temparray.update(description=description)
    rawdata.append(temparray)
    temparray={}
title=' Apr 1: I Finish the First Challenge!'
link=' http://people.dhs.sg/whatsnew/reader.py'
description=' None. dunno what to say...'
temparray.update(title=title)
temparray.update(link=link)
temparray.update(description=description)
rawdata.append(temparray)

encoded=json.dumps(rawdata)

decoded=json.loads(encoded)

outfile = open("reader.html", "w")

print(decoded)
outfile.write("""
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=gbk" />
	<meta name = "viewport" content = "width=device-width, initial-scale=1, maximum-scale=2" />
	
    <title>What's New</title>    
    <link rel="stylesheet" media="screen and (min-width: 750px),projection" type="text/css" href="http://people.dhs.sg/songkai/whatsnew/css/main.css" />
    <link rel="stylesheet" media="screen and (max-width: 750px)" type="text/css" href="http://people.dhs.sg/songkai/whatsnew/css/print.css" />
</head>

<body>

<div id="main" class="box">

    <div id="header">

        <h1 id="logo">What's<strong> New</strong></h1>
        <hr class="noscreen" />          

    </div>

     <div id="tabs" class="noprint">

            <h3 class="noscreen">Navigation</h3>
            <ul class="box">
                <li id="active"><a href="#">DHS News<span class="tab-l"></span><span class="tab-r"></span></a>
            </ul>

        <hr class="noscreen" />
     </div> 

    <div id="page" class="box">
    <div id="page-in" class="box">

        <div id="strip" class="box noprint">

            <p id="breadcrumbs">You are here: <a href="http://www.dhs.sg">DHS</a> &gt; <a href="#"><strong>News</strong></a>  </p>
            <hr class="noscreen" />
            
        </div>
    <div id="content">
""")
for item in decoded:
    outfile.write("""
<div class="article">
<h2><span>"""+item.get('title')+"""</span></h2>
<p><span class="cat"> Link: <a href=" """+item.get('link')+""" " >"""+item.get('link')+"""</a></span></p>
<h3> Description: """+item.get('description').replace('\xa0',' ')+"""</h3>
</div>
""")
outfile.write("""</div>        <div id="col" class="noprint">
            <div id="col-in">

                <!-- About Me -->
                <h3><span><a href="#">About Me</a></span></h3>

                <div id="about-me">
                    <p><img src="http://people.dhs.sg/songkai/whatsnew/design/tmp_photo.gif" id="me" alt="Yeah, it´s me!" />
                    <strong>SK</strong><br />
                    Age: 99999<br />
                    Somewhere over the rainbow<br />
                    <a href="http://people.dhs.sg/songkai">My Profile</a></p>
                </div> <!-- /about-me -->

                <hr class="noscreen" />
                <hr class="noscreen" />
            
            </div> <!-- /col-in -->
        </div> <!-- /col -->
</div>
</div>
<div id="footer">
        <div id="top" class="noprint"><p><span class="noscreen">Back on top</span> <a href="#header" title="Back on top ^">^<span></span></a></p></div>
        <hr class="noscreen" />        
        <p id="createdby">created by <a href="http://www.nuvio.cz">Nuvio | Webdesign</a> <!-- DON´T REMOVE, PLEASE! --></p>
        <p id="copyright">&copy; 2007 <a href="mailto:my@mail.com">My Name</a></p>
    </div>
    </body></html>""".replace('\xa0',' ').replace('\xb4',' ')
)
outfile.close()



