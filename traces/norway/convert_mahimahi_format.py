import os
import numpy as np


DATA_PATH = './test_sim_traces/'
OUTPUT_PATH = './mahimahi/'
BYTES_PER_PKT = 1500.0
MILLISEC_IN_SEC = 1000.0
BITS_IN_BYTE = 8.0


def main():
	files = os.listdir(DATA_PATH)

	for f in files:
		file_path = DATA_PATH +  f
		output_path = OUTPUT_PATH + f

		print(file_path)

		with open(file_path, 'r') as f, open(output_path, 'w') as mf:
			time_ms = []
			bytes_recv = []
			recv_time = []
			throughput_all = []
			for line in f:
				parse = line.split()
				if len(time_ms) > 0 and float(parse[0]) < time_ms[-1]:  # trace error, time not monotonically increasing
					break
				time_ms.append(np.floor(float(parse[0])*MILLISEC_IN_SEC))
				throughput_all.append(float(parse[1])*1000/BITS_IN_BYTE)
				#print([np.floor(float(parse[0])*MILLISEC_IN_SEC),float(parse[1])*BITS_IN_BYTE*1000000])
				#bytes_recv.append(float(parse[1]))
				#recv_time.append(float(parse[2]))

			time_ms = np.array(time_ms)
			#bytes_recv = np.array(bytes_recv)
			#recv_time = np.array(recv_time)
			#throughput_all = bytes_recv / recv_time
			throughput_all = np.array(throughput_all)

			millisec_time = 0
			mf.write(str(millisec_time) + '\n')

			for i in range(len(throughput_all)):

				throughput = throughput_all[i]
				
				pkt_per_millisec = throughput / BYTES_PER_PKT 

				millisec_count = 0
				pkt_count = 0

				while True:
					millisec_count += 1
					millisec_time += 1
					to_send = (millisec_count * pkt_per_millisec) - pkt_count
					to_send = np.floor(to_send)

					for k in range(int(to_send)):
						mf.write(str(millisec_time) + '\n')

					pkt_count += to_send
					print(time_ms[i])
					if millisec_count >= time_ms[i]:
						break
	

if __name__ == '__main__':
	main()