import os
import sys

prefix = '''digraph spdk {
    graph [
        rankdir = "LR"
        //splines=polyline
        overlap=false
    ];

    node [
        fontsize = "16"
        shape = "ellipse"\r
    ];

    edge [
    ];
'''
node_str = ""
edge_str = ""
dict_node = {}

color_arrary = ['red', 'green', 'blue', 'black','blueviolet','brown', 'cadetblue','chocolate','crimson','cyan','darkgrey','deeppink','darkred']


prefix_path = sys.argv[1]
current_path = os.getcwd()
cmd = "cd " + prefix_path + ";" + "find * -name \"*.h\" > " + current_path + "/data"
os.system(cmd)

f = open("data")
print ("//该目录下的.h文件如下:")
while True:
	line = f.readline()
	if not line:
		break
	print ("// " + line.rstrip('\n'))
	cFile = line.rstrip('\n').replace(".h", ".c")
	#print (line.replace(".h", ".c"))
	path = prefix_path + cFile
	if (os.path.exists(path)):
		print ("// " + cFile + " 存在")
		dict_node[cFile.replace(".c", "").replace("node", "node1").replace("-", "_").replace("/", "_")] = "1"

cmd = "cd " + prefix_path + ";" +  "grep \"#include \" * -nr > " + current_path + "/data"
os.system(cmd)

space4 = '    '
space8 = space4 + space4
space12 = space4 + space8
space16 = space4 + space12

colorIndex = 0
oldfileName = ""
f = open("data")
while True:
	line = f.readline()
	if not line:
		break
	line = line.rstrip('\n')
	if line.find("#include \"") != -1:

		#print (line)
		line = line.split(":")
		fileName = line[0]

		if (fileName.find(".c") == -1):
			continue

		includeFileName = line[2].replace("#include", "").replace("\"", "").replace(" ", "")
		cFile = includeFileName.replace(".h", "").replace("node", "node1").replace("-", "_").replace("/", "_")

		fileNameLabel = fileName.replace(".c", "").replace("node", "node1").replace("-", "_").replace("/", "_")

		#node_str = space4 + '\"' + file_name_wo_h + '\" [\n' + space8 + 'label = \"<head> '+ file_name_wo_h +'.h\l|\n' + space12 + '{|{\n'
		#print (fileName + " " + includeFileName)
		if (oldfileName == ""):
			node_str = space4 + '\"' + fileNameLabel + '\" [\n' + space8 + 'label = \"<head> '+ fileNameLabel +'\l|\n' + space12 + '{|{\n'
			node_str = node_str + space16 + '<'+ cFile + '> ' + includeFileName +  '\l|\n'
			if (cFile in dict_node and cFile != fileNameLabel):
				#edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"red\"]\n"
				edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"" + color_arrary[colorIndex] + "\"]\n" 
		
		elif (fileName == oldfileName):	
			node_str = node_str + space16 + '<'+ cFile + '> ' + includeFileName +  '\l|\n'
			if (cFile in dict_node  and cFile != fileNameLabel):
				#edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"red\"]\n"
				edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"" + color_arrary[colorIndex] + "\"]\n"
		else:
			node_str = node_str + space12 + '}}\"\n'
			node_str = node_str + space8 + 'shape = \"record\"\n' + space4 + '];\n'
			node_str = node_str + "\n"

			colorIndex = (colorIndex + 1) % len(color_arrary)
			node_str = node_str + space4 + '\"' + fileNameLabel + '\" [\n' + space8 + 'label = \"<head> '+ fileNameLabel +'\l|\n' + space12 + '{|{\n'
			node_str = node_str + space16 + '<'+ cFile + '> ' + includeFileName +  '\l|\n'
			if (cFile in dict_node and cFile != fileNameLabel):
				#edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"red\"]\n"
				edge_str = edge_str + fileNameLabel + ":" + cFile + "->" + cFile + ":head[color=\"" + color_arrary[colorIndex] + "\"]\n"

		oldfileName = fileName

node_str = node_str + space12 + '}}\"\n'
node_str = node_str + space8 + 'shape = \"record\"\n' + space4 + '];\n'

print (prefix + node_str + edge_str + "\n" + '}')
	#print (line.rstrip('\n'))
