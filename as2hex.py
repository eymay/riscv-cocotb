import subprocess

def as2hex(asm, inst):
    result = subprocess.run(['./dis.sh', asm, inst], stdout=subprocess.PIPE)
    #returns list of byte strings 
    return result.stdout.decode('utf-8').split()

