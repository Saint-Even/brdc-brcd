#!/usr/bin/env python3

import sys
import os
import pandas as pd
import numpy as np


class UserInterface:
    def __init__(self):
        pass

    def ask_user(self, message: str) -> str:
        return input("\n" + message + ": ")

    def notify_user(self, message: str) -> None:
        print(message)

    def choose_menu(self, heading: str, menu: dict) -> None:
        self.notify_user("\n" + heading)
        for i in menu:
            self.notify_user(f"{i}. {menu[i]['label']}")
        while True:
            try:
                choice = int(self.ask_user("Choose a menu option").strip())
                if choice in range(1, len(menu) + 1):
                    return menu[choice]["func"]
                else:
                    self.notify_user("The option must be in the menu")
            except(ValueError):
                self.notify_user("Enter a number")


class Barcoder:
    def __init__(self, fileName):
        self.inTable = pd.read_csv(fileName)
        self.outTable = pd.DataFrame()
        self.selectedPlateName = "None"

        #...source of the barcodes and protocol
        self.wellMap = {
            "A01": "CTCG",
            "B01": "TGCA",
            "C01": "ACTA",
            "D01": "CAGA",
            "E01": "AACT",
            "F01": "GCGT",
            "G01": "CGAT",
            "H01": "GTAA",
            "A02": "AGCG",
            "B02": "GATG",
            "C02": "TCAG",
            "D02": "TGCGA",
            "E02": "CGCTT",
            "F02": "TCACG",
            "G02": "CTAGG",
            "H02": "ACAAA",
            "A03": "TTCTG",
            "B03": "AGCCG",
            "C03": "GTATT",
            "D03": "CTGTA",
            "E03": "ACCGT",
            "F03": "GCTTA",
            "G03": "GGTGT",
            "H03": "AGGAT",
            "A04": "ATTGA",
            "B04": "CATCT",
            "C04": "CCTAG",
            "D04": "GAGGA",
            "E04": "GGAAG",
            "F04": "GTCAA",
            "G04": "TAATA",
            "H04": "TACAT",
            "A05": "TCGTT",
            "B05": "GGTTGT",
            "C05": "CCACGT",
            "D05": "TTCAGA",
            "E05": "TAGGAA",
            "F05": "GCTCTA",
            "G05": "CCACAA",
            "H05": "CTTCCA",
            "A06": "GAGATA",
            "B06": "ATGCCT",
            "C06": "AGTGGA",
            "D06": "ACCTAA",
            "E06": "ATATGT",
            "F06": "ATCGTA",
            "G06": "CATCGT",
            "H06": "CGCGGT",
            "A07": "CTATTA",
            "B07": "GCCAGT",
            "C07": "GGAAGA",
            "D07": "GTACTT",
            "E07": "GTTGAA",
            "F07": "TAACGA",
            "G07": "TGGCTA",
            "H07": "TATTTTT",
            "A08": "CTTGCTT",
            "B08": "ATGAAAG",
            "C08": "AAAAGTT",
            "D08": "GAATTCA",
            "E08": "GAACTTG",
            "F08": "GGACCTA",
            "G08": "GTCGATT",
            "H08": "AACGCCT",
            "A09": "AATATGG",
            "B09": "ACGTGTT",
            "C09": "ATTAATT",
            "D09": "ATTGGAT",
            "E09": "CATAAGT",
            "F09": "CGCTGAT",
            "G09": "CGGTAGA",
            "H09": "CTACGGA",
            "A10": "GCGGAAT",
            "B10": "TAGCGGA",
            "C10": "TCGAAGA",
            "D10": "TCTGTGA",
            "E10": "TGCTGGA",
            "F10": "ACGACTAG",
            "G10": "TAGCATGG",
            "H10": "TAGGCCAT",
            "A11": "TGCAAGGA",
            "B11": "TGGTACGT",
            "C11": "TCTCAGTG",
            "D11": "CGCGATAT",
            "E11": "CGCCTTAT",
            "F11": "AACCGAGA",
            "G11": "ACAGGGA",
            "H11": "ACGTGGTA",
            "A12": "CCATGGGT",
            "B12": "CGCGGAGA",
            "C12": "CGTGTGGT",
            "D12": "GCTGTGGA",
            "E12": "GGATTGGT",
            "F12": "GTGAGGGT",
            "G12": "TATCGGGA",
            "H12": "TTCCTGGA"
        }

    def filterMenu(self):
        ui = UserInterface()
        #menu values are set here, func must match a filter function
        MENU = {
            2:{
                "label": "2022 Plate Organizers",
                "func": "Filter_2022"
            },
            1:{
                "label": "2021 Plate Organizers",
                "func": "Filter_2021"
            },
            0:{
                "label": "Method Testing",
                "func": "Filter_Testing"
            }
        }

        fnStr = ui.choose_menu("Filter Menu", MENU)
        fn= getattr(self, fnStr, None)
        if fn is not None:
            fn()

    def Filter_Testing(self):
        print("TEST this section is experimental")
        barcode = self.wellMap['A01']
        print(barcode)

    def Filter_2021(self):
        #show summary of spreadsheet
        print("\nColumn Names")
        print(self.inTable.columns)
        summary = self.inTable.drop(columns=['well_A01', 'project_name', 'Sample', 'Source'])
        summary = summary.drop_duplicates()
        print("\nPlate Organizer Summary")
        print(summary)
        #user pick plate id, validate
        plateMax= summary['plate_num'].max()
        plateNum = 0
        while True:
            try:
                choice = int(input("\nSelect a plate number: ").strip())
                if choice in range(1, plateMax+1):
                    plateNum = choice
                    break
                else:
                    print("The option must be in the plate_num column")
            except(ValueError):
                print("Enter a number")


        #subset to intermediate
        plateTable= self.inTable.loc[self.inTable["plate_num"] == plateNum]
        #save the selected plate name
        plateTable= plateTable.reset_index()
        self.selectedPlateName= plateTable.loc[1,'plate_name']
        plateTable= plateTable.drop(columns=['index','plate_num', 'plate_name', 'project_name', 'Source'])

        #convert well locations to barcodes
        plateTable['well_A01']= plateTable['well_A01'].apply(self.wellToBC)
        self.outTable= plateTable

        #call to format check and pass the column name of the Sample Names
        self.format('Sample')

    def Filter_2022(self):
        #show summary of spreadsheet
        print("\nColumn Names")
        print(self.inTable.columns)
        print("\nPlate Organizer Summary")
        summary = self.inTable.drop(columns=['well_A01', 'project_name', 'Sample', 'Source'])
        summary = summary.drop_duplicates()
        print(summary)

        # user pick plate id, validate
        plateMax = summary['plate_num'].max()
        plateMax = plateMax.astype(np.int64)
        plateNum = 0
        while True:
            try:
                choice = int(input(f"\nSelect a plate number, out of {plateMax}: ").strip())
                if choice in range(1, plateMax+1):
                    plateNum = choice
                    break
                else:
                    print("The option must be in the plate_num column")
            except(ValueError):
                print("Enter a number")

        # subset to intermediate
        plateTable = self.inTable.loc[self.inTable["plate_num"] == plateNum]
        # save the selected plate name
        plateTable = plateTable.reset_index()
        self.selectedPlateName = plateTable.loc[1, 'plate_name']
                                              
        plateTable = plateTable.drop(columns=['index',
                                              'plate_num',
                                              'plate_name',
                                              'project_name',
                                              'Source',
                                              'Field_plot22',
                                              'Nursery',
                                              'Unnamed: 8',
                                              'Unnamed: 9',
                                              'Unnamed: 10',
                                              'Unnamed: 11'])
        # print(plateTable.columns) # well_A01 and Sample only remaining

        #convert well locations to barcodes
        plateTable['well_A01']= plateTable['well_A01'].apply(self.wellToBC)
        self.outTable= plateTable

        #call to format check and pass the column name of the Sample Names
        self.format('Sample')

    def wellToBC(self, wellLoc: str):
        #convert location to barcodes using the map dictionary
        return self.wellMap[wellLoc]

    def format(self, sampleCol: str):
        #check outTable format
        self.outTable[sampleCol]= self.outTable[sampleCol].apply(self.testFormat)

    def testFormat(self, sampleName: str):
        #compare argument to a cleaned version, basecase
        cleanName= self.nameCleaner(sampleName)
        if cleanName == sampleName:
                return cleanName
        while True:
            #repeat until valid format is found
            print(f"\nThis sample name contains invalid characters: {sampleName}\n\tUse only a-z,A-Z,_,-,0-9\n\tDo not use spaces")
            useSub= input(f"Enter 'n' to type a new name\nOR\nEnter 'y' to replace with: {cleanName} : ")
            if useSub == 'y':
                #use cleaned suggestion
                return cleanName
            elif useSub == 'n':
                #recursive call with user input
                suggestedName= input(f"Enter the new name of the sample {sampleName}:")
                return self.testFormat(suggestedName)

    def nameCleaner(self, sampleName: str):
        #problem character replacement
        return sampleName.replace(" ", "_").replace("(", "-").replace(")", "-").replace(".", "_")
        #...strip end characters



    def write(self):
        #optional print to screen
        if input("\nEnter 'y' to view the barcode file: ") == 'y':
            print(self.outTable)
        #user filename
        fileNameDef = f"{self.selectedPlateName}_barcodes.txt"
        if input(f"\nEnter 'y' to use {fileNameDef} as the file name: ") == 'y':
            fileName = fileNameDef
        else:
            fileName= input(f"\nFor the selected plate: {self.selectedPlateName}\nEnter a name for the produced barcode file\nExample: <Reads_PlateDataFile>_barcodes.txt: ")
        #write to disk
        self.outTable.to_csv(fileName, sep='\t', header=False, index=False)

    def reset(self):
        self.outTable = pd.DataFrame()
        self.selectedPlateName= "None"

    def run(self):
        self.filterMenu()
        #self.format() called by the filter selection
        self.write()
        self.reset()


def main():
    try:
        fileName = sys.argv[1]
    except IndexError as e:
        #print(e)
        raise Exception("Provide a plate organizer file name")
    #get plate organizer file name
    exists = False
    try:
        exists = os.path.exists(fileName)
    except Exception as e:
        print(e)
        print("Argument is not a valid file name")
    if not exists:
        raise Exception("The file name is not a file")
    #greeting
    print(f"\n║▌║█║▌│║▌║▌█\n║▌║█║▌│║▌║▌█\n║▌║█║▌│║▌║▌█\n║▌BRDC BRCD█\n")
    #instantiate object
    brcd = Barcoder(fileName)
    #run with optional loop
    again = True
    while again:
        brcd.run()
        #rerun or  quit
        a = input("Enter 'y' to run again: ")
        if a == 'y' or a == 'Y':
            again = True
        else:
            again = False

if __name__ == '__main__':
    main()
