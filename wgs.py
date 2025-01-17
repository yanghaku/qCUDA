from subprocess import check_output, CalledProcessError

class Utilization:
    def __init__(self, gpu, memory):
        self.gpu    = float(gpu)
        self.memory = float(memory)
    def set_gpu(self, gpu):
        self.gpu    = gpu
    def set_mem(self, memory):
        self.memory = memory
    def set_id(self, id):
        self.id     = id
    def set_cap(self, wa, wb):
        self.cap    = wa*self.gpu + wb*self.memory

output_gpu = check_output('nvidia-smi --query-gpu=utilization.gpu --format=csv', shell=True)
output_gpu_split = output_gpu.split('\n')
device_num = len(output_gpu_split) - 2

d_gpu = []
for i in range(device_num):
    d_gpu.append(filter(str.isdigit, output_gpu_split[i+1]))
    #print d_gpu[i]

output_memory = check_output('nvidia-smi --query-gpu=memory.used --format=csv', shell=True)
output_memory_split = output_memory.split('\n')

d_memory = []
for i in range(device_num):
    d_memory.append(filter(str.isdigit, output_memory_split[i+1]))
    #print d_memory[i]


output_memory = check_output('nvidia-smi --query-gpu=memory.total --format=csv', shell=True)
output_memory_split = output_memory.split('\n')

for i in range(device_num):
    d_memory[i] = float(d_memory[i]) / float(filter(str.isdigit, output_memory_split[i+1]))
    #print d_memory[i]

Wa = 0.5
Wb = 0.5
device_obj=[]
for i in range(device_num):
    device_obj.append(Utilization(d_gpu[i], d_memory[i]))
    device_obj[i].set_cap(Wa, Wb)
    device_obj[i].set_id(i)
    #print device_obj[i].gpu
    #print device_obj[i].memory
    #print device_obj[i].cap
    #print device_obj[i].id

#print
device_obj.sort(key=lambda i: i.cap) 
#print device_obj[0].cap
print device_obj[0].id


#f = open(".select_g", 'w')
#s = str(device_obj[0].id)
#f.write(s)
