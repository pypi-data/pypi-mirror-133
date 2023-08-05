import argparse,sys
class PromptInput(argparse.ArgumentParser):
	def add_argument(self, *args, prompt=True, secure=False, count = 0, required = False,**kwargs):
		if(count>0):
			if(required): # Need to do anything if the argument is req otherwise lib can itself add the default value.
				if(len(sys.argv) <= count):
					sys.argv.insert(count,input(kwargs['help']))
				elif(sys.argv[count]==''):
					sys.argv.pop(count)
					sys.argv.insert(count,input(kwargs['help']))
			else:
				if(len(sys.argv) <= count):
					sys.argv.insert(count,str(kwargs['default']))
				elif(sys.argv[count]==''):
					sys.argv.pop(count)
					sys.argv.insert(count,str(kwargs['default']))

		super().add_argument(*args,**kwargs)
