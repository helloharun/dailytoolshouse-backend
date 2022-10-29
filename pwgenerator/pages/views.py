from django.shortcuts import render

import string
import random

def passwordGenerator(request):
   context = {}
   if request.method == 'POST':
      passwordLength = request.POST.get('passwordLength',None)
      isCapLetter = request.POST.get('capLetter',None)
      isSmallLetter = request.POST.get('smallLetter',None)
      isDigits = request.POST.get('digits',None)
      isSpecialChars = request.POST.get('specialChars',None)
      isSimilarChars = request.POST.get('similarChars',None)
      isBeginWithALetter = request.POST.get('beginWithALetter',None)
      isRemoveDuplicateLetter = request.POST.get('removeDuplicateLetter',None)
      isRemoveSequentialLetters = request.POST.get('removeSequentialLetters',None)


      capitalLetter = ["Q","W","E","R","T","Y","U","P","A","S","D","F","G","H","J","K","Z","X","C","V","B","N","M"]

      smallLetter = ["m","n","b","v","c","x","z","k","j","h","g","f","d","s","a","p","y","t","r","e","w","q"]

      digits = [1, 2, 3, 4, 5, 6, 7, 8, 9];
      similarAlphaNumeric = ["i", "o", "l", "I", "O", "L", "0", "|"];
      specialChars = ["!",'"',";","#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@","[","]","^","_","`","{","}","~"]

      # total available strings
      total_strings = ''

      if isCapLetter is not None:
         total_strings = total_strings+"".join(capitalLetter)
      if isSmallLetter is not None:
         total_strings = total_strings+"".join(smallLetter)
      if isDigits is not None:
         total_strings = total_strings+"".join(map(str, digits))
      if isSpecialChars is not None:
         total_strings = total_strings+"".join(specialChars)
      if isSimilarChars is not None:
         total_strings = total_strings+"".join(similarAlphaNumeric)
      
      # if isBeginWithALetter is not None:
      #    total_strings = total_strings+"".join(specialChars)
      # if isRemoveDuplicateLetter is not None:
      #    total_strings = total_strings+"".join(specialChars)
      # if isRemoveSequentialLetters is not None:
      #    total_strings = total_strings+"".join(specialChars)



      # generated_password initialization
      generated_password = ''

      for i in range(int(passwordLength)):
         generated_password+=total_strings[random.randint(0, len(total_strings)-1)]
         # print(random.randint(0, len(total_strings)))

      
      # print('generated_password: ', generated_password)
      
      request.session['dth_generated_password'] = generated_password
      request.session['testing_DTH'] = generated_password

      context = {
         # 'lower':lower_string,
         # 'upper':upper_string,
         'digits': digits,
         # 'punctuations': punctuation,
         'generated_password':generated_password
      }
   try:
      pw = request.session['dth_generated_password']
      del request.session['dth_generated_password']
   except:
      pw = ''
   
   # print('PW: ', pw)
   context = {'pw':pw}
   return render(request, 'pwgenhome.html', context)