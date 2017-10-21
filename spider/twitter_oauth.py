# -*- encoding: utf-8 -*-
class TwitterOauth:
	def __init__(self, key_path):
		f = open(key_path, 'r')
		self.data = {}
		for line in f:
			one_line = line.strip()
			if(len(one_line)!=0):
				str_split = one_line.split("=")
				print("Split: "+str_split[0]+" "+str_split[1])
				self.data[str_split[0]] = str_split[1]

	def get_consumer_key(self):
		return self.data['CONSUMER_KEY']

	def get_consumer_secret(self):
		return self.data['CONSUMER_SECRET']

	def get_oauth_token(self):
		return self.data['OAUTH_TOKEN']

        def get_oauth_token_secret(self):
		return self.data['OAUTH_TOKEN_SECRET']

