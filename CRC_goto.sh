#!/usr/bin/expect -f
set timeout -1
if {[lindex $argv 0] == "1"} {
	spawn scp -r Selected/ jliu16@crcfe02.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/
} elseif {[lindex $argv 0] == "2"} {
	spawn scp -r Selected_2/ jliu16@crcfe02.crc.nd.edu:~/Private/Research/2017/DCGAN/A-DCGAN-tensorflow/
} elseif {[lindex $argv 0] == "3"} {
	spawn scp model.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/
} elseif {[lindex $argv 0] == "4"} {
	spawn scp data/pre_noise/DtP.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/data/pre_noise/DtP1.py
} elseif {[lindex $argv 0] == "5"} {
	spawn scp data/pre_noise/test_ibm.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/data/pre_noise/test_ibm.py
} elseif {[lindex $argv 0] == "6"} {
        spawn scp main.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/main.py
} elseif {[lindex $argv 0] == "7"} {
        spawn scp DCGAN/DCGAN-tensorflow/data/pre_noise/test_ibm_1.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/data/pre_noise/
} elseif {[lindex $argv 0] == "8"} {
        spawn scp DCGAN/DCGAN-tensorflow/utils.py jliu16@crcfeib01.crc.nd.edu:~/Private/Research/2017/DCGAN/DCGAN-tensorflow/utils.py
}




expect {
	"yes/no" {
		send "yes\r"
		exp_continue
	}
	"password: " {
		send "412512axfDyk\r"
	}
}
interact
