"""Main module."""
"""
Source Name:   Objectid To Text Gp ToolSets.pyt
Version:       ArcGIS 10.5
Author:        Nur Yahya.
Description:   Python tool to Convert Numeric OBJECTID field of a Feature Class to english Alphabet
               .
"""
# -*- coding: utf-8 -*-
import arcpy
import os
import time


class Toolbox(object):
    def __init__(self):
        self.label = "Objectid To Text Gp Toolbox"
        self.alias = "General"


        self.tools = [Objectid_to_text]



class Objectid_to_text(object):
    def __init__(self):
        self.label = "ObjectID to English Text"
        self.description = "This Tool Converts OBJECTID " + \
                           "to English text . The Result is Populated in predefined field " + \
                           "Name : Textual."
        self.canRunInBackground = False
        self.category = "General Tools"


    def getParameterInfo(self):
        # Define parameter definitions

        # Input Features parameter
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="Feature Class",
            parameterType="Required",
            direction="Input")


        textual_field = arcpy.Parameter(
            displayName="Textual Field",
            name="Textual_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input")

        textual_field.value = "Textual"

        # Derived Output Features parameter
        out_features = arcpy.Parameter(
            displayName="Output Features",
            name="out_features",
            datatype="Feature Class",
            parameterType="Derived",
            direction="Output")
        # Required  Vs Output is ---> The user will select the location of the Output
        # Drived Vs Output is ------> Is For Modification
        out_features.parameterDependencies = [in_features.name]
        out_features.schema.clone = True

        parameters = [in_features, textual_field, out_features]
        return parameters
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateMessages(self, parameters):  # must
        return

    def execute(self, parameters,messages):
        readTime = 2.5  # Pause to read what's written on dialog

        messages.AddMessage(os.getenv("username") + " welcome to ArcEthio Tools")
        time.sleep(readTime)

        arcpy.SetProgressorLabel("You are running ArcEthio Dire Toolsets")
        time.sleep(readTime)
        fc = parameters[0].valueAsText
        fieldName = parameters[1].valueAsText

        if fieldName in ["#", "", None]:
            fieldName = "Textual"
        arcpy.AddField_management(fc, fieldName,'TEXT')
        fields = ["OBJECTID", fieldName]
        cursor = arcpy.da.UpdateCursor(fc, fields)

        mydict = {}
        for row in cursor:
            k = row[0]
            v = row[1]
            mydict[k] = v

            for k, v in mydict.items():
                integer = str(k)
                while not (integer.isdigit()):
                    print("Only Numbers are allowed")
                    print("Type any number here ")
                    integer = input()
                ones = {'0': "", '1': "one ", '2': "two ", '3': "three ", '4': "four ", '5': "five ", '6': "six ",
                        '7': "seven ", '8': "eight ", '9': "nine ", '10': "ten "}
                teens = {'0': "ten", '1': "eleven", '2': "twelve", '3': "thirteen", '4': "fourteen", '5': "fifteen",
                         '6': "sixteen", '7': "seventeen", '8': "eighteen", '9': "nineteen"}
                dece = {'0': "", '2': "twenty ", '3': "thirty", '4': "forty", '5': "fifty", '6': "sixty",
                        '7': "seventy",
                        '8': "eighty ", '9': "ninety"}
                hundruds = {'0': "", '1': "one hundred ", '2': "two hundred ", '3': "three hundred ",
                            '4': "four hundred ",
                            '5': "five hundred ", '6': "six hundred ", '7': "seven hundred ", '8': "eight hundred ",
                            '9': "nine hundred "}
                comm_word = {'3': "thousand ", '6': "million ", '9': "billion "}
                word = ""
                integer_side = integer
                int_length = len(integer)
                integer_change = len(integer)
                change = 3

                while integer_change > 0:
                    if integer == "0":
                        word = "zero"
                    elif integer == "1":
                        word = "one"
                        break
                    if integer_side[integer_change - 2] == "1":
                        for digit in teens:
                            if integer_side[integer_change - 1] == digit:
                                word = teens[digit] + word
                    else:
                        for digit_1 in ones:
                            if integer_side[integer_change - 1] == digit_1:
                                word = ones[digit_1] + word
                        if integer_change > 1:
                            for digit_2 in dece:
                                if integer_side[integer_change - 2] == digit_2:
                                    word = dece[digit_2] + word
                    if integer_change > 2:
                        for digit_3 in hundruds:
                            if integer_side[integer_change - 3] == digit_3:
                                word = hundruds[digit_3] + word
                    if integer_change > 3:
                        word = comm_word[str(change)] + word
                    change = change + 3

                    integer_change = integer_change - 3

                    row[1] = word
                if k == 1 or k == "1" or row[0] == 1:
                    row[1] = "one"
                cursor.updateRow(row)

        del cursor







