from reedsolo import RSCodec, ReedSolomonError
import random

with open ("sample.txt","rb") as f:       # gives bytes of each character
   text_file = f.read()                      
RS = RSCodec(32)   #sets the extra bits of RS to 32
Encoded = RS.encode(text_file)      # added extra bytes


def apply_errors(p, data): #p is the probability of error
    for i in range(len(data)):
        number = random.random()
        if number <= p:
            changed = random.randint(0,255)
            while (data[i] == changed):       #changes until it's different
                changed = random.randint(0,255)
            data[i] = changed
    return data #returns error filled array
        
def RS_decode(byte_array):  #returns true or false based on success/ not success
    try: 
        Recovered = RS.decode(byte_array) #decodes it, stores in recoevered
        return (Recovered[0] == text_file) #prints true or false based on if stored matches
    except ReedSolomonError: #if too many errors to even reach, give false.
        return (False)

def repetition (text): #repetition code: triples text: 
   rep = text * 3
   return bytearray(rep)

def rep_decode (rep): # decodes correct message (tries)
   result = bytearray()
   x = len(rep) // 3
   for index in range(x): 
        if rep[index] == rep[x+index]:
            result.append(rep[index])
        elif rep[x+index] == rep[2*x+index]:
           result.append(rep[x+index])
        else:
            result.append(rep[index])
   return (result == text_file)



print(f"{'Damage':<8}{'RS':<10}{'Repetition':<12}") # makes the table
print("-" * 30)
trials = 200 
for p in [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07]: #loops through each p
    RS_success = 0 
    Rep_success = 0
    for runs in range(trials):
        Test = bytearray(Encoded) #place holder for RS encrypted
        Test = apply_errors(p,Test) #applies errors to the place holder
        if RS_decode(Test): #decodes place holder
            RS_success += 1
        if rep_decode(apply_errors(p,repetition(text_file))): # doesn't change anything but a temporary thing in memory
            Rep_success += 1
        

    print(f"{p:<8.0%}{RS_success / trials:<10.1%}{Rep_success / trials:<12.1%}") 
    print() # Print tables that show the repetition overhead, and the success percentage for RS and rep.
print(f"RS overhead: {(len(Encoded) - len(text_file)) / len(text_file):.1%}")
print("Repetition overhead: 200.0%")

Error_file = apply_errors(0.04, bytearray(Encoded)) #take error corrupted file, decode, and put in "recovered" File
recovered = RS.decode(Error_file)
with open ("recovered.txt","wb") as file:
    file.write(recovered[0])


    



        




    
