Tag_Info="${BCyan}[INFO]${Color_Off} "      # INFO messages
Tag_Task="${BYellow}[TASK]${Color_Off} "	# TASK messages
Tag_Success="${BGreen}[SUCCESS]${Color_Off} "	# SUCCESS messages
Tag_Error="${BRed}[ERROR]${Color_Off} "     # ERROR messages
Tag_Command="${BYellow}[COMMAND]${Color_Off} " # COMMAND messages
Tag_Description="${White}[DESCRIPTION]${Color_Off} " # DESCRIPTION messages

log_with_timestamp() {
  	echo -e "${White}[${Gray}$(date '+%H:%M:%S')${White}]${Color_Off} $1"
}

write_info() {
	echo -e "${Tag_Info}${Cyan}$1${Color_Off}"
}

write_task() {
	echo -e "${Tag_Task}${Yellow}$1${Color_Off}"
}

write_success() {
	echo -e "${Tag_Success}${Green}$1${Color_Off}"
}

write_command() {
	echo -e "${Tag_Command}${Gray}$1${Color_Off}"
}

write_error() {
	echo -e "${Tag_Error}${Red}$1${Color_Off}"
}

write_description() {
	echo -e "${Tag_Description}${Gray}$1${Color_Off}"
}