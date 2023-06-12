data = open("bg3.txt", "r") #open the data plaintext file
base_array = [] #contains all data which will computed on
biggest_win_biggest_lose = [0,0]
unique_scores = []
every_score_never_done = []
frequency_dictionary = {}
heatmap_hexcodes = [
    "",
    "#00FF00",
    "#2BFF00",
    "#55FF00",
    "#80FF00",
    "#AAFF00",
    "#D5FF00",

    "#FFFF00",

    "#FFD500",
    "#FFAA00",
    "#FF8000",
    "#FF5500",
    "#FF2B00",
    "#FF0000"
] #the heatmap functionality will break if future datasets return a score frequency of 14, how do you automate this?
 
#STEP ONE EXTRACT DATA WE NEED AND REFORMAT IT
for i in data:
    #extract data from spreadsheet
    team1name = i[29:47].rstrip() #get team 1 name and strip whitespace
    team2name = i[64:82].rstrip() #get team 2 name and strip whitespace
    team1score = i[47:64].split("."); team1score = team1score[2].rstrip() #get team 1 total score no 6s or 1s and remove whitespace
    team2score = i[83:100].split("."); team2score = team2score[2].rstrip() #get team 1 total score no 6s or 1s and remove whitespace
    gamenumber = i[0:5].rstrip() #gets a games number and strips whitespace
    gamenumber = gamenumber.replace(".", "") #get rid of period from number
    gamedate = i[7:18].rstrip() #gets a games date and strips whitespace
    location = i[100:118].rstrip() #gets a games date and strips whitespace
    round_no = i[24:28].rstrip() #gets a round and strips whitespace

    #order winner score first, highest score is X axis, lowest score is Y.
    concated_data = ""
    if int(team1score) > int(team2score): 
        concated_data = team1name+","+team2name+","+team1score+","+team2score+","+gamenumber+","+gamedate+","+location+","+round_no
    elif int(team1score) < int(team2score): 
        concated_data = team2name+","+team1name+","+team2score+","+team1score+","+gamenumber+","+gamedate+","+location+","+round_no
    elif int(team1score) == int(team2score):
        concated_data =  team1name+","+team2name+","+team1score+","+team2score+","+gamenumber+","+gamedate+","+location+","+round_no

    base_array.append(concated_data)

#STEP TWO GENERATE A WHITE BACKGROUND BY FIRST WORKING OUT DIMENSIONS
for i in base_array:
    data_splitter = i.split(",")
    if int(data_splitter[2]) > biggest_win_biggest_lose[0]: biggest_win_biggest_lose[0] = int(data_splitter[2]) #if winning score is greater than current highest known update it
    if int(data_splitter[3]) > biggest_win_biggest_lose[1]: biggest_win_biggest_lose[1] = int(data_splitter[3]) #if loosing score is greater than current highest known update it

#STEP THREE GET EVERY UNIQUE SCORE
#loop through base array and get just the scores
for i in base_array:
    data_splitter = i.split(",")
    unique_scores.append(data_splitter[2]+":"+data_splitter[3])
#remove duplicate scores from the list
unique_scores = list(dict.fromkeys(unique_scores)) 

#STEP FOUR GENERATE HISTORY FILE AND HEATMAP FREQUENCY
out_js = open("history_scorigami.js", "w")
out_js.write("var aflhistory = {\n")
for key in unique_scores:
    out_js.write("'"+key+"': [\n")
    #loop through base array and find matching scores
    frequency = 0
    for i in base_array:
        data_splitter = i.split(",")
        check_string = data_splitter[2]+":"+data_splitter[3]
        if key == check_string:
            #out_js.write("'"+i+"',\n")
            out_js.write("'<b>Game "+data_splitter[4]+"-"+data_splitter[7]+":</b> "+data_splitter[0]+" v "+data_splitter[1]+" <br>@ "+data_splitter[6]+", "+data_splitter[5]+"',\n")
            frequency += 1
    #print (key+"_"+str(frequency)) #generates frequency used for heatmap
    frequency_dictionary[key] = frequency
    out_js.write("],\n")
out_js.write("}\n")
out_js.close()

#STEP OH FUCK STOP WHAT ARE YOU DOING
#CREATE A LIST OF EVERY POSSIBLE SCORE (IN SCOPE) AND THEN REMOVE THE UNIQUE SCORES ........ HOLY FUCK LETS CALL PYTHON SNAIL BECAUSE IM ABOUT TO MAKE IT SLOWER
#create initial list
for i in range(biggest_win_biggest_lose[0]+1):
    for j in range(biggest_win_biggest_lose[0]+1):
        if i >= j and j <= biggest_win_biggest_lose[1]: #scores cant be lower number first so dont add it too the list
            every_score_never_done.append(str(i)+":"+str(j))
#if a unique score is found in this list remove it (too avoid DOM ids clashing)
for i in unique_scores:
    if i in every_score_never_done: every_score_never_done.remove(i)

#STEP FIVE GENERATE HTML/SVG/CSS/JS
#now the fun part generate svg
out_svg = open("output_scorigami.html", "w")
#boilerplate header
out_svg.write("<html>\n")
out_svg.write("<head><style>body {font-family: 'Courier New', monospace;}</style></head>")
out_svg.write("<body style='background-color:#AFAFAF'>\n")
out_svg.write("<script type='text/javascript' src='history_scorigami.js'></script>\n") #load history
out_svg.write("<script type='text/javascript'>\n")

#function to destroy divs alive! thanks stack overflow
out_svg.write("function removeElementsByClass(className){\n")
out_svg.write("const elements = document.getElementsByClassName(className);\n")
out_svg.write("while(elements.length > 0){\n")
out_svg.write("elements[0].parentNode.removeChild(elements[0]);\n")
out_svg.write("}\n")
out_svg.write("}\n")

#function to display information about a partifular score
out_svg.write("function reply_click(clicked_id){\n") #check what square was clicked on
out_svg.write("document.getElementById('score').innerHTML = 'Score: '+clicked_id;\n") #show the score of the square
out_svg.write("if (aflhistory[clicked_id] == undefined) {\n")
out_svg.write("document.getElementById('occured').innerHTML = 'Occured: 0 times';\n")
out_svg.write("} else {\n")
out_svg.write("document.getElementById('occured').innerHTML = 'Occured: '+aflhistory[clicked_id].length+' times';\n") #show how many times this score has happened (not working)
out_svg.write("}\n")
out_svg.write("removeElementsByClass('game');\n") #delete previous information
out_svg.write("if (aflhistory[clicked_id] == undefined) {\n")
out_svg.write("removeElementsByClass('game');\n")
out_svg.write("} else {\n")
#look up score in the history dictionary and list all games that have that score
out_svg.write("console.log(clicked_id);\n")
out_svg.write("for (var i = 0; i < aflhistory[clicked_id].length; i++) {\n")
out_svg.write("const para = document.createElement('p');\n")
out_svg.write("para.className = 'game';\n")
out_svg.write("para.innerHTML = aflhistory[clicked_id][i];\n")
out_svg.write("document.getElementById('history').appendChild(para);\n")
out_svg.write("}\n")
out_svg.write("}\n")

out_svg.write("}\n")
out_svg.write("</script>\n")
out_svg.write("<div style='display: flex;'>\n")
out_svg.write("<div style='flex: 75%;'>\n")
#start svg
out_svg.write("<svg width=95% height=auto viewBox='0 0 "+str(biggest_win_biggest_lose[0])+" "+str(biggest_win_biggest_lose[1])+"'>\n")
out_svg.write("<rect width='"+str(biggest_win_biggest_lose[0]+1)+"' height='"+str(biggest_win_biggest_lose[1]+1)+"' x=0 y=0 style='fill:rgb(0,0,0)'/>\n")
#out_svg.write("<polygon points='0,0 0,"+str(biggest_win_biggest_lose[1]+1)+" "+str(biggest_win_biggest_lose[1]+1)+","+str(biggest_win_biggest_lose[1]+1)+"' style='fill:rgb(0,0,0)'/>\n")

#every other score square time :)
for i in every_score_never_done:
    data_splitter = i.split(":")
    out_svg.write("<rect width='1' height='1' x="+str(int(data_splitter[0])*1)+" y="+str(int(data_splitter[1])*1)+" style='fill:rgb(255,255,255)' id='"+i+"' onmouseover='reply_click(this.id)'/>\n")

#unique score square time :)
for i in unique_scores:
    data_splitter = i.split(":")
    out_svg.write("<rect width='1' height='1' x="+str(int(data_splitter[0])*1)+" y="+str(int(data_splitter[1])*1)+" style='fill:"+heatmap_hexcodes[frequency_dictionary[i]]+"' id='"+i+"' onmouseover='reply_click(this.id)'/>\n")

out_svg.write("</svg>\n")
#additional fun facts
out_svg.write("</div>\n")
out_svg.write("<div style='flex: 25%;'>\n")
out_svg.write("<div style='position: relative;'>\n")
out_svg.write("<h1 style='text-align: center'>VFL/AFL Scorigami</h1>\n")
out_svg.write("<p>Last updated: 4-Jun-2023</p>\n")
out_svg.write("<h2 id='score'>Hello</h2>\n")
out_svg.write("<h2 id='occured'>World !</h2>\n")
out_svg.write("</div>\n")
out_svg.write("<div id='history' style='width: auto; height: 72%; position: absolute; overflow-y: auto; font-size: 1.5vmin;'>\n")
out_svg.write("</div>\n")
out_svg.write("</div>\n")
out_svg.write("</div>\n")
#boilerplate footer
out_svg.write("</body>\n")
out_svg.write("</html>\n")

out_svg.close()

#debug
#print(frequency_dictionary)
    #"#91a2ff",
    #"#649379",
    #"#5b8c45",
    #"#608b01",
    #"#729602",
    #"#8dab01",
    #"#aac301",
    #"#bfca00",
    #"#bbb00f",
    #"#a17c18",
    #"#864e18",
    #"#702c16",
    #"#601112"