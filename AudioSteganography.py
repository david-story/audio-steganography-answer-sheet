import struct
import sys
"""""
AudioSteganography.py
Version 1.0
Written By David Story

Description:
    AudioSteganography is a library created to provide tools to hide messages inside of audio files. This library works
    in conjunction with the AudioParse library to take lists of audio information from a 16-bit .wav file, and then
    encode or decode information in it. 

    For more information on how the Python Standard Library functions work, visit the documentation
    here as follows:

    Python Standard Library: https://docs.python.org/3/library/index.html

    For questions about this library you may email me at: storyd@sonoma.edu

"""""
# Licensing Information for this Library
""""
MIT License

Copyright (c) 2018 David Andrew Story

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#########################################################################
#                             Start Code                                #
#########################################################################

class InputFile:
    """
    InputFile Class

    Description: This class is designed to open an existing text file as defined by the user. It determines the amount
                 of bytes and bits that make up the contents of the file. It opens the file in a read-only mode. It
                 stores the name given to the file, a list of characters that make up the list, and a list of integers
                 that correspond to the ASCII values of these characters.

                 There are a few functions of the class that are called once you call the class. These are:

                 openfile()
                 calculateBitsAndBytes()
                 createIntList()

                 openfile() does what it sounds like it does, it opens the file, throwing an exception if this fails,
                 and calls the two other functions to set the parameters of the class. The file is read and a list of
                 characters is created for charlist[]

                 calculateBitsAndBytes() takes the charlist[] and increments the totalBits and totalBytes variable to
                 define the contents of the data.

                 createIntList() takes the charlist[] and makes a new list in the class called intolist[] that is
                 essentially a copy of char list but with the char values converted to their ASCII integer form.

    """
    def __init__(self, filename):
        """
        :param filename:
        """
        self.totalBits = 0
        self.totalBytes = 0
        self.charlist = []
        self.intlist = []
        self.filestr = ""
        self.filename = filename
        self.openfile()

    def openfile(self):
        """
        :return none:
        """
        # try-except to catch any file opening errors
        # if you get an error here, check that you have a .txt in the filename
        # or check that you specify either the directory location of the textfile
        # or make sure that the file is in the current directory (directory
        # where you are running your python file)
        try:
            # opens file in read mode to variable file
            file = open(self.filename, "r")
            # for characters in the file
            for item in file.read():
                # appends each character to the char list
                self.charlist.append(item)
            # appends NULL at the end to be our sentinel byte
            self.charlist.append(None)
            # calls function to add how many bits & bytes in the file
            self.totalBits, self.totalBytes = self.calculateBitsAndBytes()
            # closes the file
            file.close()
            # opens the file again in read mode, I could have also just made a string by iterating through
            # the char list[], but I wrote this portion at 1 am and I am commenting this now at 8 am.
            file = open(self.filename, "r")
            self.filestr = file.read()
            file.close()
            self.createIntList()

        except:
            # Broad exception that just catches any errors from file and quits the program
            print("Could not create file, check file name or that file is in current directory.")
            print("Exiting program.")
            sys.exit()

    def calculateBitsAndBytes(self):
        """
        :return bit byte:
        """
        bit = 0
        byte = 0
        # for characters in the list of characters
        for i in range(len(self.charlist)):
            # adds 8 bits per character
            bit += 8
            # adds 1 byte per character
            byte += 1
        # returns them for fun too
        return bit, byte

    def createIntList(self):
        """
        :return none:
        """
        # creates a new list for the integer ASCII values of the characters
        intlist = []
        # for characters in the char list - 1 (can't convert NULL to int in Python)
        for i in range(len(self.charlist)-1):
            # append the converted char -> int to new list
            intlist.append(ord(self.charlist[i]))
        # appends 0x00 as our new sentinel that is an int
        intlist.append(0)
        # adds this list to the class
        self.intlist = intlist


def encode(list, textfile):
    """
    :param list:
    :param textfile:
    :return encodedAudio:

    Description: This file takes input
    """
    file = InputFile(textfile)
    encodedAudio = []
    audioNum = 0
    # Some printing info is in here if you are stuck
    """"
    print(file.charlist)
    print("Total characters in our text file is: ", file.totalBytes)
    print("So the total bits we have to encode in the audio is: ", file.totalBits)
    print("Looking at the audio samples, we have", len(list), "audio samples.")
    print("\nSince we are assuming this 16-bit signed integer is our 'byte' for this project,")
    print("that means we can hide 1 bit in each of the audio sample 'bytes'.")

    if(len(list) < file.totalBits):
        print("\nBut since we have more bits in the text file than the audio sample bytes, we cannot hide our message.")
        sys.exit()
    elif(len(list) == file.totalBits):
        print("\nSince we have as many audio samples as bits, we can hide all of the message in the entire length of"
              "this audio file!")
    elif(len(list) > file.totalBits):
        print("\nSince we have more audio samples than bits, we can hide all of bits from the text file in the audio"
              "samples.")
    else:
        print("Something else happened! Ask an instructor for help")
        sys.exit(-1)
    """""
    # If we have equal or greater than amount of audio bytes to encode textfile bits into
    if len(list) >= file.totalBits:
        # for every character in the textfile
        for val in file.intlist:
            # for every bit in the character
            for i in range(7, -1, -1):
                # encode bit from left to right into the audio bytes
                bitToEncode = readBit(val, i)
                if list[audioNum] != abs(list[audioNum]):
                    negative = True
                else:
                    negative = False
                newVal = writeBit(abs(list[audioNum]), bitToEncode)
                if negative == True:
                    encodedAudio.append(-1*newVal)
                else:
                    encodedAudio.append(newVal)
                audioNum += 1

        #print(list)
        #print(encodedAudio)
        #print(encodedAudio + list[audioNum:])
        totalEncode = encodedAudio + list[audioNum:]

        return encodedAudio + list[audioNum:]

    else:
        print("Not enough samples to encode message in.")
        sys.exit(-1)

def decode(list, newfilename):
    """
    :param list:
    :param newfilename:
    :return strMessage or garbage:
    """
    # makes empty list to hold bits extracted
    bitlist = []
    # for all the bits in each audio sample
    for bits in list:
        # We want to treat this data as unsigned, so we abs() each audio sample value
        # then read the LSB of that audio same and append it to the bit list
        bitlist.append(readBit(abs(bits), 0))
    # Based on number of bits in our bit list, we can determine the amount of bytes by dividing the length by 8
    potentialBytes = determineTotalBytes(bitlist)
    # string variable to hold a bit string of our new data byte
    newByte = ""
    # boolean for determining if we have discovered a 0x00 sentinel byte that indicates we can stop looking for data
    endByte = False
    # counter makes sure we only append 8 bits to each new byte
    counter = 0
    # message holds our new characters we discover!
    message = []
    # for the length of potential bits
    for i in range(potentialBytes):
        # if we haven't appended 8 bits or we haven't discovered the sentinel
        if counter < 8 and endByte == False:
            # We add the newByte + a string of next bit in the bit list
            newByte += str(bitlist[i])
            # We increment the counter to indicate we added a bit
            counter += 1
        # else if we have already gotten 8 bits for our new data byte
        elif counter >= 8:
            # We get the ascii int value of the character by sequestering the base-2 string into its int form
            character = int(newByte, 2)
            # if our new character is equal zero then we have found our sentinel byte
            if(character == 0):
                # so this is true, we can exit the program!
                endByte = True
            # we append our new message as a character to the message list
            message.append(chr(character))
            # we reset newByte
            newByte = ""
            # and add a bit
            newByte += str(bitlist[i])
            # we reset the counter
            counter = 0
            # and add one to indicate we added a bit (you can also remove this line and make the above line counter = 1)
            counter += 1
        # if our end byte is true, we are done!
        elif endByte == True:
            # make a string to hold a string of our message
            strMessage = ""
            # for characters in the message list
            for characters in message:
                # we just add the characters to the string
                strMessage += characters
            # We write this message to a file, with our given file name from the input
            writeMessageToFile(strMessage, newfilename)
            # and we return the string of the message
            return strMessage

    # This section catches if there is no sentinel or the message was too long and was somehow encoded into the
    # audio sample
    print("No message found in signal (No sentinel encountered).")
    print("Returning string and file of random bytes found in message.")
    garbage = ""
    for things in message:
        garbage += things
    return garbage

def writeMessageToFile(message, filename):
    """
    :param message:
    :param filename:
    :return none:
    """
    # try-except to catch any file creation errors
    try:
        # opens new file based on file name provided
        newtext = open(filename, "w")
        # writes the message to the text file
        newtext.write(message)
        # closes the file
        newtext.close()
    except:
        print("Unable to open and write to file. Check file name and extension.")
        sys.exit()
    return

def determineTotalBytes(list):
    """
    :param list:
    :return total:
    """
    # Returns the length of the list divided by 8 as an integer (no remainder)
    return int(len(list) / 8)

def writeBit(integer, boolean):
    """
    :param integer boolean:
    :return integer:

    Description: This function takes in an integer and a boolean value. The integer is one of the samples from the
                 audio data. The boolean determines what the value of the least significant bit should be changed to.
                 The function returns the new integer with the set bit value.
    """
    # If we want to set a 1 in the LSB
    if boolean == True:
        # ORs the integer with 0x01
        value = integer | 0x01
    # We want to set a 0 in the LSB
    else:
        # ANDs the integer with the inverse of 0x01
        value = integer & ~0x01
    # Returns new value
    return value

def readBit(integer, position):
    """
    :param integer:
    :return boolean:

    Description: This function will take in an integer and a position value. The return will be a boolean based on
                 whether the bit is 1 or 0 at the requested position of the integer.

                 Example: integer = 252, which in binary is 1010 1010. This is a byte, where the LSB is at position
                          0 and the MSB is at position 7. With the above integer, position 1 is 1, position 3 is 0,
                          and position 4 is 1 and so on.
    """
    # Left shifts 0x01 by the position number, which is then AND'd with the absolute value of the passed integer,
    # This resulting value is then right shifted by the position.
    # This basically is how you can 'capture' the bit at a certain location and return its value as a boolean
    return ((0x01 << position) & abs(integer)) >> position

#########################################################################
#                              End Code                                 #
#########################################################################
