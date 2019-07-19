import string

import pygame

#Custom exceptions
class Overflow(Exception):
	"""Integer is greater than 999,999,999,999"""

#this function return a string of how-to-read a nber in range 0-999
def basic_read_3_members(s, region = 'north'):
	ns = ['Không', 'Một', 'Hai', 'Ba', 'Bốn', 'Năm', 'Sáu', 'Bảy', 'Tám', 'Chín']
	options = {'north':'Linh', 'south':'Lẻ'}
	#1-member nber
	if len(s) == 1:
		return ns[ord(s)-48]
	#2-member nber
	if len(s) == 2:
		if s == '10':
			return "Mười"
		elif s[0] == '1':
			if s[1] == '5':
				return "Mười Lăm"
			else:
				return "Mười " + ns[ord(s[1])-48]
		else:
			if s[1] == '0':
				return ns[ord(s[0])-48] + " Mươi"
			else:
				if s[1] == '5':
					return ns[ord(s[0])-48] + " Mươi Lăm"
				if s[1] == '1':
					return ns[ord(s[0])-48] + " Mươi Mốt"
				return ns[ord(s[0])-48] + " Mươi " + ns[ord(s[1])-48]
	#3-member nber
	if len(s) == 3:
		if s == '000':
			return ''
		elif int(s) % 100 == 0:
			return ns[ord(s[0])-48] + " Trăm"
		elif s[1] == '0':
			return ns[ord(s[0])-48] + " Trăm " + options[region] + " " + ns[ord(s[2])-48]
		elif s[2] == '0':
			if s[1] == '1':
				return ns[ord(s[0])-48] + " Trăm Mười"
			else:
				return ns[ord(s[0])-48] + " Trăm " + ns[ord(s[1])-48] + " Mươi"
		else:
			if s[1] == '1':
				if s[2] == '1':
					return ns[ord(s[0])-48] + " Trăm Mười Một"
				elif s[2] == '5':
					return ns[ord(s[0])-48] + " Trăm Mười Lăm"
				else:
					return ns[ord(s[0])-48] + " Trăm Mười " + ns[ord(s[2])-48]
			elif s[2] == '1':
				return ns[ord(s[0])-48] + " Trăm " + ns[ord(s[1])-48] + " Mươi Mốt"
			elif s[2] == '5':
				return ns[ord(s[0])-48] + " Trăm " + ns[ord(s[1])-48] + " Mươi Lăm"
			else:
				return ns[ord(s[0])-48] + " Trăm " + ns[ord(s[1])-48] + " Mươi " + ns[ord(s[2])-48]

#upgrade the function to a larger range (0-999 999 999 999)
def integer_to_vietnamese_numeral(n = 0, region = 'north', activate_tts = False):
	#Exceptions:
	if isinstance(activate_tts, bool) is False:
		raise TypeError('Argument "activate_tts" is not boolean')
	if isinstance(n, int) is False:
		raise TypeError("Not an integer")
	if n > 999999999999:
		raise Overflow("Integer is greater than 999,999,999,999")
	if n < 0:
		raise ValueError("Not a positive integer")

	if region not in ['north', 'south']:
		raise ValueError('Argument "region" has not a correct value')
	if isinstance(region, str) is False:
		raise TypeError('Argument "region" is not a string')

	#Main:
	options = {'north':'Nghìn', 'south':'Ngàn'}
	s = str(n)
	result = ''
	temp = ''
	#n < 1 000
	if len(s) <= 3:
		result = basic_read_3_members(s, region)
	#n < 1 000 000
	elif len(s) < 6:
		for i in range(0, len(s)%3):
			temp += s[i]
		result = basic_read_3_members(temp, region) + " " + options[region] + " " + basic_read_3_members(s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2], region)
	elif len(s) == 6:
		result = basic_read_3_members(s[0]+s[1]+s[2], region) + " " + options[region] + " " + basic_read_3_members(s[3]+s[4]+s[5], region)
	#n < 1 000 000 000
	elif len(s) < 9:
		for i in range(0, len(s)%3):
			temp += s[i]
		if s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2] == '000':
			result = basic_read_3_members(temp, region) + " Triệu " + basic_read_3_members(s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5], region)
		else:
			result = basic_read_3_members(temp, region) + " Triệu " + basic_read_3_members(s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2], region) + " " + options[region] + " " + basic_read_3_members(s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5], region)
	elif len(s) == 9:
		if s[3]+s[4]+s[5] == '000':
			result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Triệu " + basic_read_3_members(s[6]+s[7]+s[8], region)
		else:
			result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Triệu " + basic_read_3_members(s[3]+s[4]+s[5], region) + " " + options[region] + " " + basic_read_3_members(s[6]+s[7]+s[8], region)
	#n < 1 000 000 000 000
	elif len(s) < 12:
		for i in range(0, len(s)%3):
			temp += s[i]
		if s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2] == '000':
			if s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5] == '000':
				result = basic_read_3_members(temp, region) + " Tỷ " + basic_read_3_members(s[len(s)%3+6]+s[len(s)%3+7]+s[len(s)%3+8], region)
			else:
				result = basic_read_3_members(temp, region) + " Tỷ " + basic_read_3_members(s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5], region) + " " + options[region] + " " + basic_read_3_members(s[len(s)%3+6]+s[len(s)%3+7]+s[len(s)%3+8], region)
		else:
			if s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5] == '000':
				result = basic_read_3_members(temp, region) + " Tỷ " + basic_read_3_members(s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2], region) + " Triệu " + basic_read_3_members(s[len(s)%3+6]+s[len(s)%3+7]+s[len(s)%3+8], region)
			else:
				result = basic_read_3_members(temp, region) + " Tỷ " + basic_read_3_members(s[len(s)%3]+s[len(s)%3+1]+s[len(s)%3+2], region) + " Triệu " + basic_read_3_members(s[len(s)%3+3]+s[len(s)%3+4]+s[len(s)%3+5], region) + " " + options[region] + " " + basic_read_3_members(s[len(s)%3+6]+s[len(s)%3+7]+s[len(s)%3+8], region)
	else:
		if s[3]+s[4]+s[5] == '000':
			if s[6]+s[7]+s[8] == '000':
				result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Tỷ " + basic_read_3_members(s[9]+s[10]+s[11], region)
			else:
				result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Tỷ " + basic_read_3_members(s[6]+s[7]+s[8], region) + " " + options[region] + " " + basic_read_3_members(s[9]+s[10]+s[11], region)
		else:
			if s[6]+s[7]+s[8] == '000':
				result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Tỷ " + basic_read_3_members(s[3]+s[4]+s[5], region) + " Triệu " + basic_read_3_members(s[9]+s[10]+s[11], region)
			else:
				result = basic_read_3_members(s[0]+s[1]+s[2], region) + " Tỷ " + basic_read_3_members(s[3]+s[4]+s[5], region) + " Triệu " + basic_read_3_members(s[6]+s[7]+s[8], region) + " " + options[region] + " " + basic_read_3_members(s[9]+s[10]+s[11], region)
	if activate_tts is True:
		pygame.init()
		read = result.split(' ')
		for i in range(0, len(read)):
			sound = pygame.mixer.Sound('./sounds/vie/' + region + '/' + read[i] + '.ogg')
			channel = sound.play(0,1000,0)
			sound = pygame.time.delay(800)


	#return "result" as a string
	return result


def integer_to_english_numeral(n = 0, activate_tts = False):
    #Raise Exceptions:
    if isinstance(activate_tts, bool) is False:
        raise TypeError('Argument "activate_tts" is not a boolean')
    if isinstance(n, int) is False:
        raise TypeError("Not an integer")
    if n > 999999999999:
        raise Overflow("Integer is greater than 999,999,999,999")
    if n < 0:
        raise ValueError("Not a positive integer")


    d = { 0 : 'Zero',
          1 : 'One',
          2 : 'Two',
          3 : 'Three',
          4 : 'Four',
          5 : 'Five',
          6 : 'Six',
          7 : 'Seven',
          8 : 'Eight',
          9 : 'Nine',
          10 : 'Ten',
          11 : 'Eleven',
          12 : 'Twelve',
          13 : 'Thirteen',
          14 : 'Fourteen',
          15 : 'Fifteen',
          16 : 'Sixteen',
          17 : 'Seventeen',
          18 : 'Eighteen',
          19 : 'Nineteen',
          20 : 'Twenty',
          30 : 'Thirty',
          40 : 'Fourty',
          50 : 'Fifty',
          60 : 'Sixty',
          70 : 'Seventy',
          80 : 'Eighty',
          90 : 'Ninety'
    }

    tho = 1000          #thousand
    mil = tho * 1000    #million
    bil = mil * 1000    #billion
    tri = bil * 1000    #trillion

    result = ''

    if (n < 20):
        result = d[n]

    elif (n < 100):
        if n % 10 == 0:
            result = d[n]
        else:
            result = d[n // 10 * 10] + '-' + d[n % 10]

    elif (n < tho):
        if n % 100 == 0:
            result = d[n // 100] + ' Hundred'
        else:
            result = d[n // 100] + ' Hundred And ' + integer_to_english_numeral(n % 100, False)

    elif (n < mil):
        if n % tho == 0:
            result = integer_to_english_numeral(n // tho, False) + ' Thousand'
        else:
            result = integer_to_english_numeral(n // tho, False) + ' Thousand And ' + integer_to_english_numeral(n % tho, False)

    elif (n < bil):
        if (n % mil) == 0:
            result = integer_to_english_numeral(n // mil, False) + ' Million'
        else:
            result = integer_to_english_numeral(n // mil, False) + ' Million And ' + integer_to_english_numeral(n % mil, False)

    elif (n < tri):
        if (n % bil) == 0:
            result = integer_to_english_numeral(n // bil, False) + ' Billion'
        else:
            result = integer_to_english_numeral(n // bil, False) + ' Billion And ' + integer_to_english_numeral(n % bil, False)

    #Text-to-speech
    if activate_tts is True:
        pygame.init()
        temp1 = result.split(' ')
        for i in range(0,len(temp1)):
            temp2 = temp1[i].split('-')
            for j in range(0, len(temp2)):
                sound = pygame.mixer.Sound('./sounds/eng/' + temp2[j] + '.ogg')
                channel = sound.play(0, 1000, 0)
                sound = pygame.time.delay(800)

    return result

# print(integer_to_vietnamese_numeral(000))
# print(integer_to_vietnamese_numeral(405))
# print(integer_to_vietnamese_numeral(1915))
# print(integer_to_vietnamese_numeral(5061))
# print(integer_to_vietnamese_numeral(1002003))
# print(integer_to_vietnamese_numeral(1000000))
# print(integer_to_vietnamese_numeral(1030000))
# print(integer_to_vietnamese_numeral(1002003))
# print(integer_to_vietnamese_numeral(1002003004))
# print(integer_to_vietnamese_numeral(1002003004))
# print(integer_to_vietnamese_numeral(1002000004))
# print(integer_to_vietnamese_numeral(100000004))
# print(integer_to_vietnamese_numeral(999999999999))
# print(integer_to_vietnamese_numeral('9999999999990'))
# print(integer_to_vietnamese_numeral('4096'))
# print(integer_to_vietnamese_numeral(-1))
# print(integer_to_vietnamese_numeral(405, region='south'))
# print(integer_to_vietnamese_numeral(1971, region='north'))
# print(integer_to_vietnamese_numeral(1971, region='south'))
# print(integer_to_vietnamese_numeral(1, region=0))
# print(integer_to_vietnamese_numeral(1, region='whatever'))
# print(integer_to_vietnamese_numeral(405, activate_tts=True))
# print(integer_to_vietnamese_numeral(405, region='south', activate_tts=True))
# print(integer_to_vietnamese_numeral(1971, activate_tts=True, region='north'))
# print(integer_to_vietnamese_numeral(1971, region='south', activate_tts=True))
# print(integer_to_vietnamese_numeral(1, activate_tts=1))
# print(integer_to_english_numeral(96))
# print(integer_to_english_numeral(101))
# print(integer_to_english_numeral(405))
# print(integer_to_english_numeral(1971))
# print(integer_to_english_numeral(5061))
# print(integer_to_english_numeral('4096'))
# print(integer_to_english_numeral(-1))
# print(integer_to_english_numeral(1002003004, activate_tts=True))
# print(integer_to_english_numeral(1002003, activate_tts=True))
# print(integer_to_english_numeral(405, activate_tts=True))


