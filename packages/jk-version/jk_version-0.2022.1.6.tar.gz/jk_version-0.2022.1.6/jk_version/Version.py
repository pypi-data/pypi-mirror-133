



import typing
import re
import datetime











class Version(object):

	################################################################################################################################
	## Constructor
	################################################################################################################################

	#
	# Constructor
	#
	# @param		int[]|str version				The version string this object should represent
	#
	def __init__(self, version:typing.Union[str,list,tuple] = "0"):
		self.__epoch = 0
		self.__extra = None

		if isinstance(version, (list, tuple)):

			if len(version) == 0:
				raise Exception("Invalid version number: \"" + str(version) + "\"")

			for i in version:
				assert isinstance(i, int)

			self.__numbers = tuple(version)

		elif isinstance(version, str):

			try:
				m = re.match(r"^((?P<epoch>[0-9]+):)?(?P<version>[0-9\.]+)([\-~\+](?P<extra>.+))?$", version)
				if not m:
					raise Exception("Failed to parse version number: \"" + version + "\"")

				sEpoch = m.group("epoch")
				sVersion = m.group("version")
				sExtra = m.group("extra")
				if sEpoch:
					self.__epoch = int(sEpoch)
				if sExtra:
					self.__extra = sExtra

				# parse regular version number

				numbers = []
				for sVPart in sVersion.split("."):
					while (len(sVPart) > 1) and (sVPart[0] == "0"):		# remove trailing zeros of individual version components to allow accidental specification of dates as version information
						sVPart = sVPart[1:]
					numbers.append(int(sVPart))

				# ----

				self.__numbers = tuple(numbers)

			except Exception as ee:
				raise
				raise Exception("Failed to parse version number: \"" + version + "\"")

		else:
			raise Exception("Value of invalid type specified: " + str(type(version)))
	#

	################################################################################################################################
	## Public Properties
	################################################################################################################################

	@property
	def epoch(self) -> int:
		return self.__epoch
	#

	@property
	def extra(self) -> typing.Union[str,None]:
		return self.__extra
	#

	@property
	def length(self) -> int:
		return len(self.__numbers)
	#

	@property
	def numbers(self) -> list:
		return list(self.__numbers)
	#

	@property
	def isDateBase(self) -> bool:
		if len(self.__numbers) < 4:
			return False
		if self.__numbers[0] != 0:
			return False
		if (self.__numbers[1] < 2010) or (self.__numbers[1] > 2100):
			return False
		if (self.__numbers[2] < 1) or (self.__numbers[2] > 12):
			return False
		if (self.__numbers[3] < 1) or (self.__numbers[3] > 31):
			return False

		# everything seems to be plausible.

		return True
	#

	################################################################################################################################
	## Helper Methods
	################################################################################################################################

	################################################################################################################################
	## Public Methods
	################################################################################################################################

	def __hash__(self):
		return hash(self.__numbers)
	#

	def __str__(self):
		if (self.__epoch is None) or (self.__epoch == 0):
			ret = ""
		else:
			ret = str(self.__epoch) + ":"

		bFirst = True
		for v in self.__numbers:
			if bFirst:
				bFirst = False
			else:
				ret += "."
			ret += str(v)

		if self.__extra:
			ret += "-" + self.__extra

		return ret
	#

	def __repr__(self):
		return self.__str__()
	#

	def compareTo(self, other):
		if isinstance(other, str):
			other = Version(other)

		if isinstance(other, Version):
			aNumbers = [ self.__epoch ] + list(self.__numbers)
			bNumbers = [ other.__epoch ] + list(other.__numbers)

			length = len(bNumbers)
			if len(aNumbers) < length:
				while len(aNumbers) < length:
					aNumbers.append(0)
			else:
				length = len(aNumbers)
				while len(bNumbers) < length:
					bNumbers.append(0)

			for i in range(0, length):
				na = aNumbers[i]
				nb = bNumbers[i]
				x = (na > nb) - (na < nb)
				# print("> " + str(na) + "  " + str(nb) + "  " + str(x))
				if x != 0:
					return x
			return 0

		else:
			raise Exception("Incompatible types: 'Version' and " + repr(type(other).__name__))
	#

	def __cmp__(self, other):
		n = self.compareTo(other)
		return n
	#

	def __lt__(self, other):
		n = self.compareTo(other)
		#print "???? a=" + str(self)
		#print "???? b=" + str(other)
		#print "???? " + str(n)
		return n < 0
	#

	def __le__(self, other):
		n = self.compareTo(other)
		#print "???? a=" + str(self)
		#print "???? b=" + str(other)
		#print "???? " + str(n)
		return n <= 0
	#

	def __gt__(self, other):
		n = self.compareTo(other)
		return n > 0
	#

	def __ge__(self, other):
		n = self.compareTo(other)
		return n >= 0
	#

	def __eq__(self, other):
		n = self.compareTo(other)
		return n == 0
	#

	def __ne__(self, other):
		n = self.compareTo(other)
		return n != 0
	#

	def dump(self):
		print("Version<(")
		print("\tepoch=" + repr(self.__epoch))
		print("\tnumbers=" + repr(self.__numbers))
		print("\textra=" + repr(self.__extra))
		print(")>")
	#

	@staticmethod
	def now():
		dt = datetime.datetime.now()
		return Version([ 0, dt.year, dt.month, dt.day ])
	#

	@staticmethod
	def fromTimeStamp(t):
		dt = datetime.datetime.fromtimestamp(t)
		return Version([ 0, dt.year, dt.month, dt.day ])
	#

#
